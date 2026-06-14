from dataclasses import dataclass

@dataclass
class Config:
	accountId: str
	firm: str
	type: str
	server: str
	name: str
	description: str
	executablePath: str
	serverUrl: str
	baseSize: str
	tradeValue: str

