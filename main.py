import flet as ft
from Views.home_view import MainScreen


class FakeService:
    def get_all(self):
        return []

    def consulter_inventaire(self):
        return []

    def ajouter_materiel(self, **kwargs):
        print("Ajout matériel :", kwargs)
        return True

    def emprunter_materiel(self, **kwargs):
        print("Emprunt :", kwargs)
        return True

    def reserver_machine(self, **kwargs):
        print("Réservation :", kwargs)
        return True

    def create(self, **kwargs):
        print("Création :", kwargs)
        return True

    def creer_commande(self, **kwargs):
        print("Commande :", kwargs)
        return True


def main(page: ft.Page):
    print("Application SG-FabLab lancée")

    page.title = "SG-FabLab"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    fake_service = FakeService()

    main_screen = MainScreen(
        page=page,
        user={"nom": "Jessika", "role": "Gestionnaire"},
        stock_service=fake_service,
        emprunt_service=fake_service,
        alerte_service=fake_service,
        machine_service=fake_service,
        reservation_service=fake_service,
        fournisseur_service=fake_service,
        commande_service=fake_service,
        historique_service=fake_service,
        statistique_service=fake_service,
    )

    page.add(main_screen.build())
    page.update()

if __name__ == "__main__":
    ft.app(target=main)