import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class EmpruntView:
    def __init__(self, page: ft.Page, emprunt_service, user: dict):
        self.page = page
        self.emprunt_service = emprunt_service
        self.user = user
        self.role = self.user.get("role", "").upper()

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
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        controls = [
            title_text(
                "Demandes d'emprunt"
                if self.role == "GESTIONNAIRE"
                else "Mes emprunts"
            )
        ]

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
                statut = str(getattr(emprunt, "statut_emprunt", ""))

                cells = [
                    ft.DataCell(ft.Text(str(getattr(emprunt, "id_emprunt", "")))),
                    ft.DataCell(
                        ft.Text(
                            str(
                                getattr(
                                    emprunt,
                                    "nom_etudiant",
                                    getattr(emprunt, "id_etudiant", ""),
                                )
                            )
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            str(
                                getattr(
                                    emprunt,
                                    "nom_materiel",
                                    getattr(emprunt, "id_materiel", ""),
                                )
                            )
                        )
                    ),
                    ft.DataCell(ft.Text(str(getattr(emprunt, "quantite", "")))),
                    ft.DataCell(ft.Text(statut)),
                ]

                if self.role == "GESTIONNAIRE" and statut == "en attente":
                    id_emprunt = getattr(emprunt, "id_emprunt", None)

                    cells.append(
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.TextButton(
                                        "Accepter",
                                        on_click=lambda e, eid=id_emprunt: self.on_accepter_clicked(eid),
                                    ),
                                    ft.TextButton(
                                        "Refuser",
                                        on_click=lambda e, eid=id_emprunt: self.on_refuser_clicked(eid),
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
            notify(self.page, f"Erreur de chargement des emprunts : {ex}", False)

    def on_emprunter_clicked(self, e):
        try:
            id_etudiant = int(self.user.get("id"))
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
                notify(self.page, "Demande d'emprunt enregistrée. En attente de validation.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Demande refusée : matériel indisponible ou déjà emprunté.", False)

        except ValueError:
            notify(self.page, "Tous les champs numériques doivent être valides.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def on_accepter_clicked(self, id_emprunt):
        try:
            result = self.emprunt_service.accepter_emprunt(id_emprunt)

            if result:
                notify(self.page, "Emprunt accepté. Le stock a été mis à jour.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Impossible d'accepter cet emprunt.", False)

        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def on_refuser_clicked(self, id_emprunt):
        try:
            result = self.emprunt_service.refuser_emprunt(id_emprunt)

            if result:
                notify(self.page, "Emprunt refusé.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Impossible de refuser cet emprunt.", False)

        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)