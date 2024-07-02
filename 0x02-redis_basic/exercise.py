#!/usr/bin/env python3
"""
redis db module
"""

import redis
from uuid import uuid4
from typing import Union, Optional, Callable


class Cache:
    def __init__(self):
        """
        store an instance of redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key (using uuid)
        Takes data as an argument and returns a string
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        takes a key string a argument and optional Callable argument named fn.
        This callable will be used to convert the data back to the desired
        format.
        """
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        parametrize Cache.get with the correct conversion function
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        parametrize Cache.get with the correct conversion function
        """
        data = self._redis.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0
        return data
