from tabular.service.s import S

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

    def put(self, key, value):
        self.dict[key] = value

    def get(self, key):
        return self.dict.get(key, None)  
