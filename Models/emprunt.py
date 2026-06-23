from dataclasses import dataclass
from datetime import date


@dataclass
class EmpruntDTO:
    id_emprunt: int | None
    id_etudiant: int
    id_materiel: int
    quantite: int
    date_emprunt: date
    date_retour_prevue: date
    statut_emprunt: str