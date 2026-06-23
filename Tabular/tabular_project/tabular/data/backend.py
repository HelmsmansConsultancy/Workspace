from dataclasses import dataclass

@dataclass
class Backend:
    firm: str
    server: str
    urlToServer: str