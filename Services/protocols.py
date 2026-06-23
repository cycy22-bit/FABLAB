from typing import Protocol

from Models import (
    MaterielDTO,
    EmpruntDTO
)
class IMaterielRepository(Protocol):

    def get_all(self) -> list[MaterielDTO]:
        pass

    def save(self, materiel: MaterielDTO) -> bool:
        pass

    def delete(self, materiel_id: int) -> bool:
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

