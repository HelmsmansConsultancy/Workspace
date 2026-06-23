from dataclasses import dataclass
import decimal


@dataclass
class Money:
    base: decimal
    currency: str
    risk: decimal