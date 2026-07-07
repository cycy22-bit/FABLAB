import flet as ft
from .components import card


BLUE = "#0B63F6"
DARK = "#111827"
GRAY = "#64748B"


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
                ft.Text("Tableau de bord", size=34, weight=ft.FontWeight.BOLD, color=DARK),
                self._profile_card(),
                ft.Row(
                    controls=[
                        self._stat_card("Réservations", len(reservations), BLUE),
                        self._stat_card("Emprunts", len(emprunts), "#6D28D9"),
                        self._stat_card("Alertes", len(alertes), "#F97316"),
                        self._stat_card("Matériels", len(materiels), "#16A34A"),
                    ],
                    spacing=15,
                    wrap=True,
                ),
                ft.Row(
                    controls=[
                        self._emprunts_card(emprunts),
                        self._reservations_card(reservations),
                    ],
                    spacing=15,
                    wrap=True,
                ),
            ],
            spacing=20,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def _profile_card(self):
        nom = self.user.get("nom", "Utilisateur")
        email = self.user.get("email", "Email non défini")
        role = "Étudiant" if self.role == "ETUDIANT" else "Gestionnaire"

        return card(
            ft.Row(
                controls=[
                    ft.Container(
                        width=110,
                        height=110,
                        border_radius=25,
                        bgcolor="#EAF3FF",
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text("👤", size=55),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text("Bonjour,", size=22, color=DARK),
                            ft.Text(
                                str(nom).replace(".", " ").upper(),
                                size=36,
                                weight=ft.FontWeight.BOLD,
                                color=BLUE,
                            ),
                            ft.Container(
                                padding=10,
                                border_radius=10,
                                bgcolor="#DDEBFF",
                                content=ft.Text(
                                    f"Rôle : {role}",
                                    color=BLUE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Text(email, size=14, color=GRAY),
                            ft.Text("Promotion : L2 | Membre depuis : 2024", size=13, color=GRAY),
                        ],
                        spacing=8,
                        expand=True,
                    ),
                ],
                spacing=25,
            ),
            height=200,
        )

    def _stat_card(self, title, value, color):
        return card(
            ft.Column(
                controls=[
                    ft.Text(str(value), size=32, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=DARK),
                ],
                spacing=5,
            ),
            width=240,
            height=110,
        )

    def _emprunts_card(self, emprunts):
        title = "Mes emprunts en cours" if self.role == "ETUDIANT" else "Demandes d'emprunt récentes"
        controls = [ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=DARK)]

        if not emprunts:
            controls.append(ft.Text("Aucun emprunt trouvé.", color=GRAY))
        else:
            controls.append(self._header(["Matériel", "Qté", "Date", "Statut"]))

            for e in emprunts[:5]:
                controls.append(
                    self._row(
                        [
                            getattr(e, "nom_materiel", getattr(e, "id_materiel", "")),
                            getattr(e, "quantite", ""),
                            str(getattr(e, "date_emprunt", ""))[:10],
                            getattr(e, "statut_emprunt", ""),
                        ]
                    )
                )

        return card(ft.Column(controls=controls, spacing=12), width=520)

    def _reservations_card(self, reservations):
        title = "Mes réservations à venir" if self.role == "ETUDIANT" else "Réservations récentes"
        controls = [ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=DARK)]

        if not reservations:
            controls.append(ft.Text("Aucune réservation trouvée.", color=GRAY))
        else:
            controls.append(self._header(["Machine", "Date", "Heure", "Statut"]))

            for r in reservations[:5]:
                heure = f"{getattr(r, 'heure_debut', '')} - {getattr(r, 'heure_fin', '')}"
                controls.append(
                    self._row(
                        [
                            getattr(r, "nom_machine", getattr(r, "id_machine", "")),
                            getattr(r, "date_reservation", ""),
                            heure,
                            getattr(r, "statut_reservation", ""),
                        ]
                    )
                )

        return card(ft.Column(controls=controls, spacing=12), width=570)

    def _header(self, labels):
        return ft.Container(
            padding=8,
            bgcolor="#EAF3FF",
            border_radius=8,
            content=ft.Row(
                controls=[
                    ft.Text(label, expand=True, size=12, weight=ft.FontWeight.BOLD, color="#334155")
                    for label in labels
                ]
            ),
        )

    def _row(self, values):
        return ft.Container(
            padding=8,
            bgcolor="#F8FAFC",
            border_radius=8,
            content=ft.Row(
                controls=[
                    ft.Text(str(value), expand=True, size=13, color=DARK)
                    for value in values
                ]
            ),
        )

    def _get_emprunts(self):
        try:
            if self.emprunt_service is None:
                return []

            if self.role == "ETUDIANT":
                return self.emprunt_service.find_by_etudiant(self.user.get("id"))

            return self.emprunt_service.get_all()

        except Exception as ex:
            print("Erreur dashboard emprunts :", ex)
            return []

    def _get_reservations(self):
        try:
            if self.reservation_service is None:
                return []

            if self.role == "ETUDIANT":
                return self.reservation_service.find_by_etudiant(self.user.get("id"))

            return self.reservation_service.get_all()

        except Exception as ex:
            print("Erreur dashboard réservations :", ex)
            return []

    def _get_materiels(self):
        try:
            if self.stock_service is None:
                return []

            return self.stock_service.consulter_inventaire()

        except Exception as ex:
            print("Erreur dashboard matériels :", ex)
            return []

    def _get_alertes(self):
        try:
            if self.alerte_service is None:
                return []

            return self.alerte_service.get_all()

        except Exception as ex:
            print("Erreur dashboard alertes :", ex)
            return []