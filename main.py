import flet as ft

from Views.login_view import LoginView
from Views.home_view import MainScreen
from Services.service_auth import AuthService


class FakeService:
    """
    Service temporaire pour éviter que l'application plante
    tant que les vrais services ne sont pas encore branchés.
    À remplacer progressivement par les vrais services.
    """

    def get_all(self):
        return []

    def consulter_inventaire(self):
        return []

    def find_by_etudiant(self, id_etudiant: int):
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
    page.window_width = 1200
    page.window_height = 760
    page.window_min_width = 950
    page.window_min_height = 650

    auth_service = AuthService()

    stock_service = FakeService()
    emprunt_service = FakeService()
    alerte_service = FakeService()
    machine_service = FakeService()
    reservation_service = FakeService()
    fournisseur_service = FakeService()
    commande_service = FakeService()
    historique_service = FakeService()
    statistique_service = FakeService()

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

        if not isinstance(user, dict):
            page.add(ft.Text("Erreur : l'utilisateur connecté doit être un dictionnaire."))
            page.update()
            return

        if "role" not in user:
            page.add(ft.Text("Erreur : rôle utilisateur introuvable."))
            page.update()
            return

        main_screen = MainScreen(
            page=page,
            user=user,
            stock_service=stock_service,
            emprunt_service=emprunt_service,
            alerte_service=alerte_service,
            machine_service=machine_service,
            reservation_service=reservation_service,
            fournisseur_service=fournisseur_service,
            commande_service=commande_service,
            historique_service=historique_service,
            statistique_service=statistique_service,
        )

        page.add(main_screen.build())
        page.update()

    def route_change(e):
        if page.route == "/login":
            show_login()

    page.on_route_change = route_change
    show_login()


if __name__ == "__main__":
    ft.run(main)