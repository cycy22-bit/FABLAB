from dataclasses import dataclass


@dataclass
class FournisseurDTO:
    id_fournisseur: int | None
    nom_fournisseur: str
    adresse: str
    telephone: str
    email: str
    site_web: str | None