import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class CommandeView:
    def __init__(self, page: ft.Page, commande_service):
        self.page = page
        self.commande_service = commande_service

        self.id_fournisseur_field = input_field("ID fournisseur")
        self.id_gestionnaire_field = input_field("ID gestionnaire")
        self.date_commande_field = input_field("Date commande : AAAA-MM-JJ")
        self.date_livraison_field = input_field("Date livraison prévue : AAAA-MM-JJ")
        self.montant_field = input_field("Montant total")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Fournisseur")),
                ft.DataColumn(ft.Text("Gestionnaire")),
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Livraison prévue")),
                ft.DataColumn(ft.Text("Statut")),
                ft.DataColumn(ft.Text("Montant")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        return ft.Column(
            controls=[
                title_text("Commandes d'approvisionnement"),

                card(
                    ft.Column(
                        controls=[
                            self.id_fournisseur_field,
                            self.id_gestionnaire_field,
                            self.date_commande_field,
                            self.date_livraison_field,
                            self.montant_field,
                            primary_button("Créer commande", self.on_commande_clicked, ft.Icons.SHOPPING_CART),
                        ],
                        spacing=10,
                    )
                ),

                card(
                    ft.Column(
                        controls=[
                            ft.Text("Liste des commandes", size=18, weight=ft.FontWeight.BOLD),
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
            commandes = self.commande_service.get_all()

            for commande in commandes:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(commande, "id_commande", "")))),
                            ft.DataCell(ft.Text(str(getattr(commande, "id_fournisseur", "")))),
                            ft.DataCell(ft.Text(str(getattr(commande, "id_gestionnaire", "")))),
                            ft.DataCell(ft.Text(str(getattr(commande, "date_commande", "")))),
                            ft.DataCell(ft.Text(str(getattr(commande, "date_livraison_prevue", "")))),
                            ft.DataCell(ft.Text(str(getattr(commande, "statut_commande", "")))),
                            ft.DataCell(ft.Text(str(getattr(commande, "montant_total", "")))),
                        ]
                    )
                )
        except Exception:
            pass

    def on_commande_clicked(self, e):
        try:
            result = self.commande_service.creer_commande(
                id_fournisseur=int(self.id_fournisseur_field.value),
                id_gestionnaire=int(self.id_gestionnaire_field.value),
                date_commande=self.date_commande_field.value,
                date_livraison_prevue=self.date_livraison_field.value,
                montant_total=float(self.montant_field.value),
            )

            if result:
                notify(self.page, "Commande créée.", True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Commande refusée.", False)

        except ValueError:
            notify(self.page, "Vérifie les valeurs numériques.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)