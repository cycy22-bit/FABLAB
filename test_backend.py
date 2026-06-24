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