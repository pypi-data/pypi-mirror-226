import datetime as dt
import time
from _typeshed import Incomplete
from functools import partial
from typing import Any

DATE_STR_FORMAT: str
UTC: Incomplete
DEFAULT_TIME_ZONE: dt.tzinfo
CLOCK_MONOTONIC_COARSE: int
EPOCHORDINAL: Incomplete
DATETIME_RE: Incomplete
STANDARD_DURATION_RE: Incomplete
ISO8601_DURATION_RE: Incomplete
POSTGRES_INTERVAL_RE: Incomplete

def set_default_time_zone(time_zone: dt.tzinfo) -> None: ...
def get_time_zone(time_zone_str: str) -> dt.tzinfo | None: ...

utcnow: partial[dt.datetime]

def now(time_zone: dt.tzinfo | None = ...) -> dt.datetime: ...
def as_utc(dattim: dt.datetime) -> dt.datetime: ...
def as_timestamp(dt_value: dt.datetime | str) -> float: ...
def as_local(dattim: dt.datetime) -> dt.datetime: ...

utc_from_timestamp: Incomplete

def utc_to_timestamp(utc_dt: dt.datetime) -> float: ...
def start_of_local_day(dt_or_d: dt.date | dt.datetime | None = ...) -> dt.datetime: ...
def parse_datetime(dt_str: str) -> dt.datetime | None: ...
def parse_date(dt_str: str) -> dt.date | None: ...
def parse_duration(value: str) -> dt.timedelta | None: ...
def parse_time(time_str: str) -> dt.time | None: ...
def get_age(date: dt.datetime) -> str: ...
def parse_time_expression(parameter: Any, min_value: int, max_value: int) -> list[int]: ...
def _dst_offset_diff(dattim: dt.datetime) -> dt.timedelta: ...
def _lower_bound(arr: list[int], cmp: int) -> int | None: ...
def find_next_time_expression_time(now: dt.datetime, seconds: list[int], minutes: list[int], hours: list[int]) -> dt.datetime: ...
def _datetime_exists(dattim: dt.datetime) -> bool: ...
def _datetime_ambiguous(dattim: dt.datetime) -> bool: ...
def __gen_monotonic_time_coarse() -> partial[float]: ...
monotonic_time_coarse = time.monotonic
