from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Order:
	entryPrice: Decimal
	stopLoss: Decimal
	takeProfit: Decimal
	amount: Decimal
	asset: str
