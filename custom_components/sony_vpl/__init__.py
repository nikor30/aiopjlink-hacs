"""Sony VPL projector integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform

from .const import DOMAIN, DEFAULT_PORT


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up Sony VPL projector from YAML configuration."""
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    host = conf["host"]
    port = conf.get("port", DEFAULT_PORT)
    password = conf.get("password")

    hass.data[DOMAIN] = {"host": host, "port": port, "password": password}
    hass.async_create_task(async_load_platform(hass, "remote", DOMAIN, {}, config))
    return True
