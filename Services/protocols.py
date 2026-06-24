from typing import Protocol

from Models import (
    MaterielDTO,
    EmpruntDTO,
    EtudiantDTO,
    ReservationDTO,
    MachineDTO,
    AlerteDTO,
    MouvementStockDTO,
)

class IMaterielRepository(Protocol):

    def get_all(self) -> list[MaterielDTO]:
        pass

    def save(self, materiel: MaterielDTO) -> bool:
        pass

    def delete(self, materiel_id: int) -> bool:
        pass
    def get_by_id(self, materiel_id: int) -> MaterielDTO | None:
        pass

    def update_stock(self, materiel_id: int, nouvelle_quantite: int) -> bool:
        pass

class IEmpruntRepository(Protocol):

    def get_all(self) -> list[EmpruntDTO]:
        pass

    def save(self, emprunt: EmpruntDTO) -> bool:
        pass

    def update_status(self, emprunt_id: int, statut: str) -> bool:
        pass

    def delete(self, emprunt_id: int) -> bool:
        pass

class IEtudiantRepository(Protocol):

    def get_by_email(self, email: str) -> EtudiantDTO | None:
        pass

    def save(self, etudiant: EtudiantDTO) -> bool:
        pass


class IMachineRepository(Protocol):

    def get_all(self) -> list[MachineDTO]:
        pass

    def get_by_id(self, machine_id: int) -> MachineDTO | None:
        pass


class IReservationRepository(Protocol):

    def get_all(self) -> list[ReservationDTO]:
        pass

    def save(self, reservation: ReservationDTO) -> bool:
        pass

    def delete(self, reservation_id: int) -> bool:
        pass


class IAlerteRepository(Protocol):

    def get_all(self) -> list[AlerteDTO]:
        pass

    def save(self, alerte: AlerteDTO) -> bool:
        pass


class IMouvementStockRepository(Protocol):

    def get_all(self) -> list[MouvementStockDTO]:
        pass

    def save(self, mouvement: MouvementStockDTO) -> bool:
        pass

