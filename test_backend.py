from Models import MaterielDTO
from Services import MaterielService
from Repositories import SQLiteMaterielRepository


repository = SQLiteMaterielRepository(database_path="database.db")
service = MaterielService(repository=repository)

materiel = MaterielDTO(
    id_materiel=None,
    nom_materiel="Arduino Uno",
    categorie="Électronique",
    quantite_stock=10,
    stock_minimum=2
)

resultat = service.ajouter_materiel(materiel)

print("Ajout réussi :", resultat)

materiels = service.afficher_materiels()

for item in materiels:
    print(item)

from datetime import date

from Models import EmpruntDTO
from Services import EmpruntService
from Repositories import SQLiteEmpruntRepository


emprunt_repository = SQLiteEmpruntRepository(
    database_path="database.db"
)

emprunt_service = EmpruntService(
    repository=emprunt_repository
)

emprunt = EmpruntDTO(
    id_emprunt=None,
    id_etudiant=1,
    id_materiel=1,
    quantite=2,
    date_emprunt=date.today(),
    date_retour_prevue=date.today(),
    statut_emprunt="en cours"
)

resultat = emprunt_service.enregistrer_emprunt(emprunt)

print("Emprunt enregistré :", resultat)

for item in emprunt_service.afficher_emprunts():
    print(item)