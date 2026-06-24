from dataclasses import dataclass
from datetime import date


@dataclass
class CommandeDTO:
    id_commande: int | None
    id_fournisseur: int
    id_gestionnaire: int
    date_commande: date
    date_livraison_prevue: date
    date_livraison_effective: date | None
    statut_commande: str
    montant_total: float