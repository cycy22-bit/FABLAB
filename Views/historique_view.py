import flet as ft
from .components import title_text, card


class HistoriqueView:
    def __init__(self, page: ft.Page, historique_service):
        self.page = page
        self.historique_service = historique_service

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Type mouvement")),
                ft.DataColumn(ft.Text("Matériel")),
                ft.DataColumn(ft.Text("Quantité")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Référence")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        return ft.Column(
            controls=[
                title_text("Historique des mouvements de stock"),

                card(
                    ft.Column(
                        controls=[
                            ft.Text("Emprunts, retours, approvisionnements et ajustements",
                                    size=18,
                                    weight=ft.FontWeight.BOLD),
                            self.table,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            ],
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh_table(self):
        self.table.rows.clear()

        try:
            mouvements = self.historique_service.get_all()

            for mouvement in mouvements:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(mouvement, "id_mouvement", "")))),
                            ft.DataCell(ft.Text(str(getattr(mouvement, "type_mouvement", "")))),
                            ft.DataCell(ft.Text(str(getattr(mouvement, "id_materiel", "")))),
                            ft.DataCell(ft.Text(str(getattr(mouvement, "quantite", "")))),
                            ft.DataCell(ft.Text(str(getattr(mouvement, "date_mouvement", "")))),
                            ft.DataCell(ft.Text(str(getattr(mouvement, "id_reference", "")))),
                        ]
                    )
                )
        except Exception:
            pass