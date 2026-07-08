import flet as ft

from .components import BG_COLOR, PRIMARY_COLOR, DARK_COLOR, logo_ulc_icam
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
        self.content_area.content = DashboardView(
            page=self.page,
            user=self.user,
            emprunt_service=self.emprunt_service,
            reservation_service=self.reservation_service,
            stock_service=self.stock_service,
            alerte_service=self.alerte_service,
            statistique_service=self.statistique_service,
        ).build()

        return ft.Row(
            controls=[
                self.sidebar(),
                ft.Container(content=self.content_area, expand=True, bgcolor=BG_COLOR),
            ],
            expand=True,
        )

    def sidebar(self) -> ft.Container:
        role = self.user.get("role", "").upper()
        nom = self.user.get("nom", "Utilisateur")

        def menu_button(label, icon, action):
            return ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(icon, size=20, color="white"),
                        ft.Text(label, color="white"),
                    ],
                    spacing=10,
                ),
                on_click=action,
                style=ft.ButtonStyle(
                    overlay_color="#1E88E533",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )

        menu_items = [
            menu_button("Tableau de bord", ft.Icons.DASHBOARD, lambda e: self.show_dashboard()),
        ]

        if role == "GESTIONNAIRE":
            menu_items += [
                menu_button("Machines", ft.Icons.PRECISION_MANUFACTURING, lambda e: self.show_machines()),
                menu_button("Demandes de réservation", ft.Icons.CALENDAR_MONTH, lambda e: self.show_reservations()),
                menu_button("Inventaire / Stock", ft.Icons.INVENTORY, lambda e: self.show_stock()),
                menu_button("Demandes d'emprunt", ft.Icons.ASSIGNMENT, lambda e: self.show_emprunts()),
                menu_button("Fournisseurs", ft.Icons.BUSINESS, lambda e: self.show_fournisseurs()),
                menu_button("Commandes", ft.Icons.SHOPPING_CART, lambda e: self.show_commandes()),
                menu_button("Historique", ft.Icons.HISTORY, lambda e: self.show_historique()),
                menu_button("Alertes", ft.Icons.WARNING, lambda e: self.show_alertes()),
            ]

        elif role == "ETUDIANT":
            menu_items += [
                menu_button("Réserver une machine", ft.Icons.CALENDAR_MONTH, lambda e: self.show_demande_reservation()),
                menu_button("Mes réservations", ft.Icons.EVENT_NOTE, lambda e: self.show_mes_reservations()),
                menu_button("Demander un emprunt", ft.Icons.ASSIGNMENT, lambda e: self.show_demande_emprunt()),
                menu_button("Mes emprunts", ft.Icons.LIST_ALT, lambda e: self.show_mes_emprunts()),
                menu_button("Alertes", ft.Icons.WARNING, lambda e: self.show_alertes()),
            ]

        menu_items.append(ft.Container(expand=True))
        menu_items.append(menu_button("Déconnexion", ft.Icons.LOGOUT, lambda e: self.logout()))

        return ft.Container(
            width=270,
            bgcolor=DARK_COLOR,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            logo_ulc_icam(58),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "SG-FabLab",
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                        color=PRIMARY_COLOR,
                                    ),
                                    ft.Text("ULC-ICAM", size=11, color="white"),
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(color="#1E88E555"),
                    ft.Text(f"{nom}", size=13, color="white"),
                    ft.Text(f"Rôle : {role}", size=12, color="#B0BEC5"),
                    ft.Divider(color="#1E88E555"),
                    *menu_items,
                ],
                spacing=7,
            ),
        )

    def logout(self):
        self.page.controls.clear()
        self.page.go("/login")
        self.page.update()

    def set_content(self, control: ft.Control):
        self.content_area.content = control
        self.page.update()

    def show_dashboard(self):
        self.set_content(
            DashboardView(
                page=self.page,
                user=self.user,
                emprunt_service=self.emprunt_service,
                reservation_service=self.reservation_service,
                stock_service=self.stock_service,
                alerte_service=self.alerte_service,
                statistique_service=self.statistique_service,
            ).build()
        )

    def show_machines(self):
        if self.user.get("role", "").upper() != "GESTIONNAIRE":
            return
        self.set_content(MachineView(page=self.page, machine_service=self.machine_service).build())

    def show_stock(self):
        if self.user.get("role", "").upper() != "GESTIONNAIRE":
            return
        self.set_content(StockView(page=self.page, stock_service=self.stock_service, readonly=False).build())

    def show_reservations(self):
        self.set_content(
            ReservationView(
                page=self.page,
                reservation_service=self.reservation_service,
                machine_service=self.machine_service,
                user=self.user,
                mode="liste",
            ).build()
        )

    def show_emprunts(self):
        self.set_content(
            EmpruntView(
                page=self.page,
                emprunt_service=self.emprunt_service,
                stock_service=self.stock_service,
                user=self.user,
                mode="liste",
            ).build()
        )

    def show_demande_reservation(self):
        self.set_content(
            ReservationView(
                page=self.page,
                reservation_service=self.reservation_service,
                machine_service=self.machine_service,
                user=self.user,
                mode="demande",
            ).build()
        )

    def show_mes_reservations(self):
        self.set_content(
            ReservationView(
                page=self.page,
                reservation_service=self.reservation_service,
                machine_service=self.machine_service,
                user=self.user,
                mode="liste",
            ).build()
        )

    def show_demande_emprunt(self):
        self.set_content(
            EmpruntView(
                page=self.page,
                emprunt_service=self.emprunt_service,
                stock_service=self.stock_service,
                user=self.user,
                mode="demande",
            ).build()
        )

    def show_mes_emprunts(self):
        self.set_content(
            EmpruntView(
                page=self.page,
                emprunt_service=self.emprunt_service,
                stock_service=self.stock_service,
                user=self.user,
                mode="liste",
            ).build()
        )

    def show_fournisseurs(self):
        if self.user.get("role", "").upper() != "GESTIONNAIRE":
            return
        self.set_content(FournisseurView(page=self.page, fournisseur_service=self.fournisseur_service).build())

    def show_commandes(self):
        if self.user.get("role", "").upper() != "GESTIONNAIRE":
            return
        self.set_content(CommandeView(page=self.page, commande_service=self.commande_service).build())

    def show_historique(self):
        if self.user.get("role", "").upper() != "GESTIONNAIRE":
            return
        self.set_content(HistoriqueView(page=self.page, historique_service=self.historique_service).build())

    def show_alertes(self):
        self.set_content(AlerteView(page=self.page, alerte_service=self.alerte_service).build())