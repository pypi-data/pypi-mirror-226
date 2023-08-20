from typing import Any, TypeVar

from functools import lru_cache

from .async_interface import AsyncHooksBackend
from .interface import HooksBackend

T = TypeVar("T")


@lru_cache(maxsize=None)
def python_object_backend_factory(wrapped_cls: type[T]) -> type[HooksBackend]:
    class PythonObjectHooksBackend(HooksBackend):
        @classmethod
        def load(cls, identifier: str) -> Any:
            return getattr(wrapped_cls, identifier)

        @classmethod
        def save(cls, identifier: str, value: Any) -> bool:
            setattr(wrapped_cls, identifier, value)
            return True

        @classmethod
        def exists(cls, identifier: str) -> bool:
            return hasattr(wrapped_cls, identifier)

    return PythonObjectHooksBackend


@lru_cache(maxsize=None)
def async_python_object_backend_factory(
    wrapped_cls: type[T],
) -> type[AsyncHooksBackend]:
    class AsyncPythonObjectHooksBackend(AsyncHooksBackend):
        @classmethod
        async def load(cls, identifier: str) -> Any:
            return getattr(wrapped_cls, identifier)

        @classmethod
        async def save(cls, identifier: str, value: Any) -> bool:
            setattr(wrapped_cls, identifier, value)
            return True

        @classmethod
        async def exists(cls, identifier: str) -> bool:
            return hasattr(wrapped_cls, identifier)

    return AsyncPythonObjectHooksBackend
