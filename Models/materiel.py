from dataclasses import dataclass


@dataclass
class MaterielDTO:
    id_materiel: int | None
    nom_materiel: str
    categorie: str
    quantite_stock: int
    stock_minimum: int