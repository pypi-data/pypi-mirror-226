from .const import DOMAIN as DOMAIN, LOGGER as LOGGER
from collections.abc import Mapping
from homeassistant.components import onboarding as onboarding, zeroconf as zeroconf
from homeassistant.config_entries import ConfigFlow as ConfigFlow, SOURCE_ZEROCONF as SOURCE_ZEROCONF
from homeassistant.const import CONF_ACCESS_TOKEN as CONF_ACCESS_TOKEN, CONF_DEVICE as CONF_DEVICE, CONF_HOST as CONF_HOST
from homeassistant.core import callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from python_awair import AwairLocalDevice as AwairLocalDevice
from python_awair.user import AwairUser as AwairUser
from typing import Any

class AwairFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION: int
    _device: AwairLocalDevice
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> FlowResult: ...
    async def async_step_discovery_confirm(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_user(self, user_input: dict[str, str] | None = ...) -> FlowResult: ...
    async def async_step_cloud(self, user_input: Mapping[str, Any]) -> FlowResult: ...
    def _get_discovered_entries(self) -> dict[str, str]: ...
    async def async_step_local(self, user_input: Mapping[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_local_pick(self, user_input: Mapping[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult: ...
    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def _check_local_connection(self, device_address: str) -> tuple[AwairLocalDevice | None, str | None]: ...
    async def _check_cloud_connection(self, access_token: str) -> tuple[AwairUser | None, str | None]: ...
