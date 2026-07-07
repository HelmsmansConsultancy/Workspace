from dataclasses import dataclass


@dataclass
class MetatraderConfig:
    id: int = None
    path: str = None

    def __init__(self, id: int = None, path: str = None):
        self.id = id
        self.path = path