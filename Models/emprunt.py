from dataclasses import dataclass
from datetime import date


@dataclass
class EmpruntDTO:
    id_emprunt: int | None
    id_etudiant: int
    id_materiel: int
    quantite_empruntee: int
    date_emprunt: date
    date_retour_prevue: date
    date_retour_effective: date | None
    statut_emprunt: str
    etat_retour: str