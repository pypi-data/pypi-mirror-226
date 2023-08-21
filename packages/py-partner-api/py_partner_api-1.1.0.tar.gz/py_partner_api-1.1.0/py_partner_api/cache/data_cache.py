from abc import ABC, abstractclassmethod

class DataCache(ABC):
    @abstractclassmethod
    def set(self, key: any, value: any, timeout: int) -> None:
        pass
    @abstractclassmethod
    def get(self, key: any, default: any = None) -> any:
        pass