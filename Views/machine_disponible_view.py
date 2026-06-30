import flet as ft
from .components import title_text, card


class MachineDisponibleView:
    def __init__(self, page: ft.Page, machine_service):
        self.page = page
        self.machine_service = machine_service

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Machine")),
                ft.DataColumn(ft.Text("Type")),
                ft.DataColumn(ft.Text("Statut")),
                ft.DataColumn(ft.Text("Emplacement")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        return ft.Column(
            controls=[
                title_text("Machines disponibles"),
                card(
                    ft.Column(
                        controls=[
                            ft.Text("Liste des machines que l'étudiant peut réserver",
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
            machines = self.machine_service.get_all()

            for machine in machines:
                if str(getattr(machine, "statut", "")).lower() == "disponible":
                    self.table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(getattr(machine, "id_machine", "")))),
                                ft.DataCell(ft.Text(str(getattr(machine, "nom_machine", "")))),
                                ft.DataCell(ft.Text(str(getattr(machine, "type_machine", "")))),
                                ft.DataCell(ft.Text(str(getattr(machine, "statut", "")))),
                                ft.DataCell(ft.Text(str(getattr(machine, "emplacement", "")))),
                            ]
                        )
                    )

        except Exception as ex:
            print("Erreur MachineDisponibleView :", ex)