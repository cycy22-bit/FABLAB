import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class FournisseurView:
    def __init__(self, page: ft.Page, fournisseur_service):
        self.page = page
        self.fournisseur_service = fournisseur_service

        self.nom_field = input_field("Nom fournisseur")
        self.adresse_field = input_field("Adresse")
        self.telephone_field = input_field("Téléphone")
        self.email_field = input_field("Email")
        self.site_web_field = input_field("Site web")
        self.delai_field = input_field("Délai moyen de livraison")
        self.conditions_field = input_field("Conditions de paiement")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nom")),
                ft.DataColumn(ft.Text("Téléphone")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Délai")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        return ft.Column(
            controls=[
                title_text("Gestion des fournisseurs"),

                card(
                    ft.Column(
                        controls=[
                            self.nom_field,
                            self.adresse_field,
                            self.telephone_field,
                            self.email_field,
                            self.site_web_field,
                            self.delai_field,
                            self.conditions_field,
                            primary_button("Ajouter fournisseur", self.on_save_clicked, ft.Icons.ADD_BUSINESS),
                        ],
                        spacing=10,
                    )
                ),

                card(
                    ft.Column(
                        controls=[
                            ft.Text("Liste des fournisseurs", size=18, weight=ft.FontWeight.BOLD),
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
            fournisseurs = self.fournisseur_service.get_all()

            for fournisseur in fournisseurs:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(fournisseur, "id_fournisseur", "")))),
                            ft.DataCell(ft.Text(str(getattr(fournisseur, "nom_fournisseur", "")))),
                            ft.DataCell(ft.Text(str(getattr(fournisseur, "telephone", "")))),
                            ft.DataCell(ft.Text(str(getattr(fournisseur, "email", "")))),
                            ft.DataCell(ft.Text(str(getattr(fournisseur, "delai_livraison_moyen", "")))),
                        ]
                    )
                )
        except Exception:
            pass

    def on_save_clicked(self, e):
        try:
            result = self.fournisseur_service.create(
                nom_fournisseur=self.nom_field.value,
                adresse=self.adresse_field.value,
                telephone=self.telephone_field.value,
                email=self.email_field.value,
                site_web=self.site_web_field.value,
                delai_livraison_moyen=self.delai_field.value,
                conditions_paiement=self.conditions_field.value,
            )

            if result:
                notify(self.page, "Fournisseur ajouté.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Ajout impossible.", False)

        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)