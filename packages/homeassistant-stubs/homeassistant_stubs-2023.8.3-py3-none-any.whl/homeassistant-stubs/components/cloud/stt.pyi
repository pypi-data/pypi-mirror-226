from .client import CloudClient as CloudClient
from .const import DOMAIN as DOMAIN
from _typeshed import Incomplete
from collections.abc import AsyncIterable
from hass_nabucasa import Cloud as Cloud
from homeassistant.components.stt import AudioBitRates as AudioBitRates, AudioChannels as AudioChannels, AudioCodecs as AudioCodecs, AudioFormats as AudioFormats, AudioSampleRates as AudioSampleRates, Provider as Provider, SpeechMetadata as SpeechMetadata, SpeechResult as SpeechResult, SpeechResultState as SpeechResultState
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.typing import ConfigType as ConfigType, DiscoveryInfoType as DiscoveryInfoType

_LOGGER: Incomplete

async def async_get_engine(hass: HomeAssistant, config: ConfigType, discovery_info: DiscoveryInfoType | None = ...) -> CloudProvider: ...

class CloudProvider(Provider):
    cloud: Incomplete
    def __init__(self, cloud: Cloud[CloudClient]) -> None: ...
    @property
    def supported_languages(self) -> list[str]: ...
    @property
    def supported_formats(self) -> list[AudioFormats]: ...
    @property
    def supported_codecs(self) -> list[AudioCodecs]: ...
    @property
    def supported_bit_rates(self) -> list[AudioBitRates]: ...
    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]: ...
    @property
    def supported_channels(self) -> list[AudioChannels]: ...
    async def async_process_audio_stream(self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]) -> SpeechResult: ...
