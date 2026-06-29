from Repositories.Sqlite_repo import SQLiteRepository
from Models.machine import MachineDTO


class SQLiteMachineRepository(SQLiteRepository):
    TABLE = "Machines"
    PK = "id_machine"
    DTO_CLASS = MachineDTO

    def find_disponibles(self) -> list[MachineDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Machines
            WHERE statut = 'disponible'
            ORDER BY nom_machine ASC
            """
        )
        return [self._to_dto(row) for row in rows]

    def find_hors_service(self) -> list[MachineDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Machines
            WHERE statut = 'hors service'
            ORDER BY nom_machine ASC
            """
        )
        return [self._to_dto(row) for row in rows]

    def find_by_type(self, type_machine: str) -> list[MachineDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Machines
            WHERE type_machine = ?
            ORDER BY nom_machine ASC
            """,
            (type_machine,),
        )
        return [self._to_dto(row) for row in rows]