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