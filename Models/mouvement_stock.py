from dataclasses import dataclass
from datetime import date


@dataclass
class MouvementStockDTO:
    id_mouvement: int | None
    id_materiel: int
    type_mouvement: str
    quantite: int
    date_mouvement: date