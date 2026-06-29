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