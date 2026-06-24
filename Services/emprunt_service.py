from Models import EmpruntDTO
from Services.protocols import IEmpruntRepository, IMaterielRepository


class EmpruntService:

    def __init__(
        self,
        emprunt_repository: IEmpruntRepository,
        materiel_repository: IMaterielRepository
    ):
        self.emprunt_repository = emprunt_repository
        self.materiel_repository = materiel_repository

    def enregistrer_emprunt(self, emprunt: EmpruntDTO) -> bool:
        if emprunt.id_etudiant <= 0:
            return False

        if emprunt.id_materiel <= 0:
            return False

        if emprunt.quantite_empruntee <= 0:
            return False

        if emprunt.date_retour_prevue <= emprunt.date_emprunt:
            return False

        materiel = self.materiel_repository.get_by_id(emprunt.id_materiel)

        if materiel is None:
            return False

        if materiel.quantite_stock < emprunt.quantite_empruntee:
            return False

        nouveau_stock = materiel.quantite_stock - emprunt.quantite_empruntee

        emprunt_enregistre = self.emprunt_repository.save(emprunt)

        if emprunt_enregistre:
            self.materiel_repository.update_stock(
                emprunt.id_materiel,
                nouveau_stock
            )

        return emprunt_enregistre

    def afficher_emprunts(self) -> list[EmpruntDTO]:
        return self.emprunt_repository.get_all()

    def changer_statut(self, emprunt_id: int, statut: str) -> bool:
        if emprunt_id <= 0:
            return False

        if statut.strip() == "":
            return False

        return self.emprunt_repository.update_status(emprunt_id, statut)

    def supprimer_emprunt(self, emprunt_id: int) -> bool:
        if emprunt_id <= 0:
            return False

        return self.emprunt_repository.delete(emprunt_id)