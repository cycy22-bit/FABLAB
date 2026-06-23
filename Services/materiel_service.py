from Models import MaterielDTO
from Services.protocols import IMaterielRepository


class MaterielService:

    def __init__(self, repository: IMaterielRepository):
        self.repository = repository

    def ajouter_materiel(self, materiel: MaterielDTO) -> bool:
        if materiel.nom_materiel.strip() == "":
            return False

        if materiel.quantite_stock < 0:
            return False

        if materiel.stock_minimum < 0:
            return False

        return self.repository.save(materiel)

    def afficher_materiels(self) -> list[MaterielDTO]:
        return self.repository.get_all()

    def supprimer_materiel(self, materiel_id: int) -> bool:
        if materiel_id <= 0:
            return False

        return self.repository.delete(materiel_id)