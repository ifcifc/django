from typing import Callable
from django.core.cache import cache


class TTLCache:
    def __init__(self, ttl=10, prefix=""):
        self.ttl = ttl
        self.prefix = prefix

    def remove(self, key):
        cache.delete(f"{self.prefix}:{key}")

    def get_or_default(self, key, default:Callable):
        _key = f"{self.prefix}:{key}"
        if cache.has_key(_key):
            return cache.get(_key)
        
        value = default()
        cache.set(_key, value, self.ttl)
        return value


