from dataclasses import dataclass
from .backend import Backend
from .money import Money

@dataclass
class AccountConfig:
    id: str
    type: str
    description: str
    path: str
    backend: Backend
    money: Money