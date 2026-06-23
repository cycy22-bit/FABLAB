from Models import EmpruntDTO
from Services.protocols import IEmpruntRepository


class EmpruntService:

    def __init__(self, repository: IEmpruntRepository):
        self.repository = repository

    def enregistrer_emprunt(self, emprunt: EmpruntDTO) -> bool:
        if emprunt.id_etudiant <= 0:
            return False

        if emprunt.id_materiel <= 0:
            return False

        if emprunt.quantite <= 0:
            return False

        return self.repository.save(emprunt)

    def afficher_emprunts(self) -> list[EmpruntDTO]:
        return self.repository.get_all()

    def changer_statut(self, emprunt_id: int, statut: str) -> bool:
        if emprunt_id <= 0:
            return False

        if statut.strip() == "":
            return False

        return self.repository.update_status(emprunt_id, statut)

    def supprimer_emprunt(self, emprunt_id: int) -> bool:
        if emprunt_id <= 0:
            return False

        return self.repository.delete(emprunt_id)