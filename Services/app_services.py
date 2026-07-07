import sqlite3
from pathlib import Path
from types import SimpleNamespace

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Database" / "fablab.db"


def to_objects(rows):
    return [SimpleNamespace(**dict(row)) for row in rows]


def ensure_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(str(DB_PATH)) as conn:
        c = conn.cursor()

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
            destinataire_role TEXT NOT NULL,
            id_destinataire INTEGER,
            statut_alerte TEXT DEFAULT 'non lue',
            date_alerte TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        c.execute("SELECT COUNT(*) FROM Materiels")
        total = c.fetchone()[0]

        if total == 0:
            c.executemany("""
            INSERT INTO Materiels
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

        # ==========================
        # MIGRATIONS AUTOMATIQUES
        # ==========================

        def add_column_if_missing(table, column, definition):
            c.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in c.fetchall()]
            if column not in columns:
                c.execute(
                    f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
                )

        # Emprunts
        add_column_if_missing("Emprunts", "duree", "INTEGER DEFAULT 1")
        add_column_if_missing(
            "Emprunts",
            "statut_emprunt",
            "TEXT DEFAULT 'en attente'"
        )

        # Réservations
        add_column_if_missing(
            "Reservations",
            "statut_reservation",
            "TEXT DEFAULT 'en attente'"
        )

        # Alertes
        add_column_if_missing(
            "Alertes",
            "destinataire_role",
            "TEXT DEFAULT 'GESTIONNAIRE'"
        )

        add_column_if_missing(
            "Alertes",
            "id_destinataire",
            "INTEGER"
        )

        add_column_if_missing(
            "Alertes",
            "statut_alerte",
            "TEXT DEFAULT 'non lue'"
        )

        conn.commit()

class BaseService:
    def connect(self):
        ensure_database()
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def creer_alerte_interne(
        self,
        conn,
        type_alerte,
        message_alerte,
        destinataire_role,
        id_destinataire=None
    ):
        conn.execute("""
        INSERT INTO Alertes
        (type_alerte, message_alerte, destinataire_role, id_destinataire)
        VALUES (?, ?, ?, ?)
        """, (
            type_alerte,
            message_alerte,
            destinataire_role,
            id_destinataire,
        ))


class StockService(BaseService):
    def consulter_inventaire(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT *
            FROM Materiels
            ORDER BY nom_materiel
            """).fetchall()
            return to_objects(rows)

    def get_all(self):
        return self.consulter_inventaire()

    def ajouter_materiel(self, nom_materiel, categorie, quantite_stock, stock_minimum):
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO Materiels
            (nom_materiel, categorie, quantite_stock, stock_minimum)
            VALUES (?, ?, ?, ?)
            """, (nom_materiel, categorie, quantite_stock, stock_minimum))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, quantite, description)
            VALUES ('ajout_materiel', ?, ?)
            """, (quantite_stock, f"Ajout matériel : {nom_materiel}"))

            conn.commit()
        return True

    def ajouter_quantite(self, id_materiel, quantite):
        if quantite <= 0:
            return False

        with self.connect() as conn:
            conn.execute("""
            UPDATE Materiels
            SET quantite_stock = quantite_stock + ?
            WHERE id_materiel = ?
            """, (quantite, id_materiel))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, id_materiel, quantite, description)
            VALUES ('ajout_stock', ?, ?, ?)
            """, (id_materiel, quantite, f"Ajout de {quantite} unité(s)"))

            conn.commit()
        return True

    def retirer_quantite(self, id_materiel, quantite):
        if quantite <= 0:
            return False

        with self.connect() as conn:
            stock = conn.execute("""
            SELECT quantite_stock
            FROM Materiels
            WHERE id_materiel = ?
            """, (id_materiel,)).fetchone()

            if stock is None or stock["quantite_stock"] < quantite:
                return False

            conn.execute("""
            UPDATE Materiels
            SET quantite_stock = quantite_stock - ?
            WHERE id_materiel = ?
            """, (quantite, id_materiel))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, id_materiel, quantite, description)
            VALUES ('retrait_stock', ?, ?, ?)
            """, (id_materiel, quantite, f"Retrait de {quantite} unité(s)"))

            conn.commit()
        return True


