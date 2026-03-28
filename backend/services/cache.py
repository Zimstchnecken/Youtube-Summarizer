"""
In-memory cache with TTL support.
For production, replace with Redis.
"""

import time
from typing import Any, Optional
from config import CACHE_TTL


class InMemoryCache:
    """Simple in-memory cache with TTL expiration."""
    
    def __init__(self, ttl: int = CACHE_TTL):
        self._store: dict[str, dict[str, Any]] = {}
        self._ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache. Returns None if expired or missing."""
        if key not in self._store:
            return None
        
        entry = self._store[key]
        if time.time() - entry["timestamp"] > self._ttl:
            # Expired — remove and return None
            del self._store[key]
            return None
        
        return entry["data"]
    
    def set(self, key: str, data: Any) -> None:
        """Store a value in cache with current timestamp."""
        self._store[key] = {
            "data": data,
            "timestamp": time.time(),
        }
    
    def exists(self, key: str) -> bool:
        """Check if a non-expired key exists in cache."""
        return self.get(key) is not None
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self._store.clear()


# Singleton cache instance
cache = InMemoryCache()
