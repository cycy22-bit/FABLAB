import flet as ft
from .components import PRIMARY_COLOR, WHITE, card


class DashboardView:
    def __init__(
        self,
        page: ft.Page,
        user: dict,
        emprunt_service=None,
        reservation_service=None,
        stock_service=None,
        alerte_service=None,
        statistique_service=None,
    ):
        self.page = page
        self.user = user
        self.emprunt_service = emprunt_service
        self.reservation_service = reservation_service
        self.stock_service = stock_service
        self.alerte_service = alerte_service
        self.statistique_service = statistique_service
        self.role = self.user.get("role", "").upper()

    def build(self) -> ft.Control:
        emprunts = self._get_emprunts()
        reservations = self._get_reservations()
        materiels = self._get_materiels()
        alertes = self._get_alertes()

        return ft.Column(
            controls=[
                self._top_title(),
                self._profile_card(),
                self._stats_row(len(reservations), len(emprunts), len(alertes), len(materiels)),
                self._main_tables(emprunts, reservations),
                self._info_card(),
            ],
            spacing=18,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _top_title(self):
        return ft.Row(
            controls=[
                ft.Container(
                    width=45,
                    height=45,
                    border_radius=12,
                    bgcolor="#EAF3FF",
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(ft.Icons.DASHBOARD, color=PRIMARY_COLOR, size=28),
                ),
                ft.Text("Tableau de bord", size=32, weight=ft.FontWeight.BOLD, color="#111827"),
            ],
            spacing=15,
        )

    def _profile_card(self):
        nom = self.user.get("nom", "Utilisateur")
        email = self.user.get("email", "email non défini")
        role_text = "Étudiant" if self.role == "ETUDIANT" else "Gestionnaire"

        return card(
            ft.Row(
                controls=[
                    ft.Container(
                        width=150,
                        height=150,
                        border_radius=28,
                        bgcolor="#EAF3FF",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(ft.Icons.PERSON, size=95, color="#0B63F6"),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Bonjour,", size=24, color="#111827"),
                            ft.Text(
                                str(nom).replace(".", " ").upper(),
                                size=42,
                                weight=ft.FontWeight.BOLD,
                                color="#0B63F6",
                            ),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=14, vertical=6),
                                border_radius=10,
                                bgcolor="#DDEBFF",
                                content=ft.Text(
                                    f"Rôle : {role_text}",
                                    color="#0B63F6",
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Row(
                                controls=[
                                    self._info_item(ft.Icons.EMAIL, email),
                                    self._separator(),
                                    self._info_item(ft.Icons.SCHOOL, "Promotion : L2"),
                                    self._separator(),
                                    self._info_item(ft.Icons.CALENDAR_MONTH, "Membre depuis : 2024"),
                                ],
                                spacing=12,
                                wrap=True,
                            ),
                        ],
                        spacing=10,
                        expand=True,
                    ),
                ],
                spacing=35,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=230,
        )

    def _info_item(self, icon, text):
        return ft.Row(
            controls=[
                ft.Icon(icon, size=18, color="#0B63F6"),
                ft.Text(str(text), size=14, color="#111827"),
            ],
            spacing=6,
        )

    def _separator(self):
        return ft.Text("|", color="#CBD5E1")

    def _stats_row(self, reservations, emprunts, alertes, materiels):
        return ft.Row(
            controls=[
                self._stat_card("Réservations à venir", reservations, "Dans les prochains jours", ft.Icons.CALENDAR_MONTH, "#EAF3FF", "#0B63F6"),
                self._stat_card("Emprunts en cours", emprunts, "À restituer prochainement", ft.Icons.ACCESS_TIME, "#F1ECFF", "#6D28D9"),
                self._stat_card("Alertes", alertes, "Stock faible et messages", ft.Icons.NOTIFICATIONS, "#FFF1DE", "#F97316"),
                self._stat_card("Matériels disponibles", materiels, "Dans l'inventaire du FabLab", ft.Icons.INVENTORY, "#E8F8EE", "#16A34A"),
            ],
            spacing=14,
            wrap=True,
        )

    def _stat_card(self, title, value, subtitle, icon, bg_icon, color):
        return ft.Container(
            width=250,
            height=120,
            padding=18,
            bgcolor=WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="#E5E7EB"),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=55,
                        height=55,
                        border_radius=30,
                        bgcolor=bg_icon,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(icon, color=color, size=28),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(str(value), size=28, weight=ft.FontWeight.BOLD, color=color),
                            ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color="#111827"),
                            ft.Text(subtitle, size=12, color="#64748B"),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=14,
            ),
        )

    def _main_tables(self, emprunts, reservations):
        if self.role == "ETUDIANT":
            left_title = "Mes emprunts en cours"
            right_title = "Mes réservations à venir"
        else:
            left_title = "Demandes d'emprunt récentes"
            right_title = "Réservations récentes"

        return ft.Row(
            controls=[
                self._emprunts_card(left_title, emprunts),
                self._reservations_card(right_title, reservations),
            ],
            spacing=14,
            wrap=True,
        )

    def _emprunts_card(self, title, emprunts):
        rows = []

        if not emprunts:
            rows.append(ft.Text("Aucun emprunt trouvé.", color="#64748B"))
        else:
            rows.append(self._table_header(["Matériel", "Quantité", "Date", "Statut"]))

            for emprunt in emprunts[:5]:
                rows.append(
                    self._table_row(
                        [
                            getattr(emprunt, "nom_materiel", getattr(emprunt, "id_materiel", "")),
                            getattr(emprunt, "quantite", ""),
                            str(getattr(emprunt, "date_emprunt", ""))[:10],
                            self._status_badge(getattr(emprunt, "statut_emprunt", "")),
                        ]
                    )
                )

        return card(
            ft.Column(
                controls=[
                    self._card_title(ft.Icons.ASSIGNMENT, title, "Liste des matériels empruntés"),
                    *rows,
                ],
                spacing=12,
            ),
            width=520,
        )

    def _reservations_card(self, title, reservations):
        rows = []

        if not reservations:
            rows.append(ft.Text("Aucune réservation trouvée.", color="#64748B"))
        else:
            rows.append(self._table_header(["Machine", "Date", "Heure", "Statut"]))

            for reservation in reservations[:5]:
                heure = f"{getattr(reservation, 'heure_debut', '')} - {getattr(reservation, 'heure_fin', '')}"
                rows.append(
                    self._table_row(
                        [
                            getattr(reservation, "nom_machine", getattr(reservation, "id_machine", "")),
                            getattr(reservation, "date_reservation", ""),
                            heure,
                            self._status_badge(getattr(reservation, "statut_reservation", "")),
                        ]
                    )
                )

        return card(
            ft.Column(
                controls=[
                    self._card_title(ft.Icons.CALENDAR_MONTH, title, "Vos prochaines réservations de machines"),
                    *rows,
                ],
                spacing=12,
            ),
            width=580,
        )

    def _card_title(self, icon, title, subtitle):
        return ft.Row(
            controls=[
                ft.Container(
                    width=46,
                    height=46,
                    border_radius=10,
                    bgcolor="#0B63F6",
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(icon, color=WHITE, size=24),
                ),
                ft.Column(
                    controls=[
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#111827"),
                        ft.Text(subtitle, size=12, color="#64748B"),
                    ],
                    spacing=1,
                ),
            ],
            spacing=12,
        )

    def _table_header(self, labels):
        return ft.Row(
            controls=[
                ft.Text(label, expand=True, size=12, color="#475569", weight=ft.FontWeight.BOLD)
                for label in labels
            ]
        )

    def _table_row(self, values):
        controls = []

        for value in values:
            if isinstance(value, ft.Control):
                controls.append(ft.Container(content=value, expand=True))
            else:
                controls.append(ft.Text(str(value), expand=True, size=13, color="#111827"))

        return ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Row(controls=controls),
        )

    def _status_badge(self, status):
        status = str(status).lower()

        if "valid" in status or "confirm" in status or "restit" in status:
            bgcolor = "#DCFCE7"
            color = "#15803D"
        elif "attente" in status:
            bgcolor = "#FFEDD5"
            color = "#EA580C"
        else:
            bgcolor = "#DBEAFE"
            color = "#0B63F6"

        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=8,
            bgcolor=bgcolor,
            content=ft.Text(
                status.capitalize() if status else "En cours",
                size=12,
                color=color,
                weight=ft.FontWeight.BOLD,
            ),
        )

    def _info_card(self):
        return ft.Container(
            padding=18,
            bgcolor="#EAF3FF",
            border_radius=16,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=45,
                        height=45,
                        border_radius=30,
                        bgcolor="#0B63F6",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(ft.Icons.INFO, color=WHITE),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Informations", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Pensez à restituer vos emprunts à temps et à annuler vos réservations si vous ne pouvez plus venir.",
                                size=13,
                                color="#334155",
                            ),
                        ],
                    ),
                ],
                spacing=14,
            ),
        )

    def _get_emprunts(self):
        try:
            if self.emprunt_service is None:
                return []
            if self.role == "ETUDIANT" and hasattr(self.emprunt_service, "find_by_etudiant"):
                return self.emprunt_service.find_by_etudiant(self.user.get("id"))
            return self.emprunt_service.get_all()
        except Exception:
            return []

    def _get_reservations(self):
        try:
            if self.reservation_service is None:
                return []
            if self.role == "ETUDIANT" and hasattr(self.reservation_service, "find_by_etudiant"):
                return self.reservation_service.find_by_etudiant(self.user.get("id"))
            return self.reservation_service.get_all()
        except Exception:
            return []

    def _get_materiels(self):
        try:
            if self.stock_service is None:
                return []
            return self.stock_service.consulter_inventaire()
        except Exception:
            return []

    def _get_alertes(self):
        try:
            if self.alerte_service is None:
                return []
            return self.alerte_service.get_all()
        except Exception:
            return []