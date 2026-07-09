from tabular.service.s import S
from typing import TypeVar

class SingletonMeta(type):
    """
    Metaclass for creating Singleton classes.
    Ensures only one instance exists.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # If instance doesn't exist, create it
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonService(metaclass=SingletonMeta):
    def __init__(self):
        self.dict = {}

    def put(self, key, value) -> None:
        self.dict[key] = [value, None]

    # def put(self, key, value, clazz) -> None:
    #     if bool(clazz) and isinstance(clazz, type):
    #         self.dict[key] = [value, clazz]
    #     else:
    #         raise TypeError(f"{clazz!r} is not a class")

    def get(self, key) -> any:
        result = self.dict.get(key)
        if bool(result):
            return result[0]
        else:
            return None

    # def get(self, key, clazz) -> any:
    #     [value, clazz] = self.dict.get(key)
    #     if bool(clazz):
    #         if isinstance(clazz, type):
    #             typeVar = TypeVar(clazz)
    #             if isinstance(value, clazz):
    #                 return value
    #             else:
    #                 raise TypeError(f"{value!r} is not of class {clazz!r}")
    #         else:
    #             raise TypeError(f"{clazz!r} is not a class")
    #     else:
    #         return value
