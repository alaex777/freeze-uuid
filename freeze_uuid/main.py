import uuid
import functools
from typing import Any, Callable, Union
from inspect import iscoroutinefunction

DEFAULT_VALUE = '00000000-0000-0000-0000-000000000000'

VALUES = [DEFAULT_VALUE]
COUNT = 0


class FakeUUID:
    def __init__(self, *args, **kwargs) -> None:
        global COUNT
        self.value = VALUES[COUNT] if COUNT < len(VALUES) else VALUES[-1]
        self.int = int(self.value.replace('-', ''), 16)
        COUNT += 1

    def __str__(self) -> str:
        return self.value

    def __eq__(self, __value: object) -> bool:
        return str(__value) == self.value

    def __lt__(self, other: object) -> bool:
        if isinstance(other, FakeUUID):
            return self.int < other.int
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, FakeUUID):
            return self.int > other.int
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, FakeUUID):
            return self.int <= other.int
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, FakeUUID):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))
    
    @property
    def bytes(self):
        return self.int.to_bytes(16)  # big endian

    @property
    def bytes_le(self):
        bytes = self.bytes
        return (bytes[4-1::-1] + bytes[6-1:4-1:-1] + bytes[8-1:6-1:-1] +
                bytes[8:])

    @property
    def fields(self):
        return (self.time_low, self.time_mid, self.time_hi_version,
                self.clock_seq_hi_variant, self.clock_seq_low, self.node)

    @property
    def time_low(self):
        return self.int >> 96

    @property
    def time_mid(self):
        return (self.int >> 80) & 0xffff

    @property
    def time_hi_version(self):
        return (self.int >> 64) & 0xffff

    @property
    def clock_seq_hi_variant(self):
        return (self.int >> 56) & 0xff

    @property
    def clock_seq_low(self):
        return (self.int >> 48) & 0xff

    @property
    def time(self):
        return (((self.time_hi_version & 0x0fff) << 48) |
                (self.time_mid << 32) | self.time_low)

    @property
    def clock_seq(self):
        return (((self.clock_seq_hi_variant & 0x3f) << 8) |
                self.clock_seq_low)

    @property
    def node(self):
        return self.int & 0xffffffffffff

    @property
    def hex(self):
        return '%032x' % self.int

    @property
    def urn(self):
        return 'urn:uuid:' + str(self)

    @property
    def variant(self):
        if not self.int & (0x8000 << 48):
            return uuid.RESERVED_NCS
        elif not self.int & (0x4000 << 48):
            return uuid.RFC_4122
        elif not self.int & (0x2000 << 48):
            return uuid.RESERVED_MICROSOFT
        else:
            return uuid.RESERVED_FUTURE

    @property
    def version(self):
        # The version bits are only meaningful for RFC 4122 UUIDs.
        if self.variant == uuid.RFC_4122:
            return int((self.int >> 76) & 0xf)


def freeze_uuid(values: Union[str, list] = DEFAULT_VALUE) -> Callable:
    def inner(func: Callable) -> Callable:
        def value_magic():
            global VALUES
            if isinstance(values, str):
                VALUES = [values]
            else:
                VALUES = values

            global COUNT
            COUNT = 0

            for value in VALUES:
                uuid.UUID(value)

        def wrapper(*args: Any, **kwargs: Any) -> None:
            value_magic()
            prev_uuid = uuid.UUID
            uuid.UUID = FakeUUID

            func_result = func(*args, **kwargs)

            uuid.UUID = prev_uuid
            return func_result

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> None:
            value_magic()
            prev_uuid = uuid.UUID
            uuid.UUID = FakeUUID

            func_result = await func(*args, **kwargs)

            uuid.UUID = prev_uuid
            return func_result

        if iscoroutinefunction(func):
            return async_wrapper

        return wrapper
    return inner
