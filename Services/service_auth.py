import re
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Database" / "fablab.db"


class AuthService:
    def __init__(self):
        self.ensure_tables()

    def connect(self):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_tables(self):
        with self.connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS Etudiants (
                id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_etudiant TEXT NOT NULL,
                prenom_etudiant TEXT,
                post_nom_etudiant TEXT,
                adresse_mail_etudiant TEXT NOT NULL UNIQUE,
                mot_de_passe_e TEXT NOT NULL,
                telephone_etudiant TEXT,
                promotion TEXT,
                date_inscription TEXT DEFAULT CURRENT_DATE,
                statut_compte TEXT DEFAULT 'actif'
            )
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS Gestionnaires (
                id_gestionnaire INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_gestionnaire TEXT NOT NULL,
                email_gestionnaire TEXT NOT NULL UNIQUE,
                telephone_gestionnaire TEXT,
                mot_de_passe_g TEXT NOT NULL
            )
            """)

            conn.commit()

    def se_connecter(self, email: str, password: str):
        email = email.strip().lower()
        password = password.strip()

        if not email or not password:
            return None

        # Mot de passe simple pour le projet
        if password != "1234":
            return None

        if self.est_email_etudiant(email):
            return self.connecter_ou_creer_etudiant(email, password)

        if self.est_email_gestionnaire(email):
            return self.connecter_ou_creer_gestionnaire(email, password)

        return None

    def est_email_etudiant(self, email: str) -> bool:
        return re.match(
            r"^[a-z]+(\.[a-z]+)*@[0-9]{4}\.ulc-icam\.com$",
            email
        ) is not None

    def est_email_gestionnaire(self, email: str) -> bool:
        return re.match(
            r"^[a-z]+(\.[a-z]+)*@ulc-icam\.com$",
            email
        ) is not None

    def connecter_ou_creer_etudiant(self, email: str, password: str):
        with self.connect() as conn:
            etudiant = conn.execute("""
                SELECT *
                FROM Etudiants
                WHERE adresse_mail_etudiant = ?
            """, (email,)).fetchone()

            if etudiant:
                return {
                    "id": etudiant["id_etudiant"],
                    "nom": etudiant["nom_etudiant"],
                    "role": "ETUDIANT",
                    "email": etudiant["adresse_mail_etudiant"],
                    "promotion": etudiant["promotion"],
                }

            nom_email = email.split("@")[0]
            nom_affiche = nom_email.replace(".", " ").title()
            annee = email.split("@")[1].split(".")[0]

            cursor = conn.execute("""
                INSERT INTO Etudiants
                (
                    nom_etudiant,
                    prenom_etudiant,
                    post_nom_etudiant,
                    adresse_mail_etudiant,
                    mot_de_passe_e,
                    telephone_etudiant,
                    promotion
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nom_affiche,
                "",
                "",
                email,
                password,
                "",
                f"Promotion {annee}",
            ))

            conn.commit()

            return {
                "id": cursor.lastrowid,
                "nom": nom_affiche,
                "role": "ETUDIANT",
                "email": email,
                "promotion": f"Promotion {annee}",
            }

    def connecter_ou_creer_gestionnaire(self, email: str, password: str):
        with self.connect() as conn:
            gestionnaire = conn.execute("""
                SELECT *
                FROM Gestionnaires
                WHERE email_gestionnaire = ?
            """, (email,)).fetchone()

            if gestionnaire:
                return {
                    "id": gestionnaire["id_gestionnaire"],
                    "nom": gestionnaire["nom_gestionnaire"],
                    "role": "GESTIONNAIRE",
                    "email": gestionnaire["email_gestionnaire"],
                }

            nom_email = email.split("@")[0]
            nom_affiche = nom_email.replace(".", " ").title()

            cursor = conn.execute("""
                INSERT INTO Gestionnaires
                (
                    nom_gestionnaire,
                    email_gestionnaire,
                    telephone_gestionnaire,
                    mot_de_passe_g
                )
                VALUES (?, ?, ?, ?)
            """, (
                nom_affiche,
                email,
                "",
                password,
            ))

            conn.commit()

            return {
                "id": cursor.lastrowid,
                "nom": nom_affiche,
                "role": "GESTIONNAIRE",
                "email": email,
            }