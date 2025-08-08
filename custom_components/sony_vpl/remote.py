"""Remote control for Sony VPL projectors via PJLink."""
from __future__ import annotations

from homeassistant.components.remote import RemoteEntity

from aiopjlink import PJLink, Sources

from .const import DOMAIN, DEFAULT_NAME


COMMAND_MAP = {
    "power_on": lambda link: link.power.turn_on(),
    "power_off": lambda link: link.power.turn_off(),
    "input_hdmi1": lambda link: link.sources.set(Sources.Mode.DIGITAL, 1),
    "input_hdmi2": lambda link: link.sources.set(Sources.Mode.DIGITAL, 2),
    "shutter_open": lambda link: link.shutter.open(),
    "shutter_close": lambda link: link.shutter.close(),
    "mute_audio": lambda link: link.audio_mute.on(),
    "unmute_audio": lambda link: link.audio_mute.off(),
    "mute_video": lambda link: link.video_mute.on(),
    "unmute_video": lambda link: link.video_mute.off(),
    "freeze_on": lambda link: link.freeze.on(),
    "freeze_off": lambda link: link.freeze.off(),
}


class SonyVPLRemote(RemoteEntity):
    """Representation of a Sony VPL projector as a remote."""

    def __init__(self, hass):
        """Initialize the remote."""
        data = hass.data[DOMAIN]
        self._host = data["host"]
        self._port = data["port"]
        self._password = data["password"]
        self._name = DEFAULT_NAME
        self._is_on = False

    async def async_turn_on(self, **kwargs):
        """Turn the projector on."""
        await self._dispatch("power_on")
        self._is_on = True

    async def async_turn_off(self, **kwargs):
        """Turn the projector off."""
        await self._dispatch("power_off")
        self._is_on = False

    async def async_send_command(self, command, **kwargs):
        """Send a list of commands to the projector."""
        for single in command:
            await self._dispatch(single)

    async def _dispatch(self, key):
        func = COMMAND_MAP.get(key)
        if func is None:
            raise ValueError(f"Unknown command: {key}")
        async with PJLink(address=self._host, port=self._port, password=self._password) as link:
            await func(link)

    @property
    def name(self):
        """Return the name of the remote."""
        return self._name

    @property
    def should_poll(self):
        return False

    @property
    def is_on(self):
        return self._is_on


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Sony VPL remote platform."""
    async_add_entities([SonyVPLRemote(hass)])
