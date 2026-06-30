import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "fablab.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        c.execute("PRAGMA foreign_keys = ON")

        c.execute("""
        CREATE TABLE IF NOT EXISTS Etudiants (
            id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_etudiant TEXT NOT NULL,
            prenom_etudiant TEXT,
            adresse_mail_etudiant TEXT NOT NULL UNIQUE,
            mot_de_passe_e TEXT NOT NULL,
            promotion TEXT,
            statut_compte TEXT DEFAULT 'actif'
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Gestionnaires (
            id_gestionnaire INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_gestionnaire TEXT NOT NULL,
            email_gestionnaire TEXT NOT NULL UNIQUE,
            mot_de_passe_g TEXT NOT NULL
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Materiels (
            id_materiel INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_materiel TEXT NOT NULL,
            categorie TEXT NOT NULL,
            quantite_stock INTEGER NOT NULL DEFAULT 0,
            stock_minimum INTEGER NOT NULL DEFAULT 0
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Machines (
            id_machine INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_machine TEXT NOT NULL,
            type_machine TEXT NOT NULL,
            description TEXT,
            caracteristiques_techniques TEXT,
            statut TEXT DEFAULT 'disponible',
            emplacement TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Fournisseurs (
            id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_fournisseur TEXT NOT NULL,
            adresse TEXT,
            telephone TEXT,
            email TEXT,
            site_web TEXT,
            delai_livraison_moyen TEXT,
            conditions_paiement TEXT
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Reservations (
            id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER NOT NULL,
            id_machine INTEGER NOT NULL,
            date_reservation TEXT NOT NULL,
            heure_debut TEXT NOT NULL,
            heure_fin TEXT NOT NULL,
            statut_reservation TEXT DEFAULT 'en attente',
            FOREIGN KEY (id_etudiant) REFERENCES Etudiants(id_etudiant),
            FOREIGN KEY (id_machine) REFERENCES Machines(id_machine)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Emprunts (
            id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER NOT NULL,
            id_materiel INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            duree INTEGER NOT NULL,
            statut_emprunt TEXT DEFAULT 'en attente',
            date_emprunt TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_etudiant) REFERENCES Etudiants(id_etudiant),
            FOREIGN KEY (id_materiel) REFERENCES Materiels(id_materiel)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Commandes (
            id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fournisseur INTEGER NOT NULL,
            id_gestionnaire INTEGER NOT NULL,
            date_commande TEXT NOT NULL,
            date_livraison_prevue TEXT NOT NULL,
            statut_commande TEXT DEFAULT 'en cours',
            montant_total REAL NOT NULL,
            FOREIGN KEY (id_fournisseur) REFERENCES Fournisseurs(id_fournisseur),
            FOREIGN KEY (id_gestionnaire) REFERENCES Gestionnaires(id_gestionnaire)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS MouvementsStock (
            id_mouvement INTEGER PRIMARY KEY AUTOINCREMENT,
            type_mouvement TEXT NOT NULL,
            id_materiel INTEGER,
            quantite INTEGER,
            description TEXT,
            date_mouvement TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS Alertes (
            id_alerte INTEGER PRIMARY KEY AUTOINCREMENT,
            type_alerte TEXT NOT NULL,
            message_alerte TEXT NOT NULL,
            date_alerte TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        c.executemany("""
        INSERT OR IGNORE INTO Etudiants
        (id_etudiant, nom_etudiant, prenom_etudiant, adresse_mail_etudiant, mot_de_passe_e, promotion)
        VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (1, "Mpoze", "Jessika", "jessika@2025.ulc-icam.com", "1234", "L2"),
            (2, "Lukamba", "Nathan", "nathan@2025.ulc-icam.com", "1234", "L2"),
        ])

        c.executemany("""
        INSERT OR IGNORE INTO Gestionnaires
        (id_gestionnaire, nom_gestionnaire, email_gestionnaire, mot_de_passe_g)
        VALUES (?, ?, ?, ?)
        """, [
            (1, "Gestionnaire FabLab", "gestionnaire@ulc-cam.com", "1234"),
        ])

        c.executemany("""
        INSERT OR IGNORE INTO Materiels
        (id_materiel, nom_materiel, categorie, quantite_stock, stock_minimum)
        VALUES (?, ?, ?, ?, ?)
        """, [
            (1, "Arduino UNO", "Microcontrôleur", 4, 2),
            (2, "ESP32", "Microcontrôleur", 6, 2),
            (3, "Potentiomètre 10kΩ", "Composant électronique", 12, 5),
            (4, "Résistance 5kΩ", "Composant électronique", 18, 5),
            (5, "Capteur ultrason HC-SR04", "Capteur", 5, 2),
            (6, "Câble USB", "Accessoire", 10, 3),
            (7, "Gants de protection", "EPI", 20, 5),
        ])

        c.executemany("""
        INSERT OR IGNORE INTO Machines
        (id_machine, nom_machine, type_machine, description, caracteristiques_techniques, statut, emplacement)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, "Imprimante 3D", "Impression 3D", "Machine pour prototypage rapide", "PLA/ABS", "disponible", "Atelier 1"),
            (2, "Découpeuse laser", "Découpe", "Découpe et gravure", "Bois, plexiglas", "disponible", "Atelier 2"),
            (3, "Perceuse colonne", "Usinage", "Perçage mécanique", "Vitesse réglable", "disponible", "Atelier mécanique"),
        ])

        c.executemany("""
        INSERT OR IGNORE INTO Fournisseurs
        (id_fournisseur, nom_fournisseur, adresse, telephone, email, site_web, delai_livraison_moyen, conditions_paiement)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, "Fournisseur Arduino", "Kinshasa/Gombe", "0810000001", "arduino@fournisseur.com", "www.arduino-fournisseur.com", "7 jours", "Paiement à la livraison"),
            (2, "Fournisseur EPI", "Kinshasa/Limete", "0810000002", "epi@fournisseur.com", "www.epi-rdc.com", "5 jours", "Paiement comptant"),
            (3, "Fournisseur Composants", "Kinshasa/Matete", "0810000003", "composants@fournisseur.com", "www.composants-rdc.com", "10 jours", "Paiement après livraison"),
        ])

        conn.commit()

    print("Base de données FabLab initialisée avec succès.")


if __name__ == "__main__":
    init_db()