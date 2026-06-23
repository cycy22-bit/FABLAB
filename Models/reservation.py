from dataclasses import dataclass
from datetime import date, time


@dataclass
class ReservationDTO:
    id_reservation: int | None
    id_etudiant: int
    id_machine: int
    date_reservation: date
    heure_debut: time
    heure_fin: time
    statut_reservation: str