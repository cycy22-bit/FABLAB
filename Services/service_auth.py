import re

from Repositories.sqlite.sqlite_gestionnaire_repository import SQLiteGestionnaireRepository
from Repositories.sqlite.sqlite_etudiant_repository import SQLiteEtudiantRepository


class AuthService:
    def __init__(self):
        self.gestionnaire_repo = SQLiteGestionnaireRepository()
        self.etudiant_repo = SQLiteEtudiantRepository()

    def se_connecter(self, email: str, password: str):
        email = email.strip().lower()
        password = password.strip()

        if not email or not password:
            return None

        # 1. Chercher d'abord dans les gestionnaires
        gestionnaire = self.gestionnaire_repo.find_by_email(email)

        if gestionnaire:
            return {
                "id": gestionnaire.id_gestionnaire,
                "nom": gestionnaire.nom_gestionnaire,
                "role": "GESTIONNAIRE",
                "email": email,
            }

        # 2. Chercher ensuite dans les étudiants
        etudiant = self.etudiant_repo.find_by_email(email)

        if etudiant:
            return {
                "id": etudiant.id_etudiant,
                "nom": etudiant.nom_etudiant,
                "role": "ETUDIANT",
                "email": email,
            }

        # 3. Sécurité temporaire si la base n'est pas encore bien remplie
        if re.match(r"^[a-z]+\.[a-z]+@ulc-icam\.com$", email):
            return {
                "id": 1,
                "nom": "Gestionnaire",
                "role": "GESTIONNAIRE",
                "email": email,
            }

        if re.match(r"^[a-z]+\.[a-z]+@[0-9]{4}\.ulc-icam\.com$", email):
            return {
                "id": 1,
                "nom": "Etudiant",
                "role": "ETUDIANT",
                "email": email,
            }

        return None