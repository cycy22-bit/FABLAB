from Repositories.Sqlite_repo import SQLiteRepository
from Models.gestionnaire import GestionnaireDTO


class SQLiteGestionnaireRepository(SQLiteRepository):
    TABLE = "Gestionnaires"
    PK = "id_gestionnaire"
    DTO_CLASS = GestionnaireDTO

    def find_by_email(self, email: str) -> GestionnaireDTO | None:
        row = self.fetch_one(
            "SELECT * FROM Gestionnaires WHERE email_gestionnaire = ?",
            (email,),
        )
        return self._to_dto(row) if row else None

    def email_exists(self, email: str) -> bool:
        row = self.fetch_one(
            "SELECT 1 FROM Gestionnaires WHERE email_gestionnaire = ?",
            (email,),
        )
        return row is not None