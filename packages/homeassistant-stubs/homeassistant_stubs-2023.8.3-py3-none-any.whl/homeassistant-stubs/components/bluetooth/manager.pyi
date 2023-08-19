from .advertisement_tracker import AdvertisementTracker as AdvertisementTracker, TRACKER_BUFFERING_WOBBLE_SECONDS as TRACKER_BUFFERING_WOBBLE_SECONDS
from .base_scanner import BaseHaScanner as BaseHaScanner, BluetoothScannerDevice as BluetoothScannerDevice
from .const import FALLBACK_MAXIMUM_STALE_ADVERTISEMENT_SECONDS as FALLBACK_MAXIMUM_STALE_ADVERTISEMENT_SECONDS, UNAVAILABLE_TRACK_SECONDS as UNAVAILABLE_TRACK_SECONDS
from .match import ADDRESS as ADDRESS, BluetoothCallbackMatcher as BluetoothCallbackMatcher, BluetoothCallbackMatcherIndex as BluetoothCallbackMatcherIndex, BluetoothCallbackMatcherWithCallback as BluetoothCallbackMatcherWithCallback, CALLBACK as CALLBACK, CONNECTABLE as CONNECTABLE, IntegrationMatcher as IntegrationMatcher, ble_device_matches as ble_device_matches
from .models import BluetoothCallback as BluetoothCallback, BluetoothChange as BluetoothChange, BluetoothServiceInfoBleak as BluetoothServiceInfoBleak
from .storage import BluetoothStorage as BluetoothStorage
from .usage import install_multiple_bleak_catcher as install_multiple_bleak_catcher, uninstall_multiple_bleak_catcher as uninstall_multiple_bleak_catcher
from .util import async_load_history_from_system as async_load_history_from_system
from _typeshed import Incomplete
from bleak.backends.device import BLEDevice as BLEDevice
from bleak.backends.scanner import AdvertisementData as AdvertisementData, AdvertisementDataCallback as AdvertisementDataCallback
from bleak_retry_connector import BleakSlotManager as BleakSlotManager
from bluetooth_adapters import AdapterDetails as AdapterDetails, BluetoothAdapters as BluetoothAdapters
from collections.abc import Callable as Callable, Iterable
from datetime import datetime
from homeassistant import config_entries as config_entries
from homeassistant.components.logger import EVENT_LOGGING_CHANGED as EVENT_LOGGING_CHANGED
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, Event as Event, HomeAssistant as HomeAssistant
from homeassistant.helpers import discovery_flow as discovery_flow
from homeassistant.helpers.event import async_track_time_interval as async_track_time_interval
from homeassistant.util.dt import monotonic_time_coarse as monotonic_time_coarse
from typing import Any, Final

FILTER_UUIDS: Final[str]
APPLE_MFR_ID: Final[int]
APPLE_IBEACON_START_BYTE: Final[int]
APPLE_HOMEKIT_START_BYTE: Final[int]
APPLE_DEVICE_ID_START_BYTE: Final[int]
APPLE_HOMEKIT_NOTIFY_START_BYTE: Final[int]
APPLE_START_BYTES_WANTED: Final[Incomplete]
MONOTONIC_TIME: Final[Incomplete]
_LOGGER: Incomplete

def _dispatch_bleak_callback(callback: AdvertisementDataCallback | None, filters: dict[str, set[str]], device: BLEDevice, advertisement_data: AdvertisementData) -> None: ...

class BluetoothManager:
    __slots__: Incomplete
    hass: Incomplete
    _integration_matcher: Incomplete
    _cancel_unavailable_tracking: Incomplete
    _cancel_logging_listener: Incomplete
    _advertisement_tracker: Incomplete
    _unavailable_callbacks: Incomplete
    _connectable_unavailable_callbacks: Incomplete
    _callback_index: Incomplete
    _bleak_callbacks: Incomplete
    _all_history: Incomplete
    _connectable_history: Incomplete
    _non_connectable_scanners: Incomplete
    _connectable_scanners: Incomplete
    _adapters: Incomplete
    _sources: Incomplete
    _bluetooth_adapters: Incomplete
    storage: Incomplete
    slot_manager: Incomplete
    _debug: Incomplete
    def __init__(self, hass: HomeAssistant, integration_matcher: IntegrationMatcher, bluetooth_adapters: BluetoothAdapters, storage: BluetoothStorage, slot_manager: BleakSlotManager) -> None: ...
    @property
    def supports_passive_scan(self) -> bool: ...
    def async_scanner_count(self, connectable: bool = ...) -> int: ...
    async def async_diagnostics(self) -> dict[str, Any]: ...
    def _find_adapter_by_address(self, address: str) -> str | None: ...
    def async_scanner_by_source(self, source: str) -> BaseHaScanner | None: ...
    async def async_get_bluetooth_adapters(self, cached: bool = ...) -> dict[str, AdapterDetails]: ...
    async def async_get_adapter_from_address(self, address: str) -> str | None: ...
    def _async_logging_changed(self, event: Event) -> None: ...
    async def async_setup(self) -> None: ...
    def async_stop(self, event: Event) -> None: ...
    def async_scanner_devices_by_address(self, address: str, connectable: bool) -> list[BluetoothScannerDevice]: ...
    def _async_all_discovered_addresses(self, connectable: bool) -> Iterable[str]: ...
    def async_discovered_devices(self, connectable: bool) -> list[BLEDevice]: ...
    def async_setup_unavailable_tracking(self) -> None: ...
    def _async_check_unavailable(self, now: datetime) -> None: ...
    def _async_dismiss_discoveries(self, address: str) -> None: ...
    def _prefer_previous_adv_from_different_source(self, old: BluetoothServiceInfoBleak, new: BluetoothServiceInfoBleak) -> bool: ...
    def scanner_adv_received(self, service_info: BluetoothServiceInfoBleak) -> None: ...
    def _async_describe_source(self, service_info: BluetoothServiceInfoBleak) -> str: ...
    def async_track_unavailable(self, callback: Callable[[BluetoothServiceInfoBleak], None], address: str, connectable: bool) -> Callable[[], None]: ...
    def async_register_callback(self, callback: BluetoothCallback, matcher: BluetoothCallbackMatcher | None) -> Callable[[], None]: ...
    def async_ble_device_from_address(self, address: str, connectable: bool) -> BLEDevice | None: ...
    def async_address_present(self, address: str, connectable: bool) -> bool: ...
    def async_discovered_service_info(self, connectable: bool) -> Iterable[BluetoothServiceInfoBleak]: ...
    def async_last_service_info(self, address: str, connectable: bool) -> BluetoothServiceInfoBleak | None: ...
    def _async_trigger_matching_discovery(self, service_info: BluetoothServiceInfoBleak) -> None: ...
    def async_rediscover_address(self, address: str) -> None: ...
    def async_register_scanner(self, scanner: BaseHaScanner, connectable: bool, connection_slots: int | None = ...) -> CALLBACK_TYPE: ...
    def async_register_bleak_callback(self, callback: AdvertisementDataCallback, filters: dict[str, set[str]]) -> CALLBACK_TYPE: ...
    def async_release_connection_slot(self, device: BLEDevice) -> None: ...
    def async_allocate_connection_slot(self, device: BLEDevice) -> bool: ...
