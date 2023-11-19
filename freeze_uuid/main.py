import uuid
import functools
from typing import Any, Callable
from inspect import iscoroutinefunction

DEFAULT_VALUE = '00000000-0000-0000-0000-000000000000'

VALUE = DEFAULT_VALUE


class FakeUUID:
    def __init__(self, *args, **kwargs) -> None:
        self.value = VALUE

    def __str__(self) -> str:
        return self.value

    def __eq__(self, __value: object) -> bool:
        return str(__value) == self.value


def freeze_uuid(value: str = DEFAULT_VALUE) -> Callable:
    def inner(func: Callable) -> Callable:
        def value_magic():
            global VALUE
            VALUE = value

            uuid.UUID(value)

        def wrapper(*args: Any, **kwargs: Any) -> None:
            value_magic()
            prev_uuid = uuid.UUID
            uuid.UUID = FakeUUID

            func(*args, **kwargs)

            uuid.UUID = prev_uuid

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> None:
            value_magic()
            prev_uuid = uuid.UUID
            uuid.UUID = FakeUUID

            await func(*args, **kwargs)

            uuid.UUID = prev_uuid

        if iscoroutinefunction(func):
            return async_wrapper

        return wrapper
    return inner
