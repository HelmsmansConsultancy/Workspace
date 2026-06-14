from dataclasses import dataclass
from datetime import datetime

@dataclass
class Status:
	accountId: str
	balance: str
	lastAccess: datetime
	lastOrder: datetime
	lastPosition: datetime