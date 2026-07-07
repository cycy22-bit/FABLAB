import flet as ft
from .components import title_text, input_field, primary_button, card, notify, show_popup


class ReservationView:
    def __init__(self, page: ft.Page, reservation_service, user: dict, machine_service=None, mode="liste"):
        self.page = page
        self.reservation_service = reservation_service
        self.machine_service = machine_service
        self.user = user
        self.mode = mode
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

        self.machine_table = ft.DataTable(
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
        controls = []

        if self.role == "GESTIONNAIRE":
            self.refresh_table()
            controls.append(title_text("Demandes de réservation"))
            controls.append(self._reservations_card())
            return self._page(controls)

        if self.mode == "demande":
            self.refresh_machine_table()
            controls.append(title_text("Réserver une machine"))
            controls.append(self._form_card())
            controls.append(self._machines_card())
            return self._page(controls)

        self.refresh_table()
        controls.append(title_text("Mes réservations"))
        controls.append(self._reservations_card())
        return self._page(controls)

    def _page(self, controls):
        return ft.Column(
            controls=controls,
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _form_card(self):
        return card(
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

    def _machines_card(self):
        return card(
            ft.Column(
                controls=[
                    ft.Text("Machines disponibles", size=18, weight=ft.FontWeight.BOLD),
                    self.machine_table,
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        )

    def _reservations_card(self):
        return card(
            ft.Column(
                controls=[
                    ft.Text("Liste des réservations", size=18, weight=ft.FontWeight.BOLD),
                    self.table,
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        )

    def refresh_machine_table(self):
        self.machine_table.rows.clear()

        try:
            if self.machine_service is None:
                return

            machines = self.machine_service.get_all()

            for machine in machines:
                statut = str(getattr(machine, "statut", "")).lower()

                if statut == "disponible":
                    self.machine_table.rows.append(
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
            notify(self.page, f"Erreur de chargement des machines : {ex}", False)

    def refresh_table(self):
        self.table.rows.clear()

        try:
            if self.role == "ETUDIANT":
                reservations = self.reservation_service.find_by_etudiant(self.user.get("id"))
            else:
                reservations = self.reservation_service.get_all()

            for reservation in reservations:
                statut = str(getattr(reservation, "statut_reservation", ""))

                cells = [
                    ft.DataCell(ft.Text(str(getattr(reservation, "id_reservation", "")))),
                    ft.DataCell(ft.Text(str(getattr(reservation, "nom_etudiant", getattr(reservation, "id_etudiant", ""))))),
                    ft.DataCell(ft.Text(str(getattr(reservation, "nom_machine", getattr(reservation, "id_machine", ""))))),
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
            id_machine = int(self.id_machine_field.value)
            date_reservation = self.date_field.value.strip()
            heure_debut = self.heure_debut_field.value.strip()
            heure_fin = self.heure_fin_field.value.strip()

            result = self.reservation_service.reserver_machine(
                id_etudiant=id_etudiant,
                id_machine=id_machine,
                date_reservation=date_reservation,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
            )

            if result:
                show_popup(
                    self.page,
                    "Détails de la réservation",
                    f"Votre demande de réservation de la machine n°{id_machine} a été enregistrée.\n\n"
                    f"Date : {date_reservation}\n"
                    f"Heure : {heure_debut} - {heure_fin}\n\n"
                    "Elle est maintenant en attente de validation par le gestionnaire.",
                    "en attente",
                    True,
                )

                self.id_machine_field.value = ""
                self.date_field.value = ""
                self.heure_debut_field.value = ""
                self.heure_fin_field.value = ""
                self.refresh_machine_table()
                self.page.update()
            else:
                show_popup(
                    self.page,
                    "Détails de la réservation",
                    "Votre demande de réservation a été rejetée.\n\n"
                    "Ce créneau est déjà occupé ou la machine n'est pas disponible.",
                    "rejeté",
                    False,
                )

        except ValueError:
            show_popup(
                self.page,
                "Détails de la réservation",
                "L'ID machine doit être un nombre valide.",
                "rejeté",
                False,
            )
        except Exception as ex:
            show_popup(self.page, "Erreur système", f"Une erreur est survenue : {ex}", "erreur", False)

    def on_accepter_clicked(self, id_reservation):
        try:
            result = self.reservation_service.accepter_reservation(id_reservation)

            if result:
                show_popup(
                    self.page,
                    "Détails de la réservation",
                    f"La réservation n°{id_reservation} a été acceptée.",
                    "acceptée",
                    True,
                )
                self.refresh_table()
                self.page.update()
            else:
                show_popup(
                    self.page,
                    "Détails de la réservation",
                    f"Impossible d'accepter la réservation n°{id_reservation}.\n\n"
                    "Elle est peut-être déjà traitée.",
                    "erreur",
                    False,
                )

        except Exception as ex:
            show_popup(self.page, "Erreur système", f"Une erreur est survenue : {ex}", "erreur", False)

    def on_refuser_clicked(self, id_reservation):
        try:
            result = self.reservation_service.refuser_reservation(id_reservation)

            if result:
                show_popup(
                    self.page,
                    "Détails de la réservation",
                    f"La réservation n°{id_reservation} a été refusée.",
                    "rejetée",
                    False,
                )
                self.refresh_table()
                self.page.update()
            else:
                show_popup(
                    self.page,
                    "Détails de la réservation",
                    f"Impossible de refuser la réservation n°{id_reservation}.\n\n"
                    "Elle est peut-être déjà traitée.",
                    "erreur",
                    False,
                )

        except Exception as ex:
            show_popup(self.page, "Erreur système", f"Une erreur est survenue : {ex}", "erreur", False)