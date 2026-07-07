import flet as ft
from .components import title_text, input_field, primary_button, card, notify, show_popup


class EmpruntView:
    def __init__(self, page: ft.Page, emprunt_service, user: dict, stock_service=None, mode="liste"):
        self.page = page
        self.emprunt_service = emprunt_service
        self.stock_service = stock_service
        self.user = user
        self.mode = mode
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

        self.stock_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Matériel")),
                ft.DataColumn(ft.Text("Catégorie")),
                ft.DataColumn(ft.Text("Disponible")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        controls = []

        if self.role == "GESTIONNAIRE":
            self.refresh_table()
            controls.append(title_text("Demandes d'emprunt"))
            controls.append(self._emprunts_card())
            return self._page(controls)

        if self.mode == "demande":
            self.refresh_stock_table()
            controls.append(title_text("Demander un emprunt"))
            controls.append(self._form_card())
            controls.append(self._stock_card())
            return self._page(controls)

        self.refresh_table()
        controls.append(title_text("Mes emprunts"))
        controls.append(self._emprunts_card())
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

    def _stock_card(self):
        return card(
            ft.Column(
                controls=[
                    ft.Text("Matériels disponibles", size=18, weight=ft.FontWeight.BOLD),
                    self.stock_table,
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        )

    def _emprunts_card(self):
        return card(
            ft.Column(
                controls=[
                    ft.Text("Liste des emprunts", size=18, weight=ft.FontWeight.BOLD),
                    self.table,
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        )

    def refresh_stock_table(self):
        self.stock_table.rows.clear()

        try:
            if self.stock_service is None:
                return

            materiels = self.stock_service.consulter_inventaire()

            for materiel in materiels:
                quantite = getattr(materiel, "quantite_stock", 0)

                if quantite > 0:
                    self.stock_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(getattr(materiel, "id_materiel", "")))),
                                ft.DataCell(ft.Text(str(getattr(materiel, "nom_materiel", "")))),
                                ft.DataCell(ft.Text(str(getattr(materiel, "categorie", "")))),
                                ft.DataCell(ft.Text(str(quantite))),
                            ]
                        )
                    )

        except Exception as ex:
            notify(self.page, f"Erreur de chargement du stock : {ex}", False)

    def refresh_table(self):
        self.table.rows.clear()

        try:
            if self.role == "ETUDIANT":
                emprunts = self.emprunt_service.find_by_etudiant(self.user.get("id"))
            else:
                emprunts = self.emprunt_service.get_all()

            for emprunt in emprunts:
                statut = str(getattr(emprunt, "statut_emprunt", ""))

                cells = [
                    ft.DataCell(ft.Text(str(getattr(emprunt, "id_emprunt", "")))),
                    ft.DataCell(ft.Text(str(getattr(emprunt, "nom_etudiant", getattr(emprunt, "id_etudiant", ""))))),
                    ft.DataCell(ft.Text(str(getattr(emprunt, "nom_materiel", getattr(emprunt, "id_materiel", ""))))),
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
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    "La quantité demandée doit être supérieure à zéro.",
                    "rejeté",
                    False,
                )
                return

            if duree <= 0 or duree > 30:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    "La durée d'emprunt doit être comprise entre 1 et 30 jours.",
                    "rejeté",
                    False,
                )
                return

            result = self.emprunt_service.emprunter_materiel(
                id_etudiant=id_etudiant,
                id_materiel=id_materiel,
                quantite=quantite,
                duree=duree,
            )

            if result:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    f"Votre demande d'emprunt du matériel n°{id_materiel} a été enregistrée.\n\n"
                    f"Quantité demandée : {quantite}\n"
                    f"Durée : {duree} jour(s)\n\n"
                    "Elle est maintenant en attente de validation par le gestionnaire.",
                    "en attente",
                    True,
                )

                self.id_materiel_field.value = ""
                self.quantite_field.value = ""
                self.duree_field.value = ""
                self.refresh_stock_table()
                self.page.update()
            else:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    "Votre demande d'emprunt a été rejetée.\n\n"
                    "Causes possibles :\n"
                    "- vous avez déjà un emprunt actif pour ce matériel ;\n"
                    "- le stock disponible est insuffisant ;\n"
                    "- le matériel demandé n'existe pas.",
                    "rejeté",
                    False,
                )

        except ValueError:
            show_popup(
                self.page,
                "Détails de l'emprunt",
                "Les champs ID matériel, quantité et durée doivent contenir des nombres valides.",
                "rejeté",
                False,
            )
        except Exception as ex:
            show_popup(
                self.page,
                "Erreur système",
                f"Une erreur est survenue : {ex}",
                "erreur",
                False,
            )

    def on_accepter_clicked(self, id_emprunt):
        try:
            result = self.emprunt_service.accepter_emprunt(id_emprunt)

            if result:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    f"L'emprunt n°{id_emprunt} a été accepté.\n\nLe stock a été automatiquement mis à jour.",
                    "accepté",
                    True,
                )
                self.refresh_table()
                self.page.update()
            else:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    f"Impossible d'accepter l'emprunt n°{id_emprunt}.\n\n"
                    "Causes possibles : stock insuffisant ou demande déjà traitée.",
                    "rejeté",
                    False,
                )

        except Exception as ex:
            show_popup(self.page, "Erreur système", f"Une erreur est survenue : {ex}", "erreur", False)

    def on_refuser_clicked(self, id_emprunt):
        try:
            result = self.emprunt_service.refuser_emprunt(id_emprunt)

            if result:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    f"L'emprunt n°{id_emprunt} a été refusé.\n\nAucune modification du stock n'a été effectuée.",
                    "rejeté",
                    False,
                )
                self.refresh_table()
                self.page.update()
            else:
                show_popup(
                    self.page,
                    "Détails de l'emprunt",
                    f"Impossible de refuser l'emprunt n°{id_emprunt}.\n\nLa demande est peut-être déjà traitée.",
                    "erreur",
                    False,
                )

        except Exception as ex:
            show_popup(self.page, "Erreur système", f"Une erreur est survenue : {ex}", "erreur", False)