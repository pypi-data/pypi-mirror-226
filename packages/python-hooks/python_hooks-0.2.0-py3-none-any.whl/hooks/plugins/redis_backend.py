from typing import Any, Union

from hooks.backends.async_interface import AsyncHooksBackend
from hooks.backends.interface import HooksBackend

try:
    # Extend pickle to support lambdas
    import dill as pickle
    import redis

    class RedisBackend(HooksBackend):
        redis_client = None

        @classmethod
        def use(cls, host: str, port: int, *args: Any, **kwargs: Any) -> Any:
            cls.redis_client = redis.Redis(host=host, port=port, **kwargs)
            super().use(**kwargs)
            return cls

        @classmethod
        def load(cls, identifier: str) -> Any:
            if cls.redis_client:
                return pickle.loads(cls.redis_client.get(identifier))
            else:
                raise Exception("Redis client not initialized")

        @classmethod
        def save(cls, identifier: str, value: Any) -> Union[bool, None, Any]:
            if cls.redis_client:
                return cls.redis_client.set(identifier, pickle.dumps(value))
            else:
                raise Exception("Redis client not initialized")

        @classmethod
        def exists(cls, identifier: str) -> bool:
            if cls.redis_client:
                return cls.redis_client.exists(identifier) == 1
            else:
                raise Exception("Redis client not initialized")

        @classmethod
        def reset_backend(cls):
            if cls.redis_client:
                for key in cls.redis_client.scan_iter("*"):
                    cls.redis_client.delete(key)

    import redis.asyncio as async_redis

    class AsyncRedisBackend(AsyncHooksBackend):
        redis_client = None

        @classmethod
        async def use(cls, host: str, port: int, *args: Any, **kwargs: Any) -> Any:
            cls.redis_client = async_redis.Redis(host=host, port=port, **kwargs)
            await super().use(**kwargs)
            return cls

        @classmethod
        async def load(cls, identifier: str) -> Any:
            if cls.redis_client:
                return pickle.loads(await cls.redis_client.get(identifier))
            else:
                raise Exception("Redis client not initialized")

        @classmethod
        async def save(cls, identifier: str, value: Any) -> Union[bool, None, Any]:
            if cls.redis_client:
                return await cls.redis_client.set(identifier, pickle.dumps(value))
            else:
                raise Exception("Redis client not initialized")

        @classmethod
        async def exists(cls, identifier: str) -> bool:
            if cls.redis_client:
                return await cls.redis_client.exists(identifier) == 1
            else:
                raise Exception("Redis client not initialized")

        @classmethod
        async def reset_backend(cls):
            if cls.redis_client:
                for key in await cls.redis_client.scan_iter("*"):
                    await cls.redis_client.delete(key)

except ImportError:
    raise ImportError("Redis backend requires redis to be installed")
