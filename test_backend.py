from datetime import date, timedelta

from Models import MaterielDTO, EmpruntDTO
from Services import MaterielService, EmpruntService
from Repositories import SQLiteMaterielRepository, SQLiteEmpruntRepository


materiel_repository = SQLiteMaterielRepository(database_path="database.db")
emprunt_repository = SQLiteEmpruntRepository(database_path="database.db")

materiel_service = MaterielService(repository=materiel_repository)

emprunt_service = EmpruntService(
    emprunt_repository=emprunt_repository,
    materiel_repository=materiel_repository
)

materiel = MaterielDTO(
    id_materiel=None,
    nom_materiel="Arduino Uno",
    categorie="Électronique",
    quantite_stock=10,
    stock_minimum=2
)

resultat_materiel = materiel_service.ajouter_materiel(materiel)

print("Ajout matériel réussi :", resultat_materiel)

print("\nListe des matériels :")
for item in materiel_service.afficher_materiels():
    print(item)

emprunt = EmpruntDTO(
    id_emprunt=None,
    id_etudiant=1,
    id_materiel=1,
    quantite_empruntee=2,
    date_emprunt=date.today(),
    date_retour_prevue=date.today() + timedelta(days=7),
    date_retour_effective=None,
    statut_emprunt="en cours",
    etat_retour="non retourné"
)

resultat_emprunt = emprunt_service.enregistrer_emprunt(emprunt)

print("\nEmprunt enregistré :", resultat_emprunt)

print("\nListe des emprunts :")
for item in emprunt_service.afficher_emprunts():
    print(item)

print("\nStock après emprunt :")
materiel_apres_emprunt = materiel_repository.get_by_id(1)
print(materiel_apres_emprunt)