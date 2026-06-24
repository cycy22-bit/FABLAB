import flet as ft
from .components import title_text, input_field, primary_button, card, notify


class StockView:
    def __init__(self, page: ft.Page, stock_service):
        self.page = page
        self.stock_service = stock_service

        self.nom_field = input_field("Nom du matériel")
        self.categorie_field = input_field("Catégorie")
        self.quantite_field = input_field("Quantité")
        self.stock_min_field = input_field("Stock minimum")

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nom")),
                ft.DataColumn(ft.Text("Catégorie")),
                ft.DataColumn(ft.Text("Quantité")),
                ft.DataColumn(ft.Text("Stock min.")),
            ],
            rows=[],
        )

    def build(self) -> ft.Control:
        self.refresh_table()

        return ft.Column(
            controls=[
                title_text("Inventaire / Stock"),

                card(
                    ft.Column(
                        controls=[
                            self.nom_field,
                            self.categorie_field,
                            self.quantite_field,
                            self.stock_min_field,
                            primary_button("Ajouter matériel", self.on_save_clicked, ft.Icons.ADD),
                        ],
                        spacing=10,
                    )
                ),

                card(
                    ft.Column(
                        controls=[
                            ft.Text("Liste des matériels", size=18, weight=ft.FontWeight.BOLD),
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
            materiels = self.stock_service.consulter_inventaire()

            for materiel in materiels:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(getattr(materiel, "id_materiel", "")))),
                            ft.DataCell(ft.Text(str(getattr(materiel, "nom_materiel", "")))),
                            ft.DataCell(ft.Text(str(getattr(materiel, "categorie", "")))),
                            ft.DataCell(ft.Text(str(getattr(materiel, "quantite_stock", "")))),
                            ft.DataCell(ft.Text(str(getattr(materiel, "stock_minimum", "")))),
                        ]
                    )
                )

        except Exception:
            pass

    def on_save_clicked(self, e):
        try:
            nom = self.nom_field.value.strip()
            categorie = self.categorie_field.value.strip()
            quantite = int(self.quantite_field.value)
            stock_minimum = int(self.stock_min_field.value)

            if not nom or not categorie:
                notify(self.page, "Nom et catégorie obligatoires.", success=False)
                return

            result = self.stock_service.ajouter_materiel(
                nom_materiel=nom,
                categorie=categorie,
                quantite_stock=quantite,
                stock_minimum=stock_minimum,
            )

            if result:
                notify(self.page, "Matériel ajouté avec succès.", success=True)
                self.refresh_table()
                self.page.update()
            else:
                notify(self.page, "Ajout impossible.", success=False)

        except ValueError:
            notify(self.page, "La quantité et le stock minimum doivent être numériques.", success=False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", success=False)