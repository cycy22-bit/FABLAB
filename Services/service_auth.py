import re


class AuthService:
    def se_connecter(self, email: str, password: str):
        email = email.strip().lower()
        password = password.strip()

        if not email or not password:
            return None

        if password != "1234":
            return None

        if re.match(r"^[a-z]+(\.[a-z]+)*@[0-9]{4}\.ulc-icam\.com$", email):
            return {
                "id": 1,
                "nom": email.split("@")[0],
                "role": "ETUDIANT",
                "email": email,
            }

        if re.match(r"^[a-z]+(\.[a-z]+)*@ulc-icam\.com$", email):
            return {
                "id": 1,
                "nom": email.split("@")[0],
                "role": "GESTIONNAIRE",
                "email": email,
            }

        return None