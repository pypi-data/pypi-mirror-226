from .const import BT_PREFIX as BT_PREFIX, CONF_REQUEST_RSSI as CONF_REQUEST_RSSI, DEFAULT_DEVICE_ID as DEFAULT_DEVICE_ID, DOMAIN as DOMAIN, SERVICE_UPDATE as SERVICE_UPDATE
from _typeshed import Incomplete
from homeassistant.components.device_tracker import CONF_SCAN_INTERVAL as CONF_SCAN_INTERVAL, CONF_TRACK_NEW as CONF_TRACK_NEW, DEFAULT_TRACK_NEW as DEFAULT_TRACK_NEW, SCAN_INTERVAL as SCAN_INTERVAL, SourceType as SourceType
from homeassistant.components.device_tracker.legacy import AsyncSeeCallback as AsyncSeeCallback, Device as Device, YAML_DEVICES as YAML_DEVICES, async_load_config as async_load_config
from homeassistant.const import CONF_DEVICE_ID as CONF_DEVICE_ID
from homeassistant.core import HomeAssistant as HomeAssistant, ServiceCall as ServiceCall
from homeassistant.helpers.event import async_track_time_interval as async_track_time_interval
from homeassistant.helpers.typing import ConfigType as ConfigType, DiscoveryInfoType as DiscoveryInfoType
from typing import Final

_LOGGER: Final[Incomplete]
PLATFORM_SCHEMA: Final[Incomplete]

def is_bluetooth_device(device: Device) -> bool: ...
def discover_devices(device_id: int) -> list[tuple[str, str]]: ...
async def see_device(hass: HomeAssistant, async_see: AsyncSeeCallback, mac: str, device_name: str, rssi: tuple[int] | None = ...) -> None: ...
async def get_tracking_devices(hass: HomeAssistant) -> tuple[set[str], set[str]]: ...
def lookup_name(mac: str) -> str | None: ...
async def async_setup_scanner(hass: HomeAssistant, config: ConfigType, async_see: AsyncSeeCallback, discovery_info: DiscoveryInfoType | None = ...) -> bool: ...