class MachineService(BaseService):
    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT *
            FROM Machines
            ORDER BY nom_machine
            """).fetchall()
            return to_objects(rows)

    def create(self, nom_machine, type_machine, description, caracteristiques_techniques, emplacement):
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO Machines
            (nom_machine, type_machine, description, caracteristiques_techniques, statut, emplacement)
            VALUES (?, ?, ?, ?, 'disponible', ?)
            """, (nom_machine, type_machine, description, caracteristiques_techniques, emplacement))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('ajout_machine', ?)
            """, (f"Ajout de la machine : {nom_machine}",))

            conn.commit()
        return True


class FournisseurService(BaseService):
    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT *
            FROM Fournisseurs
            ORDER BY nom_fournisseur
            """).fetchall()
            return to_objects(rows)

    def create(
        self,
        nom_fournisseur,
        adresse,
        telephone,
        email,
        site_web,
        delai_livraison_moyen,
        conditions_paiement
    ):
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO Fournisseurs
            (nom_fournisseur, adresse, telephone, email, site_web, delai_livraison_moyen, conditions_paiement)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nom_fournisseur,
                adresse,
                telephone,
                email,
                site_web,
                delai_livraison_moyen,
                conditions_paiement,
            ))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('ajout_fournisseur', ?)
            """, (f"Ajout du fournisseur : {nom_fournisseur}",))

            conn.commit()
        return True


class ReservationService(BaseService):
    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT r.*, e.nom_etudiant, m.nom_machine
            FROM Reservations r
            JOIN Etudiants e ON e.id_etudiant = r.id_etudiant
            JOIN Machines m ON m.id_machine = r.id_machine
            ORDER BY r.id_reservation DESC
            """).fetchall()
            return to_objects(rows)

    def find_by_etudiant(self, id_etudiant):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT r.*, m.nom_machine
            FROM Reservations r
            JOIN Machines m ON m.id_machine = r.id_machine
            WHERE r.id_etudiant = ?
            ORDER BY r.id_reservation DESC
            """, (id_etudiant,)).fetchall()
            return to_objects(rows)

    def reserver_machine(self, id_etudiant, id_machine, date_reservation, heure_debut, heure_fin):
        with self.connect() as conn:
            conflit = conn.execute("""
            SELECT id_reservation
            FROM Reservations
            WHERE id_machine = ?
            AND date_reservation = ?
            AND statut_reservation IN ('en attente', 'validée')
            AND NOT (heure_fin <= ? OR heure_debut >= ?)
            """, (id_machine, date_reservation, heure_debut, heure_fin)).fetchone()

            if conflit:
                self.creer_alerte_interne(
                    conn,
                    "Réservation bloquée",
                    "Ce créneau est déjà occupé pour cette machine.",
                    "ETUDIANT",
                    id_etudiant,
                )
                conn.commit()
                return False

            conn.execute("""
            INSERT INTO Reservations
            (id_etudiant, id_machine, date_reservation, heure_debut, heure_fin, statut_reservation)
            VALUES (?, ?, ?, ?, ?, 'en attente')
            """, (id_etudiant, id_machine, date_reservation, heure_debut, heure_fin))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('demande_reservation', ?)
            """, (f"Demande de réservation machine {id_machine} par étudiant {id_etudiant}",))

            self.creer_alerte_interne(
                conn,
                "Nouvelle réservation",
                f"Nouvelle demande de réservation de la machine {id_machine}.",
                "GESTIONNAIRE",
                None,
            )

            conn.commit()
        return True

    def accepter_reservation(self, id_reservation):
        with self.connect() as conn:
            reservation = conn.execute("""
            SELECT *
            FROM Reservations
            WHERE id_reservation = ?
            """, (id_reservation,)).fetchone()

            if reservation is None:
                return False

            if reservation["statut_reservation"] != "en attente":
                return False

            conn.execute("""
            UPDATE Reservations
            SET statut_reservation = 'validée'
            WHERE id_reservation = ?
            """, (id_reservation,))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('reservation_validée', ?)
            """, (f"Réservation {id_reservation} validée",))

            self.creer_alerte_interne(
                conn,
                "Réservation acceptée",
                f"Votre réservation n°{id_reservation} a été acceptée.",
                "ETUDIANT",
                reservation["id_etudiant"],
            )

            conn.commit()
        return True

    def refuser_reservation(self, id_reservation):
        with self.connect() as conn:
            reservation = conn.execute("""
            SELECT *
            FROM Reservations
            WHERE id_reservation = ?
            """, (id_reservation,)).fetchone()

            if reservation is None:
                return False

            if reservation["statut_reservation"] != "en attente":
                return False

            conn.execute("""
            UPDATE Reservations
            SET statut_reservation = 'refusée'
            WHERE id_reservation = ?
            """, (id_reservation,))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('reservation_refusée', ?)
            """, (f"Réservation {id_reservation} refusée",))

            self.creer_alerte_interne(
                conn,
                "Réservation refusée",
                f"Votre réservation n°{id_reservation} a été refusée.",
                "ETUDIANT",
                reservation["id_etudiant"],
            )

            conn.commit()
        return True


