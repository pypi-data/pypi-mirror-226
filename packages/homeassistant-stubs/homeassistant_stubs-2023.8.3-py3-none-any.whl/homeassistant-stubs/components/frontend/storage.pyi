from collections.abc import Callable as Callable
from homeassistant.components import websocket_api as websocket_api
from homeassistant.components.websocket_api.connection import ActiveConnection as ActiveConnection
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.storage import Store as Store
from typing import Any

DATA_STORAGE: str
STORAGE_VERSION_USER_DATA: int

def _initialize_frontend_storage(hass: HomeAssistant) -> None: ...
async def async_setup_frontend_storage(hass: HomeAssistant) -> None: ...
async def async_user_store(hass: HomeAssistant, user_id: str) -> tuple[Store, dict[str, Any]]: ...
def with_store(orig_func: Callable) -> Callable: ...
async def websocket_set_user_data(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any], store: Store, data: dict[str, Any]) -> None: ...
async def websocket_get_user_data(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any], store: Store, data: dict[str, Any]) -> None: ...
