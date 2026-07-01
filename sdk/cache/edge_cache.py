#!/usr/bin/env python3
"""Edge Cache — 10-100x faster resolution for ENS, beam weights. LRU + TTL."""
import time, hashlib
from collections import OrderedDict
from typing import Dict, Optional, Any

class EdgeCache:
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.store: OrderedDict = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl

    def _key(self, raw: str) -> str:
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def get(self, key: str) -> Optional[Any]:
        k = self._key(key)
        if k not in self.store:
            return None
        val, ts = self.store[k]
        if time.time() - ts > self.ttl:
            del self.store[k]
            return None
        self.store.move_to_end(k)
        return val

    def set(self, key: str, value: Any):
        k = self._key(key)
        if len(self.store) >= self.max_size:
            self.store.popitem(last=False)
        self.store[k] = (value, time.time())

    def clear(self): self.store.clear()

cache = EdgeCache()
