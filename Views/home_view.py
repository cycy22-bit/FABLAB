import flet as ft

from .components import BG_COLOR, PRIMARY_COLOR
from .dashboard_view import DashboardView
from .stock_view import StockView
from .emprunt_view import EmpruntView
from .alerte_view import AlerteView
from .machine_view import MachineView
from .reservation_view import ReservationView
from .fournisseur_view import FournisseurView
from .commande_view import CommandeView
from .historique_view import HistoriqueView


class MainScreen:
    def __init__(
        self,
        page: ft.Page,
        user,
        stock_service,
        emprunt_service,
        alerte_service,
        machine_service,
        reservation_service,
        fournisseur_service,
        commande_service,
        historique_service,
        statistique_service=None,
    ):
        self.page = page
        self.user = user

        self.stock_service = stock_service
        self.emprunt_service = emprunt_service
        self.alerte_service = alerte_service
        self.machine_service = machine_service
        self.reservation_service = reservation_service
        self.fournisseur_service = fournisseur_service
        self.commande_service = commande_service
        self.historique_service = historique_service
        self.statistique_service = statistique_service

        self.content_area = ft.Container(expand=True, padding=25)

    def build(self) -> ft.Control:
        self.show_dashboard()

        return ft.Row(
            controls=[
                self.sidebar(),
                ft.Container(
                    content=self.content_area,
                    expand=True,
                    bgcolor=BG_COLOR,
                ),
            ],
            expand=True,
        )

    def sidebar(self) -> ft.Container:
        return ft.Container(
            width=260,
            bgcolor="white",
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("SG-FabLab", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    ft.Text("Système de gestion", size=12, color="#666666"),
                    ft.Divider(),

                    ft.TextButton(
                        text="Tableau de bord",
                        icon=ft.Icons.DASHBOARD,
                        on_click=lambda e: self.show_dashboard(),
                    ),
                    ft.TextButton(
                        text="Machines",
                        icon=ft.Icons.PRECISION_MANUFACTURING,
                        on_click=lambda e: self.show_machines(),
                    ),
                    ft.TextButton(
                        text="Réservations",
                        icon=ft.Icons.CALENDAR_MONTH,
                        on_click=lambda e: self.show_reservations(),
                    ),
                    ft.TextButton(
                        text="Inventaire / Stock",
                        icon=ft.Icons.INVENTORY,
                        on_click=lambda e: self.show_stock(),
                    ),
                    ft.TextButton(
                        text="Emprunts",
                        icon=ft.Icons.ASSIGNMENT,
                        on_click=lambda e: self.show_emprunts(),
                    ),
                    ft.TextButton(
                        text="Fournisseurs",
                        icon=ft.Icons.BUSINESS,
                        on_click=lambda e: self.show_fournisseurs(),
                    ),
                    ft.TextButton(
                        text="Commandes",
                        icon=ft.Icons.SHOPPING_CART,
                        on_click=lambda e: self.show_commandes(),
                    ),
                    ft.TextButton(
                        text="Historique",
                        icon=ft.Icons.HISTORY,
                        on_click=lambda e: self.show_historique(),
                    ),
                    ft.TextButton(
                        text="Alertes",
                        icon=ft.Icons.WARNING,
                        on_click=lambda e: self.show_alertes(),
                    ),

                    ft.Container(expand=True),

                    ft.TextButton(
                        text="Déconnexion",
                        icon=ft.Icons.LOGOUT,
                        on_click=lambda e: self.page.go("/login"),
                    ),
                ],
                spacing=6,
            ),
        )

    def set_content(self, control: ft.Control):
        self.content_area.content = control
        self.page.update()

    def show_dashboard(self):
        self.set_content(
            DashboardView(
                page=self.page,
                statistique_service=self.statistique_service,
            ).build()
        )

    def show_machines(self):
        self.set_content(
            MachineView(
                page=self.page,
                machine_service=self.machine_service,
            ).build()
        )

    def show_reservations(self):
        self.set_content(
            ReservationView(
                page=self.page,
                reservation_service=self.reservation_service,
            ).build()
        )

    def show_stock(self):
        self.set_content(
            StockView(
                page=self.page,
                stock_service=self.stock_service,
            ).build()
        )

    def show_emprunts(self):
        self.set_content(
            EmpruntView(
                page=self.page,
                emprunt_service=self.emprunt_service,
            ).build()
        )

    def show_fournisseurs(self):
        self.set_content(
            FournisseurView(
                page=self.page,
                fournisseur_service=self.fournisseur_service,
            ).build()
        )

    def show_commandes(self):
        self.set_content(
            CommandeView(
                page=self.page,
                commande_service=self.commande_service,
            ).build()
        )

    def show_historique(self):
        self.set_content(
            HistoriqueView(
                page=self.page,
                historique_service=self.historique_service,
            ).build()
        )

    def show_alertes(self):
        self.set_content(
            AlerteView(
                page=self.page,
                alerte_service=self.alerte_service,
            ).build()
        )

    def on_save_clicked(self, e):
        pass