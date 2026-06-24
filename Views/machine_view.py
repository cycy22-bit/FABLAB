import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class MachineView:
    def __init__(self, page: ft.Page, machine_service):
        self.page = page
        self.machine_service = machine_service

        self.nom_field = input_field("Nom de la machine")
        self.type_field = input_field("Type de machine")
        self.description_field = input_field("Description")
        self.caracteristiques_field = input_field("Caractéristiques techniques")
        self.emplacement_field = input_field("Emplacement")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nom")),
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
                title_text("Gestion des machines"),

                card(
                    ft.Column(
                        controls=[
                            self.nom_field,
                            self.type_field,
                            self.description_field,
                            self.caracteristiques_field,
                            self.emplacement_field,
                            primary_button("Ajouter machine", self.on_save_clicked, ft.Icons.ADD),
                        ],
                        spacing=10,
                    )
                ),

                card(
                    ft.Column(
                        controls=[
                            ft.Text("Catalogue des machines", size=18, weight=ft.FontWeight.BOLD),
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
        except Exception:
            pass

    def on_save_clicked(self, e):
        try:
            result = self.machine_service.create(
                nom_machine=self.nom_field.value,
                type_machine=self.type_field.value,
                description=self.description_field.value,
                caracteristiques_techniques=self.caracteristiques_field.value,
                emplacement=self.emplacement_field.value,
            )

            if result:
                notify(self.page, "Machine ajoutée avec succès.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Ajout impossible.", False)

        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)