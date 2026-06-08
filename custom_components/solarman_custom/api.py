"""Solarman Cloud API client."""
from __future__ import annotations

import hashlib
import logging
import time
from typing import Any

import aiohttp

from .const import (
    BASE_URL,
    ENDPOINT_DEVICE_CURRENT,
    ENDPOINT_STATION_BASE,
    ENDPOINT_STATION_DEVICE,
    ENDPOINT_STATION_LIST,
    ENDPOINT_STATION_REALTIME,
    ENDPOINT_TOKEN,
    TOKEN_EXPIRY_BUFFER,
)

_LOGGER = logging.getLogger(__name__)


class SolarmanApiError(Exception):
    """Base exception for Solarman API errors."""


class SolarmanAuthError(SolarmanApiError):
    """Authentication error."""


class SolarmanApi:
    """Client for the Solarman Open API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
        app_id: str,
        app_secret: str,
        device_sn: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._email = email
        self._password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self._app_id = app_id
        self._app_secret = app_secret
        self._device_sn = device_sn

        self._token: str | None = None
        self._token_expiry: float = 0
        self._station_id: int | None = None
        self._battery_sn: str | None = None
        self._collector_sn: str | None = None

    @property
    def station_id(self) -> int | None:
        """Return the station ID."""
        return self._station_id

    @property
    def battery_sn(self) -> str | None:
        """Return the battery serial number."""
        return self._battery_sn

    @property
    def collector_sn(self) -> str | None:
        """Return the collector serial number."""
        return self._collector_sn

    async def _ensure_token(self) -> str:
        """Ensure we have a valid access token."""
        if self._token and time.time() < self._token_expiry:
            return self._token

        _LOGGER.debug("Requesting new access token")
        url = f"{BASE_URL}{ENDPOINT_TOKEN}"
        params = {"appId": self._app_id, "language": "en"}
        payload = {
            "appSecret": self._app_secret,
            "email": self._email,
            "password": self._password_hash,
        }

        try:
            async with self._session.post(
                url, params=params, json=payload, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                data = await resp.json()
        except Exception as err:
            raise SolarmanApiError(f"Connection error during authentication: {err}") from err

        if not data.get("success", False):
            code = data.get("code", "unknown")
            msg = data.get("msg", "unknown error")
            raise SolarmanAuthError(f"Authentication failed [{code}]: {msg}")

        self._token = data.get("access_token")
        # Token typically expires in 7200s (2 hours); refresh early
        expires_in = data.get("expires_in", 7200)
        self._token_expiry = time.time() + expires_in - TOKEN_EXPIRY_BUFFER

        if not self._token:
            raise SolarmanAuthError("No access_token in response")

        _LOGGER.debug("Token obtained, expires in %ds", expires_in)
        return self._token

    async def _api_call(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Make an authenticated API call."""
        token = await self._ensure_token()
        url = f"{BASE_URL}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {token}",
        }

        try:
            async with self._session.post(
                url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                data = await resp.json()
        except Exception as err:
            raise SolarmanApiError(f"API call to {endpoint} failed: {err}") from err

        if not data.get("success", True):
            code = data.get("code", "unknown")
            msg = data.get("msg", "unknown error")
            # If token expired, invalidate and retry once
            if "token" in msg.lower() or code in ("2101019",):
                _LOGGER.debug("Token expired, refreshing")
                self._token = None
                self._token_expiry = 0
                return await self._api_call(endpoint, payload)
            _LOGGER.warning("API error [%s]: %s (endpoint: %s)", code, msg, endpoint)

        return data

    async def discover_station(self) -> dict[str, Any]:
        """Discover station ID and all devices."""
        # Get station list
        data = await self._api_call(ENDPOINT_STATION_LIST, {"page": 1, "size": 20})
        stations = data.get("stationList", [])
        if not stations:
            raise SolarmanApiError("No stations found for this account")

        self._station_id = stations[0].get("id")
        _LOGGER.info("Discovered station ID: %s", self._station_id)

        # Get station details
        station_detail = await self._api_call(
            ENDPOINT_STATION_BASE, {"stationId": self._station_id}
        )

        # Get devices for station
        devices_data = await self._api_call(
            ENDPOINT_STATION_DEVICE,
            {"stationId": self._station_id, "page": 1, "size": 50},
        )

        devices = devices_data.get("deviceListItems", [])
        for device in devices:
            dtype = device.get("deviceType", "")
            dsn = device.get("deviceSn", "")
            _LOGGER.info("Found device: %s (type: %s)", dsn, dtype)

            if dtype == "BATTERY" and not self._battery_sn:
                self._battery_sn = dsn
            elif dtype == "COLLECTOR" and not self._collector_sn:
                self._collector_sn = dsn

        return {
            "station": stations[0],
            "station_detail": station_detail,
            "devices": devices,
        }

    async def get_inverter_data(self) -> dict[str, str]:
        """Get current data from the inverter, returned as {key: value}."""
        data = await self._api_call(
            ENDPOINT_DEVICE_CURRENT, {"deviceSn": self._device_sn}
        )
        return self._parse_data_list(data)

    async def get_battery_data(self) -> dict[str, str]:
        """Get current data from the battery device."""
        if not self._battery_sn:
            return {}
        data = await self._api_call(
            ENDPOINT_DEVICE_CURRENT, {"deviceSn": self._battery_sn}
        )
        return self._parse_data_list(data)

    async def get_collector_data(self) -> dict[str, str]:
        """Get current data from the collector/logger."""
        if not self._collector_sn:
            return {}
        data = await self._api_call(
            ENDPOINT_DEVICE_CURRENT, {"deviceSn": self._collector_sn}
        )
        return self._parse_data_list(data)

    async def get_station_realtime(self) -> dict[str, Any]:
        """Get station real-time overview data."""
        if not self._station_id:
            return {}
        data = await self._api_call(
            ENDPOINT_STATION_REALTIME, {"stationId": self._station_id}
        )
        # Station data is flat (not in dataList), filter out metadata keys
        result = {}
        skip_keys = {"requestId", "code", "msg", "success", "lastUpdateTime"}
        for key, value in data.items():
            if key not in skip_keys and value is not None:
                result[key] = value
        return result

    async def get_station_info(self) -> dict[str, Any]:
        """Get station base information."""
        if not self._station_id:
            return {}
        data = await self._api_call(
            ENDPOINT_STATION_BASE, {"stationId": self._station_id}
        )
        skip_keys = {"requestId", "code", "msg", "success"}
        return {k: v for k, v in data.items() if k not in skip_keys}

    @staticmethod
    def _parse_data_list(data: dict[str, Any]) -> dict[str, str]:
        """Parse the dataList from a device API response into a flat dict."""
        result = {}
        data_list = data.get("dataList", [])
        for item in data_list:
            key = item.get("key", "")
            value = item.get("value", "")
            if key:
                result[key] = value if value is not None else ""
        return result

    async def test_connection(self) -> bool:
        """Test if the API connection works."""
        try:
            await self._ensure_token()
            return True
        except SolarmanApiError:
            return False
