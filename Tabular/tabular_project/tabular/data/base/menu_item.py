from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class MenuItem:
    label: str
    command: Callable[[], bool]
    suffix: Optional[Callable[[], str]] = None
    enabled: bool = True   # or: Callable[[], bool] for dynamic state