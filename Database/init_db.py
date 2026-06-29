import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "fablab.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Gestionnaires (
            id_gestionnaire INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_gestionnaire TEXT NOT NULL,
            email_gestionnaire TEXT NOT NULL UNIQUE,
            telephone_gestionnaire TEXT,
            mot_de_passe_g TEXT NOT NULL
        )
        """)

        cursor.execute("""
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

        cursor.execute("""
        INSERT OR IGNORE INTO Gestionnaires
        (nom_gestionnaire, email_gestionnaire, telephone_gestionnaire, mot_de_passe_g)
        VALUES ('Gestionnaire Test', 'gestionnaire@ucam.com', '000000000', '1234')
        """)

        cursor.execute("""
        INSERT OR IGNORE INTO Etudiants
        (nom_etudiant, prenom_etudiant, adresse_mail_etudiant, mot_de_passe_e, telephone_etudiant, promotion)
        VALUES ('Mpoze', 'Jessika', 'jessika@2025.ucam.com', '1234', '000000000', 'L2')
        """)

        conn.commit()

    print("Base fablab.db initialisée avec succès.")


if __name__ == "__main__":
    init_db()