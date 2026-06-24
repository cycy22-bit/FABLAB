from typing import Any

from Repositories.sqlite_repo import SQLiteRepository

from Models.etudiant import EtudiantDTO
from Models.gestionnaire import GestionnaireDTO
from Models.machine import MachineDTO
from Models.materiel import MaterielDTO
from Models.reservation import ReservationDTO
from Models.emprunt import EmpruntDTO
from Models.fournisseur import FournisseurDTO
from Models.commande import CommandeDTO
from Models.lignecommande import LigneCommandeDTO
from Models.mouvement_stock import MouvementStockDTO
from Models.alerte import AlerteDTO


class BaseSQLiteRepository(SQLiteRepository):
    TABLE: str = ""
    PK: str = ""
    DTO_CLASS = None

    def _to_dto(self, row):
        return self.DTO_CLASS(**dict(row))

    def _to_dict(self, dto) -> dict[str, Any]:
        return dto.__dict__.copy()

    def get_all(self):
        rows = self.fetch_all(f"SELECT * FROM {self.TABLE}")
        return [self._to_dto(row) for row in rows]

    def get_by_id(self, id_value: int):
        row = self.fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE {self.PK} = ?",
            (id_value,),
        )
        return self._to_dto(row) if row else None

    def create(self, dto) -> bool:
        data = self._to_dict(dto)
        data.pop(self.PK, None)

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))

        query = f"""
        INSERT INTO {self.TABLE} ({columns})
        VALUES ({placeholders})
        """

        return self.execute(query, tuple(data.values()))

    def update(self, dto) -> bool:
        data = self._to_dict(dto)
        pk_value = data.pop(self.PK)

        assignments = ", ".join([f"{column}=?" for column in data.keys()])

        query = f"""
        UPDATE {self.TABLE}
        SET {assignments}
        WHERE {self.PK}=?
        """

        return self.execute(query, tuple(data.values()) + (pk_value,))

    def delete(self, id_value: int) -> bool:
        return self.execute(
            f"DELETE FROM {self.TABLE} WHERE {self.PK}=?",
            (id_value,),
        )


class SQLiteEtudiantRepository(BaseSQLiteRepository):
    TABLE = "Etudiants"
    PK = "id_etudiant"
    DTO_CLASS = EtudiantDTO

    def find_by_email(self, email: str) -> EtudiantDTO | None:
        row = self.fetch_one(
            "SELECT * FROM Etudiants WHERE adresse_mail_etudiant=?",
            (email,),
        )
        return self._to_dto(row) if row else None


class SQLiteGestionnaireRepository(BaseSQLiteRepository):
    TABLE = "Gestionnaires"
    PK = "id_gestionnaire"
    DTO_CLASS = GestionnaireDTO

    def find_by_email(self, email: str) -> GestionnaireDTO | None:
        row = self.fetch_one(
            "SELECT * FROM Gestionnaires WHERE email_gestionnaire=?",
            (email,),
        )
        return self._to_dto(row) if row else None


class SQLiteMachineRepository(BaseSQLiteRepository):
    TABLE = "Machine"
    PK = "id_machine"
    DTO_CLASS = MachineDTO


class SQLiteMaterielRepository(BaseSQLiteRepository):
    TABLE = "Materiel"
    PK = "id_materiel"
    DTO_CLASS = MaterielDTO

    def get_stock_faible(self) -> list[MaterielDTO]:
        rows = self.fetch_all(
            "SELECT * FROM Materiel WHERE quantite_stock < stock_minimum"
        )
        return [self._to_dto(row) for row in rows]


class SQLiteReservationRepository(BaseSQLiteRepository):
    TABLE = "reserver"
    PK = "id_reservation"
    DTO_CLASS = ReservationDTO

    def find_by_machine_and_date(
        self,
        id_machine: int,
        date_reservation: str,
    ) -> list[ReservationDTO]:
        rows = self.fetch_all(
            """
            SELECT * FROM reserver
            WHERE id_machine=? AND date_reservation=?
            """,
            (id_machine, date_reservation),
        )
        return [self._to_dto(row) for row in rows]


class SQLiteEmpruntRepository(BaseSQLiteRepository):
    TABLE = "Emprunter"
    PK = "id_emprunt"
    DTO_CLASS = EmpruntDTO

    def find_emprunt_actif(
        self,
        id_etudiant: int,
        id_materiel: int,
    ) -> EmpruntDTO | None:
        row = self.fetch_one(
            """
            SELECT * FROM Emprunter
            WHERE id_etudiant=?
              AND id_materiel=?
              AND statut_emprunt IN ('EN_ATTENTE', 'VALIDE')
            """,
            (id_etudiant, id_materiel),
        )
        return self._to_dto(row) if row else None


class SQLiteFournisseurRepository(BaseSQLiteRepository):
    TABLE = "Fournisseur"
    PK = "id_fournisseur"
    DTO_CLASS = FournisseurDTO


class SQLiteCommandeRepository(BaseSQLiteRepository):
    TABLE = "Commandes"
    PK = "id_commande"
    DTO_CLASS = CommandeDTO


class SQLiteLigneCommandeRepository(BaseSQLiteRepository):
    TABLE = "Ligne_commande"
    PK = "id_ligne"
    DTO_CLASS = LigneCommandeDTO

    def find_by_commande(self, id_commande: int) -> list[LigneCommandeDTO]:
        rows = self.fetch_all(
            "SELECT * FROM Ligne_commande WHERE id_commande=?",
            (id_commande,),
        )
        return [self._to_dto(row) for row in rows]


class SQLiteMouvementStockRepository(BaseSQLiteRepository):
    TABLE = "Mouvement_stock"
    PK = "id_mouvement"
    DTO_CLASS = MouvementStockDTO

    def get_by_materiel(self, id_materiel: int) -> list[MouvementStockDTO]:
        rows = self.fetch_all(
            """
            SELECT * FROM Mouvement_stock
            WHERE id_materiel=?
            ORDER BY date_mouvement DESC
            """,
            (id_materiel,),
        )
        return [self._to_dto(row) for row in rows]


class SQLiteAlerteRepository(BaseSQLiteRepository):
    TABLE = "Alerte"
    PK = "id_alerte"
    DTO_CLASS = AlerteDTO