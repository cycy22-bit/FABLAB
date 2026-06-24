import flet as ft
from .components import title_text, card


class AlerteView:
    def __init__(self, page: ft.Page, alerte_service):
        self.page = page
        self.alerte_service = alerte_service

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Type")),
                ft.DataColumn(ft.Text("Message")),
                ft.DataColumn(ft.Text("Date")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        return ft.Column(
            controls=[
                title_text("Alertes du système"),

                card(
                    ft.Column(
                        controls=[
                            ft.Text("Stock faible, retards et notifications", size=18, weight=ft.FontWeight.BOLD),
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
            alertes = self.alerte_service.get_all()

            for alerte in alertes:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(alerte, "id_alerte", "")))),
                            ft.DataCell(ft.Text(str(getattr(alerte, "type_alerte", "")))),
                            ft.DataCell(ft.Text(str(getattr(alerte, "message_alerte", "")))),
                            ft.DataCell(ft.Text(str(getattr(alerte, "date_alerte", "")))),
                        ]
                    )
                )

        except Exception:
            pass