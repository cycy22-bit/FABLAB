from Repositories.Sqlite_repo import SQLiteRepository
from Models.emprunt import EmpruntDTO


class SQLiteEmpruntRepository(SQLiteRepository):
    TABLE = "Emprunts"
    PK = "id_emprunt"
    DTO_CLASS = EmpruntDTO

    def find_emprunt_actif(
        self,
        id_etudiant: int,
        id_materiel: int
    ) -> EmpruntDTO | None:
        row = self.fetch_one(
            """
            SELECT *
            FROM Emprunts
            WHERE id_etudiant = ?
            AND id_materiel = ?
            AND statut_emprunt IN ('en attente', 'accepté', 'en cours')
            """,
            (id_etudiant, id_materiel),
        )
        return self._to_dto(row) if row else None

    def find_by_etudiant(self, id_etudiant: int) -> list[EmpruntDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Emprunts
            WHERE id_etudiant = ?
            ORDER BY date_emprunt DESC
            """,
            (id_etudiant,),
        )
        return [self._to_dto(row) for row in rows]

    def find_en_cours(self) -> list[EmpruntDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Emprunts
            WHERE statut_emprunt IN ('en attente', 'accepté', 'en cours')
            ORDER BY date_emprunt DESC
            """
        )
        return [self._to_dto(row) for row in rows]

    def find_retards(self) -> list[EmpruntDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Emprunts
            WHERE date_retour_prevue < DATE('now')
            AND statut_emprunt IN ('accepté', 'en cours')
            ORDER BY date_retour_prevue ASC
            """
        )
        return [self._to_dto(row) for row in rows]

    def find_historique_etudiant(self, id_etudiant: int) -> list[EmpruntDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Emprunts
            WHERE id_etudiant = ?
            ORDER BY date_emprunt DESC
            """,
            (id_etudiant,),
        )
        return [self._to_dto(row) for row in rows]