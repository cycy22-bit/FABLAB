from Repositories.Sqlite_repo import SQLiteRepository
from Models.etudiant import EtudiantDTO


class SQLiteEtudiantRepository(SQLiteRepository):
    TABLE = "Etudiants"
    PK = "id_etudiant"
    DTO_CLASS = EtudiantDTO

    def find_by_email(self, email: str) -> EtudiantDTO | None:
        row = self.fetch_one(
            "SELECT * FROM Etudiants WHERE adresse_mail_etudiant = ?",
            (email,),
        )
        return self._to_dto(row) if row else None

    def email_exists(self, email: str) -> bool:
        row = self.fetch_one(
            "SELECT 1 FROM Etudiants WHERE adresse_mail_etudiant = ?",
            (email,),
        )
        return row is not None

    def count_reservations_actives(self, id_etudiant: int) -> int:
        row = self.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM Reservations
            WHERE id_etudiant = ?
            AND statut_reservation IN ('en attente', 'validée', 'active')
            """,
            (id_etudiant,),
        )
        return row["total"] if row else 0

    def count_emprunts_actifs(self, id_etudiant: int) -> int:
        row = self.fetch_one(
            """
            SELECT COUNT(*) AS total
            FROM Emprunts
            WHERE id_etudiant = ?
            AND statut_emprunt IN ('en attente', 'accepté', 'en cours')
            """,
            (id_etudiant,),
        )
        return row["total"] if row else 0