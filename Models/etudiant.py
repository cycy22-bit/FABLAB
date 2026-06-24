from dataclasses import dataclass
from datetime import date


@dataclass
class EtudiantDTO:
    id_etudiant: int | None
    nom_etudiant: str
    prenom_etudiant: str
    post_nom_etudiant: str
    adresse_mail_etudiant: str
    mots_de_passe: str
    telephone: str
    promotion_filiaire: str
    date_inscription: date
    statut_compte: str