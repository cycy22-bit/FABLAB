from dataclasses import dataclass
from datetime import date


@dataclass
class AlerteDTO:
    id_alerte: int | None
    type_alerte: str
    message_alerte: str
    date_alerte: date