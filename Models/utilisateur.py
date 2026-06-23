from dataclasses import dataclass


@dataclass
class UtilisateurDTO:
    id_etudiant: int | None
    nom: str
    prenom: str
    email: str
    telephone: str
    promotion: str
    statut_compte: str