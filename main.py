import flet as ft

from Views.login_view import LoginView
from Views.home_view import MainScreen
from Services.service_auth import AuthService


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
    page.title = "SG-FabLab"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    auth_service = AuthService()
    fake_service = FakeService()

    def show_login():
        page.controls.clear()

        login_view = LoginView(
            page=page,
            auth_service=auth_service,
            on_login_success=show_home,
        )

        page.add(login_view.build())
        page.update()

    def show_home(user):
        page.controls.clear()

        main_screen = MainScreen(
            page=page,
            user=user,
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

    def route_change(e):
        if page.route == "/login":
            show_login()

    page.on_route_change = route_change

    show_login()


if __name__ == "__main__":
    ft.app(target=main)