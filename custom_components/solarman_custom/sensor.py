"""Sensor platform for Solarman Custom integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ALL_SENSORS,
    CONF_DEVICE_SN,
    DOMAIN,
    SolarmanSensorDescription,
)
from .coordinator import SolarmanCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solarman sensors from a config entry."""
    coordinator: SolarmanCoordinator = hass.data[DOMAIN][entry.entry_id]
    device_sn = entry.data[CONF_DEVICE_SN]

    entities: list[SolarmanSensor] = []

    for description in ALL_SENSORS:
        entities.append(
            SolarmanSensor(
                coordinator=coordinator,
                description=description,
                device_sn=device_sn,
            )
        )

    async_add_entities(entities)
    _LOGGER.info("Added %d Solarman sensors", len(entities))


class SolarmanSensor(CoordinatorEntity[SolarmanCoordinator], SensorEntity):
    """Representation of a Solarman sensor."""

    entity_description: SolarmanSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SolarmanCoordinator,
        description: SolarmanSensorDescription,
        device_sn: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_sn = device_sn
        self._source = description.source
        self._api_key = description.api_key

        # Unique ID: domain_devicesn_sensorkey
        self._attr_unique_id = f"{DOMAIN}_{device_sn}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info to group sensors by device."""
        station_info = self.coordinator.station_info

        if self._source == "inverter":
            return DeviceInfo(
                identifiers={(DOMAIN, self._device_sn)},
                name=f"Inverter {station_info.get('name', self._device_sn)}",
                manufacturer="Deye",
                model="HYD 5KTL-3PH",
                serial_number=self._device_sn,
                sw_version=self._get_inverter_value("FWv1"),
            )
        elif self._source == "battery":
            battery_sn = self.coordinator.api.battery_sn or "battery"
            return DeviceInfo(
                identifiers={(DOMAIN, f"{self._device_sn}_battery")},
                name=f"Battery {station_info.get('name', '')}".strip(),
                manufacturer="Deye",
                model="BTS 5K",
                serial_number=battery_sn,
                via_device=(DOMAIN, self._device_sn),
            )
        elif self._source == "collector":
            collector_sn = self.coordinator.api.collector_sn or "collector"
            return DeviceInfo(
                identifiers={(DOMAIN, f"{self._device_sn}_collector")},
                name=f"Collector {station_info.get('name', '')}".strip(),
                manufacturer="Solarman",
                model="WiFi Logger",
                serial_number=collector_sn,
                via_device=(DOMAIN, self._device_sn),
            )
        else:  # station
            return DeviceInfo(
                identifiers={(DOMAIN, f"{self._device_sn}_station")},
                name=f"Station {station_info.get('name', '')}".strip(),
                manufacturer="Solarman",
                model="Power Station",
                via_device=(DOMAIN, self._device_sn),
            )

    @property
    def native_value(self) -> str | float | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None

        source_data = self.coordinator.data.get(self._source, {})

        if not source_data:
            return None

        raw_value = source_data.get(self._api_key)

        if raw_value is None or raw_value == "":
            return None

        # Try to convert to float for numeric sensors
        if self.entity_description.device_class is not None or self.entity_description.state_class is not None:
            try:
                return float(raw_value)
            except (ValueError, TypeError):
                # Some values like "Grid connected" are strings
                return raw_value

        return raw_value

    @property
    def available(self) -> bool:
        """Return True if the sensor data source has data."""
        if not super().available:
            return False
        if self.coordinator.data is None:
            return False
        source_data = self.coordinator.data.get(self._source, {})
        # Sensor is available if the source has data (even if this specific key is missing)
        return bool(source_data)

    def _get_inverter_value(self, key: str) -> str | None:
        """Get a value from inverter data (for device info)."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("inverter", {}).get(key)
