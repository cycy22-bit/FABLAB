from dataclasses import dataclass


@dataclass
class LigneCommandeDTO:
    id_ligne: int | None
    id_commande: int
    id_materiel: int
    quantite_commandee: int
    prix_unitaire: float
    prix_total: float