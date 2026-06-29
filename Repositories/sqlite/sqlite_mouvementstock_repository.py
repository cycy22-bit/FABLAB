from Repositories.Sqlite_repo import SQLiteRepository
from Models.mouvement_stock import MouvementStockDTO


class SQLiteMouvementStockRepository(SQLiteRepository):
    TABLE = "MouvementStock"
    PK = "id_mouvement"
    DTO_CLASS = MouvementStockDTO

    def get_by_materiel(self, id_materiel: int) -> list[MouvementStockDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM MouvementStock
            WHERE id_materiel = ?
            ORDER BY date_mouvement DESC
            """,
            (id_materiel,),
        )
        return [self._to_dto(row) for row in rows]

    def find_by_type(self, type_mouvement: str) -> list[MouvementStockDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM MouvementStock
            WHERE type_mouvement = ?
            ORDER BY date_mouvement DESC
            """,
            (type_mouvement,),
        )
        return [self._to_dto(row) for row in rows]

    def find_by_periode(self, date_debut: str, date_fin: str) -> list[MouvementStockDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM MouvementStock
            WHERE date_mouvement BETWEEN ? AND ?
            ORDER BY date_mouvement DESC
            """,
            (date_debut, date_fin),
        )
        return [self._to_dto(row) for row in rows]