class EmpruntService(BaseService):
    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT em.*, e.nom_etudiant, m.nom_materiel
            FROM Emprunts em
            JOIN Etudiants e ON e.id_etudiant = em.id_etudiant
            JOIN Materiels m ON m.id_materiel = em.id_materiel
            ORDER BY em.id_emprunt DESC
            """).fetchall()
            return to_objects(rows)

    def find_by_etudiant(self, id_etudiant):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT em.*, m.nom_materiel
            FROM Emprunts em
            JOIN Materiels m ON m.id_materiel = em.id_materiel
            WHERE em.id_etudiant = ?
            ORDER BY em.id_emprunt DESC
            """, (id_etudiant,)).fetchall()
            return to_objects(rows)

    def emprunter_materiel(self, id_etudiant, id_materiel, quantite, duree):
        with self.connect() as conn:
            deja = conn.execute("""
            SELECT id_emprunt
            FROM Emprunts
            WHERE id_etudiant = ?
            AND id_materiel = ?
            AND statut_emprunt IN ('en attente', 'accepté', 'en cours')
            """, (id_etudiant, id_materiel)).fetchone()

            if deja:
                self.creer_alerte_interne(
                    conn,
                    "Emprunt bloqué",
                    "Vous avez déjà un emprunt actif pour ce matériel.",
                    "ETUDIANT",
                    id_etudiant,
                )
                conn.commit()
                return False

            stock = conn.execute("""
            SELECT quantite_stock
            FROM Materiels
            WHERE id_materiel = ?
            """, (id_materiel,)).fetchone()

            if stock is None or stock["quantite_stock"] < quantite:
                self.creer_alerte_interne(
                    conn,
                    "Emprunt bloqué",
                    "Stock insuffisant pour ce matériel.",
                    "ETUDIANT",
                    id_etudiant,
                )
                conn.commit()
                return False

            conn.execute("""
            INSERT INTO Emprunts
            (id_etudiant, id_materiel, quantite, duree, statut_emprunt)
            VALUES (?, ?, ?, ?, 'en attente')
            """, (id_etudiant, id_materiel, quantite, duree))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, id_materiel, quantite, description)
            VALUES ('demande_emprunt', ?, ?, ?)
            """, (id_materiel, quantite, f"Demande d'emprunt de {quantite} unité(s) par étudiant {id_etudiant}"))

            self.creer_alerte_interne(
                conn,
                "Nouvelle demande d'emprunt",
                f"Nouvelle demande d'emprunt pour le matériel {id_materiel}.",
                "GESTIONNAIRE",
                None,
            )

            conn.commit()
        return True

    def accepter_emprunt(self, id_emprunt):
        with self.connect() as conn:
            emprunt = conn.execute("""
            SELECT *
            FROM Emprunts
            WHERE id_emprunt = ?
            """, (id_emprunt,)).fetchone()

            if emprunt is None:
                return False

            if emprunt["statut_emprunt"] != "en attente":
                return False

            stock = conn.execute("""
            SELECT quantite_stock
            FROM Materiels
            WHERE id_materiel = ?
            """, (emprunt["id_materiel"],)).fetchone()

            if stock is None or stock["quantite_stock"] < emprunt["quantite"]:
                self.creer_alerte_interne(
                    conn,
                    "Emprunt impossible",
                    f"Impossible d'accepter l'emprunt n°{id_emprunt} : stock insuffisant.",
                    "GESTIONNAIRE",
                    None,
                )
                conn.commit()
                return False

            conn.execute("""
            UPDATE Emprunts
            SET statut_emprunt = 'accepté'
            WHERE id_emprunt = ?
            """, (id_emprunt,))

            conn.execute("""
            UPDATE Materiels
            SET quantite_stock = quantite_stock - ?
            WHERE id_materiel = ?
            """, (emprunt["quantite"], emprunt["id_materiel"]))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, id_materiel, quantite, description)
            VALUES ('emprunt_accepté', ?, ?, ?)
            """, (
                emprunt["id_materiel"],
                emprunt["quantite"],
                f"Emprunt {id_emprunt} accepté et stock diminué",
            ))

            self.creer_alerte_interne(
                conn,
                "Emprunt accepté",
                f"Votre demande d'emprunt n°{id_emprunt} a été acceptée.",
                "ETUDIANT",
                emprunt["id_etudiant"],
            )

            conn.commit()
        return True

    def refuser_emprunt(self, id_emprunt):
        with self.connect() as conn:
            emprunt = conn.execute("""
            SELECT *
            FROM Emprunts
            WHERE id_emprunt = ?
            """, (id_emprunt,)).fetchone()

            if emprunt is None:
                return False

            if emprunt["statut_emprunt"] != "en attente":
                return False

            conn.execute("""
            UPDATE Emprunts
            SET statut_emprunt = 'refusé'
            WHERE id_emprunt = ?
            """, (id_emprunt,))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('emprunt_refusé', ?)
            """, (f"Emprunt {id_emprunt} refusé",))

            self.creer_alerte_interne(
                conn,
                "Emprunt refusé",
                f"Votre demande d'emprunt n°{id_emprunt} a été refusée.",
                "ETUDIANT",
                emprunt["id_etudiant"],
            )

            conn.commit()
        return True


class CommandeService(BaseService):
    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT c.*, f.nom_fournisseur, g.nom_gestionnaire
            FROM Commandes c
            JOIN Fournisseurs f ON f.id_fournisseur = c.id_fournisseur
            JOIN Gestionnaires g ON g.id_gestionnaire = c.id_gestionnaire
            ORDER BY c.id_commande DESC
            """).fetchall()
            return to_objects(rows)

    def creer_commande(self, id_fournisseur, id_gestionnaire, date_commande, date_livraison_prevue, montant_total):
        with self.connect() as conn:
            conn.execute("""
            INSERT INTO Commandes
            (id_fournisseur, id_gestionnaire, date_commande, date_livraison_prevue, montant_total)
            VALUES (?, ?, ?, ?, ?)
            """, (id_fournisseur, id_gestionnaire, date_commande, date_livraison_prevue, montant_total))

            conn.execute("""
            INSERT INTO MouvementsStock
            (type_mouvement, description)
            VALUES ('commande', ?)
            """, (f"Commande créée chez fournisseur {id_fournisseur}",))

            self.creer_alerte_interne(
                conn,
                "Commande créée",
                f"Une commande a été créée chez le fournisseur {id_fournisseur}.",
                "GESTIONNAIRE",
                None,
            )

            conn.commit()
        return True


