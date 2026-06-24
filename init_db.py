import sqlite3


DATABASE_PATH = "database.db"


class DatabaseInitializer:

    def __init__(self, database_path: str = DATABASE_PATH):
        self.database_path = database_path

    def create_tables(self) -> None:
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS materiels (
            id_materiel INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_materiel TEXT NOT NULL,
            categorie TEXT NOT NULL,
            quantite_stock INTEGER NOT NULL DEFAULT 0,
            stock_minimum INTEGER NOT NULL DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id_etudiant INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telephone TEXT NOT NULL,
            promotion TEXT NOT NULL,
            statut_compte TEXT NOT NULL DEFAULT 'actif'
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprunts (
            id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER NOT NULL,
            id_materiel INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            date_emprunt TEXT NOT NULL,
            date_retour_prevue TEXT NOT NULL,
            statut_emprunt TEXT NOT NULL DEFAULT 'en cours',

            FOREIGN KEY (id_etudiant) REFERENCES etudiants(id_etudiant),
            FOREIGN KEY (id_materiel) REFERENCES materiels(id_materiel)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id_machine INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_machine TEXT NOT NULL,
            type_machine TEXT NOT NULL,
            statut_machine TEXT NOT NULL DEFAULT 'disponible',
            emplacement TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
            id_etudiant INTEGER NOT NULL,
            id_machine INTEGER NOT NULL,
            date_reservation TEXT NOT NULL,
            heure_debut TEXT NOT NULL,
            heure_fin TEXT NOT NULL,
            statut_reservation TEXT NOT NULL DEFAULT 'en attente',

            FOREIGN KEY (id_etudiant) REFERENCES etudiants(id_etudiant),
            FOREIGN KEY (id_machine) REFERENCES machines(id_machine)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs (
            id_fournisseur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_fournisseur TEXT NOT NULL,
            adresse TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            site_web TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commandes (
            id_commande INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fournisseur INTEGER NOT NULL,
            date_commande TEXT NOT NULL,
            date_livraison_prevue TEXT NOT NULL,
            statut_commande TEXT NOT NULL DEFAULT 'en attente',
            montant_total REAL NOT NULL DEFAULT 0,

            FOREIGN KEY (id_fournisseur) REFERENCES fournisseurs(id_fournisseur)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alertes (
            id_alerte INTEGER PRIMARY KEY AUTOINCREMENT,
            type_alerte TEXT NOT NULL,
            message_alerte TEXT NOT NULL,
            date_alerte TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mouvement_stock (
            id_mouvement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_materiel INTEGER NOT NULL,
            type_mouvement TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            date_mouvement TEXT NOT NULL,

            FOREIGN KEY (id_materiel) REFERENCES materiels(id_materiel)
        )
        """)

        conn.commit()
        conn.close()


if __name__ == "__main__":
    initializer = DatabaseInitializer()
    initializer.create_tables()
    print("Base de données SG-FabLab créée avec succès.")