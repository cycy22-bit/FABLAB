from dataclasses import dataclass


@dataclass
class GestionnaireDTO:
    id_gestionnaire: int | None
    nom_gestionnaire: str
    email_gestionnaire: str
    telephone_gestionnaire: str
    mot_de_passe: str