class HistoriqueService(BaseService):
    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT *
            FROM MouvementsStock
            ORDER BY id_mouvement DESC
            """).fetchall()
            return to_objects(rows)


class AlerteService(BaseService):
    def creer_alerte(self, type_alerte, message_alerte, destinataire_role, id_destinataire=None):
        with self.connect() as conn:
            self.creer_alerte_interne(
                conn,
                type_alerte,
                message_alerte,
                destinataire_role,
                id_destinataire,
            )
            conn.commit()
        return True

    def get_all(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT
                id_alerte,
                type_alerte,
                message_alerte,
                destinataire_role,
                id_destinataire,
                statut_alerte,
                date_alerte
            FROM Alertes

            UNION ALL

            SELECT
                id_materiel AS id_alerte,
                'Stock faible' AS type_alerte,
                'Stock faible pour : ' || nom_materiel AS message_alerte,
                'GESTIONNAIRE' AS destinataire_role,
                NULL AS id_destinataire,
                'non lue' AS statut_alerte,
                CURRENT_TIMESTAMP AS date_alerte
            FROM Materiels
            WHERE quantite_stock < stock_minimum

            ORDER BY date_alerte DESC
            """).fetchall()

            return to_objects(rows)

    def find_by_etudiant(self, id_etudiant):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT
                id_alerte,
                type_alerte,
                message_alerte,
                destinataire_role,
                id_destinataire,
                statut_alerte,
                date_alerte
            FROM Alertes
            WHERE destinataire_role = 'ETUDIANT'
            AND id_destinataire = ?
            ORDER BY date_alerte DESC
            """, (id_etudiant,)).fetchall()

            return to_objects(rows)

    def find_by_gestionnaire(self):
        with self.connect() as conn:
            rows = conn.execute("""
            SELECT
                id_alerte,
                type_alerte,
                message_alerte,
                destinataire_role,
                id_destinataire,
                statut_alerte,
                date_alerte
            FROM Alertes
            WHERE destinataire_role = 'GESTIONNAIRE'

            UNION ALL

            SELECT
                id_materiel AS id_alerte,
                'Stock faible' AS type_alerte,
                'Stock faible pour : ' || nom_materiel AS message_alerte,
                'GESTIONNAIRE' AS destinataire_role,
                NULL AS id_destinataire,
                'non lue' AS statut_alerte,
                CURRENT_TIMESTAMP AS date_alerte
            FROM Materiels
            WHERE quantite_stock < stock_minimum

            ORDER BY date_alerte DESC
            """).fetchall()

            return to_objects(rows)