"""Config flow for Solarman Custom integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SolarmanApi, SolarmanApiError, SolarmanAuthError
from .const import CONF_APP_ID, CONF_APP_SECRET, CONF_DEVICE_SN, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_APP_ID): str,
        vol.Required(CONF_APP_SECRET): str,
        vol.Required(CONF_DEVICE_SN): str,
    }
)


class SolarmanCustomConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solarman Custom."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Check if already configured with this device SN
            await self.async_set_unique_id(user_input[CONF_DEVICE_SN])
            self._abort_if_unique_id_configured()

            # Validate credentials
            session = async_get_clientsession(self.hass)
            api = SolarmanApi(
                session=session,
                email=user_input[CONF_EMAIL],
                password=user_input[CONF_PASSWORD],
                app_id=user_input[CONF_APP_ID],
                app_secret=user_input[CONF_APP_SECRET],
                device_sn=user_input[CONF_DEVICE_SN],
            )

            try:
                success = await api.test_connection()
                if not success:
                    errors["base"] = "auth_failed"
                else:
                    # Try to discover station
                    await api.discover_station()

            except SolarmanAuthError as err:
                _LOGGER.error("Solarman auth error: %s", err)
                errors["base"] = "auth_failed"
            except SolarmanApiError as err:
                _LOGGER.error("Solarman API error: %s", err)
                errors["base"] = "connection_error"
            except Exception as err:
                _LOGGER.exception("Unexpected error during config flow: %s", err)
                errors["base"] = "unknown"

            if not errors:
                return self.async_create_entry(
                    title=f"Solarman ({user_input[CONF_DEVICE_SN]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
