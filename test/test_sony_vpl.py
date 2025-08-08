import types
import sys
import unittest
from unittest.mock import AsyncMock, patch

# Create minimal homeassistant stubs
ha = types.ModuleType("homeassistant")
components = types.ModuleType("components")
remote_mod = types.ModuleType("remote")
core_mod = types.ModuleType("core")
helpers_mod = types.ModuleType("helpers")
discovery_mod = types.ModuleType("discovery")

class RemoteEntity:
    pass

async def async_load_platform(hass, platform, domain, info, config):
    return None

remote_mod.RemoteEntity = RemoteEntity
components.remote = remote_mod
helpers_mod.discovery = discovery_mod
discovery_mod.async_load_platform = async_load_platform
class HomeAssistant:
    def async_create_task(self, coro):
        return coro
core_mod.HomeAssistant = HomeAssistant
ha.components = components
ha.core = core_mod
ha.helpers = helpers_mod
sys.modules["homeassistant"] = ha
sys.modules["homeassistant.components"] = components
sys.modules["homeassistant.components.remote"] = remote_mod
sys.modules["homeassistant.core"] = core_mod
sys.modules["homeassistant.helpers"] = helpers_mod
sys.modules["homeassistant.helpers.discovery"] = discovery_mod

from custom_components.sony_vpl.remote import SonyVPLRemote


class TestSonyVPLRemote(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        hass_obj = types.SimpleNamespace()
        hass_obj.data = {"sony_vpl": {"host": "127.0.0.1", "port": 4352, "password": None}}
        self.hass = hass_obj

    async def test_turn_on_invokes_library(self):
        remote = SonyVPLRemote(self.hass)
        with patch("custom_components.sony_vpl.remote.PJLink") as pjlink_cls:
            link = AsyncMock()
            pjlink_cls.return_value.__aenter__.return_value = link
            await remote.async_turn_on()
            link.power.turn_on.assert_awaited()

    async def test_unknown_command_raises(self):
        remote = SonyVPLRemote(self.hass)
        with self.assertRaises(ValueError):
            await remote.async_send_command(["badcommand"])
