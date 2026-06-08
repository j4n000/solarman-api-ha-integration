"""Data update coordinator for Solarman Custom."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SolarmanApi, SolarmanApiError, SolarmanAuthError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class SolarmanCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage fetching Solarman data."""

    def __init__(self, hass: HomeAssistant, api: SolarmanApi) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self._station_info: dict[str, Any] = {}
        self._discovered = False

    @property
    def station_info(self) -> dict[str, Any]:
        """Return cached station info."""
        return self._station_info

    async def _async_setup(self) -> None:
        """Discover station and devices on first run."""
        if self._discovered:
            return

        try:
            discovery = await self.api.discover_station()
            self._station_info = discovery.get("station_detail", {})
            self._discovered = True
            _LOGGER.info(
                "Solarman setup complete: station=%s, battery=%s, collector=%s",
                self.api.station_id,
                self.api.battery_sn,
                self.api.collector_sn,
            )
        except SolarmanApiError as err:
            raise UpdateFailed(f"Failed to discover station: {err}") from err

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from all devices."""
        # Ensure discovery has run
        await self._async_setup()

        try:
            # Fetch all data sources in sequence to avoid rate limits
            inverter_data = await self.api.get_inverter_data()
            battery_data = await self.api.get_battery_data()
            collector_data = await self.api.get_collector_data()
            station_data = await self.api.get_station_realtime()

            result = {
                "inverter": inverter_data,
                "battery": battery_data,
                "collector": collector_data,
                "station": station_data,
            }

            _LOGGER.debug(
                "Data updated: inverter=%d points, battery=%d points, "
                "collector=%d points, station=%d points",
                len(inverter_data),
                len(battery_data),
                len(collector_data),
                len(station_data),
            )

            return result

        except SolarmanAuthError as err:
            raise UpdateFailed(f"Authentication error: {err}") from err
        except SolarmanApiError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
