import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class EmpruntView:
    def __init__(self, page: ft.Page, emprunt_service, user: dict):
        self.page = page
        self.emprunt_service = emprunt_service
        self.user = user
        self.role = self.user.get("role", "").upper()

        self.id_etudiant_field = input_field("ID étudiant")
        self.id_materiel_field = input_field("ID matériel")
        self.quantite_field = input_field("Quantité")
        self.duree_field = input_field("Durée d'emprunt en jours")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Étudiant")),
                ft.DataColumn(ft.Text("Matériel")),
                ft.DataColumn(ft.Text("Quantité")),
                ft.DataColumn(ft.Text("Statut")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        controls = [
            title_text(
                "Liste des emprunts"
                if self.role == "GESTIONNAIRE"
                else "Mes emprunts"
            )
        ]

        # Le formulaire n'est visible que pour l'étudiant
        if self.role == "ETUDIANT":
            controls.append(
                card(
                    ft.Column(
                        controls=[
                            self.id_materiel_field,
                            self.quantite_field,
                            self.duree_field,
                            primary_button(
                                "Demander emprunt",
                                self.on_emprunter_clicked,
                                ft.Icons.SEND,
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
                            "Liste des emprunts",
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
            if self.role == "ETUDIANT" and hasattr(self.emprunt_service, "find_by_etudiant"):
                emprunts = self.emprunt_service.find_by_etudiant(self.user.get("id"))
            else:
                emprunts = self.emprunt_service.get_all()

            for emprunt in emprunts:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(emprunt, "id_emprunt", "")))),
                            ft.DataCell(ft.Text(str(getattr(emprunt, "id_etudiant", "")))),
                            ft.DataCell(ft.Text(str(getattr(emprunt, "id_materiel", "")))),
                            ft.DataCell(ft.Text(str(getattr(emprunt, "quantite", "")))),
                            ft.DataCell(ft.Text(str(getattr(emprunt, "statut_emprunt", "")))),
                        ]
                    )
                )

        except Exception as ex:
            notify(self.page, f"Erreur de chargement des emprunts : {ex}", False)

    def on_emprunter_clicked(self, e):
        try:
            if self.role == "ETUDIANT":
                id_etudiant = int(self.user.get("id"))
            else:
                id_etudiant = int(self.id_etudiant_field.value)

            id_materiel = int(self.id_materiel_field.value)
            quantite = int(self.quantite_field.value)
            duree = int(self.duree_field.value)

            if quantite <= 0:
                notify(self.page, "La quantité doit être supérieure à 0.", False)
                return

            if duree <= 0 or duree > 30:
                notify(self.page, "La durée d'emprunt doit être comprise entre 1 et 30 jours.", False)
                return

            result = self.emprunt_service.emprunter_materiel(
                id_etudiant=id_etudiant,
                id_materiel=id_materiel,
                quantite=quantite,
                duree=duree,
            )

            if result:
                notify(self.page, "Demande d'emprunt enregistrée.", success=True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Demande refusée.", success=False)

        except ValueError:
            notify(self.page, "Tous les champs numériques doivent être valides.", success=False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", success=False)