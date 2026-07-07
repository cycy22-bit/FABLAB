import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class ReservationView:
    def __init__(self, page: ft.Page, reservation_service, user: dict):
        self.page = page
        self.reservation_service = reservation_service
        self.user = user
        self.role = self.user.get("role", "").upper()

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
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        controls = [
            title_text(
                "Demandes de réservation"
                if self.role == "GESTIONNAIRE"
                else "Mes réservations"
            )
        ]

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
                statut = str(getattr(reservation, "statut_reservation", ""))

                cells = [
                    ft.DataCell(ft.Text(str(getattr(reservation, "id_reservation", "")))),
                    ft.DataCell(
                        ft.Text(
                            str(
                                getattr(
                                    reservation,
                                    "nom_etudiant",
                                    getattr(reservation, "id_etudiant", ""),
                                )
                            )
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(
                                getattr(
                                    reservation,
                                    "nom_machine",
                                    getattr(reservation, "id_machine", ""),
                                )
                            )
                        )
                    ),
                    ft.DataCell(ft.Text(str(getattr(reservation, "date_reservation", "")))),
                    ft.DataCell(ft.Text(str(getattr(reservation, "heure_debut", "")))),
                    ft.DataCell(ft.Text(str(getattr(reservation, "heure_fin", "")))),
                    ft.DataCell(ft.Text(statut)),
                ]

                if self.role == "GESTIONNAIRE" and statut == "en attente":
                    id_reservation = getattr(reservation, "id_reservation", None)

                    cells.append(
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.TextButton(
                                        "Accepter",
                                        on_click=lambda e, rid=id_reservation: self.on_accepter_clicked(rid),
                                    ),
                                    ft.TextButton(
                                        "Refuser",
                                        on_click=lambda e, rid=id_reservation: self.on_refuser_clicked(rid),
                                    ),
                                ],
                                spacing=5,
                            )
                        )
                    )
                else:
                    cells.append(ft.DataCell(ft.Text("-")))

                self.table.rows.append(ft.DataRow(cells=cells))

        except Exception as ex:
            notify(self.page, f"Erreur de chargement des réservations : {ex}", False)

    def on_reserver_clicked(self, e):
        try:
            id_etudiant = int(self.user.get("id"))

            result = self.reservation_service.reserver_machine(
                id_etudiant=id_etudiant,
                id_machine=int(self.id_machine_field.value),
                date_reservation=self.date_field.value,
                heure_debut=self.heure_debut_field.value,
                heure_fin=self.heure_fin_field.value,
            )

            if result:
                notify(self.page, "Réservation enregistrée. En attente de validation.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Réservation refusée : créneau déjà occupé.", False)

        except ValueError:
            notify(self.page, "Les ID doivent être numériques.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def on_accepter_clicked(self, id_reservation):
        try:
            result = self.reservation_service.accepter_reservation(id_reservation)

            if result:
                notify(self.page, "Réservation acceptée.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Impossible d'accepter cette réservation.", False)

        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def on_refuser_clicked(self, id_reservation):
        try:
            result = self.reservation_service.refuser_reservation(id_reservation)

            if result:
                notify(self.page, "Réservation refusée.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Impossible de refuser cette réservation.", False)

        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)