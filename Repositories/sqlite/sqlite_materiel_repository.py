from Repositories.Sqlite_repo import SQLiteRepository
from Models.materiel import MaterielDTO


class SQLiteMaterielRepository(SQLiteRepository):
    TABLE = "Materiels"
    PK = "id_materiel"
    DTO_CLASS = MaterielDTO

    def get_stock_faible(self) -> list[MaterielDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Materiels
            WHERE quantite_stock < stock_minimum
            ORDER BY quantite_stock ASC
            """
        )
        return [self._to_dto(row) for row in rows]

    def find_disponibles(self) -> list[MaterielDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Materiels
            WHERE quantite_stock > 0
            ORDER BY nom_materiel ASC
            """
        )
        return [self._to_dto(row) for row in rows]

    def find_by_categorie(self, categorie: str) -> list[MaterielDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Materiels
            WHERE categorie = ?
            ORDER BY nom_materiel ASC
            """,
            (categorie,),
        )
        return [self._to_dto(row) for row in rows]