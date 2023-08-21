from .data_cache import DataCache

class MemoryCache(DataCache):
    def __init__(self):
        self.__cache = {}
    def set(self, key: any, value: any, timeout: int = 0) -> None:
        self.__cache[key] = value
    def get(self, key: any, default: any = None) -> any:
        return self.__cache.get(key, default)