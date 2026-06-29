from Repositories.Sqlite_repo import SQLiteRepository
from Models.reservation import ReservationDTO


class SQLiteReservationRepository(SQLiteRepository):
    TABLE = "Reservations"
    PK = "id_reservation"
    DTO_CLASS = ReservationDTO

    def find_by_machine_and_date(
        self,
        id_machine: int,
        date_reservation: str
    ) -> list[ReservationDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Reservations
            WHERE id_machine = ?
            AND date_reservation = ?
            """,
            (id_machine, date_reservation),
        )
        return [self._to_dto(row) for row in rows]

    def find_by_etudiant(self, id_etudiant: int) -> list[ReservationDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Reservations
            WHERE id_etudiant = ?
            ORDER BY date_reservation DESC, heure_debut DESC
            """,
            (id_etudiant,),
        )
        return [self._to_dto(row) for row in rows]

    def find_actives_by_etudiant(self, id_etudiant: int) -> list[ReservationDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Reservations
            WHERE id_etudiant = ?
            AND statut_reservation IN ('en attente', 'validée', 'active')
            ORDER BY date_reservation ASC, heure_debut ASC
            """,
            (id_etudiant,),
        )
        return [self._to_dto(row) for row in rows]

    def find_overlapping_reservations(
        self,
        id_machine: int,
        date_reservation: str,
        heure_debut: str,
        heure_fin: str
    ) -> list[ReservationDTO]:
        rows = self.fetch_all(
            """
            SELECT *
            FROM Reservations
            WHERE id_machine = ?
            AND date_reservation = ?
            AND statut_reservation IN ('en attente', 'validée', 'active')
            AND NOT (
                heure_fin <= ?
                OR heure_debut >= ?
            )
            """,
            (id_machine, date_reservation, heure_debut, heure_fin),
        )
        return [self._to_dto(row) for row in rows]