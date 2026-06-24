import flet as ft
from .components import title_text, subtitle_text, card


class DashboardView:
    def __init__(self, page: ft.Page, statistique_service=None):
        self.page = page
        self.statistique_service = statistique_service

    def build(self) -> ft.Control:
        return ft.Column(
            controls=[
                title_text("Tableau de bord"),
                subtitle_text("Vue générale de l'activité du FabLab"),

                ft.Row(
                    controls=[
                        self._stat_card("Machines", "Disponibilité et réservations", ft.Icons.PRECISION_MANUFACTURING),
                        self._stat_card("Stock", "Inventaire des matériels", ft.Icons.INVENTORY),
                        self._stat_card("Emprunts", "Demandes et retours", ft.Icons.ASSIGNMENT),
                        self._stat_card("Alertes", "Stock faible et retards", ft.Icons.WARNING),
                    ],
                    spacing=20,
                    wrap=True,
                ),
            ],
            spacing=25,
            expand=True,
        )

    def _stat_card(self, title: str, description: str, icon) -> ft.Container:
        return card(
            ft.Column(
                controls=[
                    ft.Icon(icon, size=35, color="#1E88E5"),
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(description, size=13, color="#666666"),
                ],
                spacing=10,
            ),
            width=230,
            height=150,
        )