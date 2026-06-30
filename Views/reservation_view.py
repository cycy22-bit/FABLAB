import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class ReservationView:
    def __init__(self, page: ft.Page, reservation_service, user: dict):
        self.page = page
        self.reservation_service = reservation_service
        self.user = user
        self.role = self.user.get("role", "").upper()

        self.id_etudiant_field = input_field("ID étudiant")
        self.id_machine_field = input_field("ID machine")
        self.date_field = input_field("Date réservation : AAAA-MM-JJ")
        self.heure_debut_field = input_field("Heure début : HH:MM")
        self.heure_fin_field = input_field("Heure fin : HH:MM")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Étudiant")),
                ft.DataColumn(ft.Text("Machine")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Début")),
                ft.DataColumn(ft.Text("Fin")),
                ft.DataColumn(ft.Text("Statut")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        controls = [
            title_text(
                "Liste des réservations"
                if self.role == "GESTIONNAIRE"
                else "Mes réservations"
            )
        ]

        # Le formulaire n'est visible que pour l'étudiant
        if self.role == "ETUDIANT":
            controls.append(
                card(
                    ft.Column(
                        controls=[
                            self.id_machine_field,
                            self.date_field,
                            self.heure_debut_field,
                            self.heure_fin_field,
                            primary_button(
                                "Réserver machine",
                                self.on_reserver_clicked,
                                ft.Icons.CALENDAR_MONTH,
                            ),
                        ],
                        spacing=10,
                    )
                )
            )

        controls.append(
            card(
                ft.Column(
                    controls=[
                        ft.Text(
                            "Liste des réservations",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        self.table,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        )

        return ft.Column(
            controls=controls,
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def refresh_table(self):
        self.table.rows.clear()

        try:
            if self.role == "ETUDIANT" and hasattr(self.reservation_service, "find_by_etudiant"):
                reservations = self.reservation_service.find_by_etudiant(self.user.get("id"))
            else:
                reservations = self.reservation_service.get_all()

            for reservation in reservations:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(reservation, "id_reservation", "")))),
                            ft.DataCell(ft.Text(str(getattr(reservation, "id_etudiant", "")))),
                            ft.DataCell(ft.Text(str(getattr(reservation, "id_machine", "")))),
                            ft.DataCell(ft.Text(str(getattr(reservation, "date_reservation", "")))),
                            ft.DataCell(ft.Text(str(getattr(reservation, "heure_debut", "")))),
                            ft.DataCell(ft.Text(str(getattr(reservation, "heure_fin", "")))),
                            ft.DataCell(ft.Text(str(getattr(reservation, "statut_reservation", "")))),
                        ]
                    )
                )
        except Exception as ex:
            notify(self.page, f"Erreur de chargement des réservations : {ex}", False)

    def on_reserver_clicked(self, e):
        try:
            if self.role == "ETUDIANT":
                id_etudiant = int(self.user.get("id"))
            else:
                id_etudiant = int(self.id_etudiant_field.value)

            result = self.reservation_service.reserver_machine(
                id_etudiant=id_etudiant,
                id_machine=int(self.id_machine_field.value),
                date_reservation=self.date_field.value,
                heure_debut=self.heure_debut_field.value,
                heure_fin=self.heure_fin_field.value,
            )

            if result:
                notify(self.page, "Réservation enregistrée.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Réservation refusée.", False)

        except ValueError:
            notify(self.page, "Les ID doivent être numériques.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)