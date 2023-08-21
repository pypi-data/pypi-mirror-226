from .data_cache import DataCache

class RedisCache(DataCache):
    def __init__(self, redis):
        self.__redis = redis
    def set(self, key: any, value: any, timeout: int) -> None:
        self.__redis.set(key, value, timeout)
    def get(self, key: any, default: any = None) -> any:
        return self.__redis.get(key, default)