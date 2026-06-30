import flet as ft
from .components import title_text, input_field, primary_button, card, notify, PRIMARY_COLOR


class StockView:
    def __init__(self, page: ft.Page, stock_service, readonly: bool = False):
        self.page = page
        self.stock_service = stock_service
        self.readonly = readonly

        self.nom_field = input_field("Nom du matériel")
        self.categorie_field = input_field("Catégorie")
        self.quantite_field = input_field("Quantité initiale")
        self.stock_min_field = input_field("Stock minimum")

        self.id_materiel_field = input_field("ID matériel existant")
        self.quantite_mouvement_field = input_field("Quantité à ajouter/retirer")

        self.list_container = ft.Column(spacing=8)

    def build(self) -> ft.Control:
        self.refresh_list()

        controls = [
            title_text("Stock disponible" if self.readonly else "Inventaire / Stock"),
        ]

        if not self.readonly:
            controls.append(
                card(
                    ft.Column(
                        controls=[
                            ft.Text("Ajouter un nouveau matériel", size=18, weight=ft.FontWeight.BOLD),
                            self.nom_field,
                            self.categorie_field,
                            self.quantite_field,
                            self.stock_min_field,
                            primary_button("Ajouter matériel", self.on_save_clicked, ft.Icons.ADD),
                        ],
                        spacing=10,
                    )
                )
            )

            controls.append(
                card(
                    ft.Column(
                        controls=[
                            ft.Text("Modifier la quantité d'un matériel existant", size=18, weight=ft.FontWeight.BOLD),
                            self.id_materiel_field,
                            self.quantite_mouvement_field,
                            ft.Row(
                                controls=[
                                    primary_button("Ajouter quantité", self.on_ajouter_quantite, ft.Icons.ADD),
                                    primary_button("Retirer quantité", self.on_retirer_quantite, ft.Icons.REMOVE),
                                ],
                                spacing=10,
                                wrap=True,
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
                        ft.Text("Liste des matériels", size=18, weight=ft.FontWeight.BOLD),
                        self._header_row(),
                        self.list_container,
                    ],
                    spacing=8,
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

    def _header_row(self):
        return ft.Container(
            bgcolor="#EAF3FF",
            border_radius=8,
            padding=10,
            content=ft.Row(
                controls=[
                    ft.Text("ID", width=50, weight=ft.FontWeight.BOLD),
                    ft.Text("Nom", width=220, weight=ft.FontWeight.BOLD),
                    ft.Text("Catégorie", width=180, weight=ft.FontWeight.BOLD),
                    ft.Text("Quantité", width=100, weight=ft.FontWeight.BOLD),
                    ft.Text("Stock min.", width=100, weight=ft.FontWeight.BOLD),
                    ft.Text("État", width=120, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
        )

    def _materiel_row(self, materiel):
        quantite = int(getattr(materiel, "quantite_stock", 0))
        stock_min = int(getattr(materiel, "stock_minimum", 0))
        etat = "Stock faible" if quantite < stock_min else "Disponible"

        return ft.Container(
            padding=10,
            border_radius=8,
            bgcolor="white",
            border=ft.border.all(1, "#E0E0E0"),
            content=ft.Row(
                controls=[
                    ft.Text(str(getattr(materiel, "id_materiel", "")), width=50),
                    ft.Text(str(getattr(materiel, "nom_materiel", "")), width=220),
                    ft.Text(str(getattr(materiel, "categorie", "")), width=180),
                    ft.Text(str(quantite), width=100, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
                    ft.Text(str(stock_min), width=100),
                    ft.Text(etat, width=120),
                ],
                spacing=10,
            ),
        )

def refresh_list(self):
    self.list_container.controls.clear()

    try:
        materiels = self.stock_service.consulter_inventaire()
        print("MATERIELS CHARGES :", materiels)

        if not materiels:
            self.list_container.controls.append(
                ft.Text("Aucun matériel disponible.", color="#777777")
            )
        else:
            for materiel in materiels:
                self.list_container.controls.append(self._materiel_row(materiel))

        self.page.update()

    except Exception as ex:
        print("ERREUR STOCK VIEW :", ex)
        self.list_container.controls.append(
            ft.Text(f"Erreur de chargement : {ex}", color="red")
        )
        self.page.update()

    def on_save_clicked(self, e):
        if self.readonly:
            notify(self.page, "Action interdite : accès étudiant en lecture seule.", False)
            return

        try:
            nom = self.nom_field.value.strip()
            categorie = self.categorie_field.value.strip()
            quantite = int(self.quantite_field.value)
            stock_minimum = int(self.stock_min_field.value)

            if not nom or not categorie:
                notify(self.page, "Nom et catégorie obligatoires.", False)
                return

            if quantite < 0 or stock_minimum < 0:
                notify(self.page, "Les quantités doivent être positives.", False)
                return

            result = self.stock_service.ajouter_materiel(
                nom_materiel=nom,
                categorie=categorie,
                quantite_stock=quantite,
                stock_minimum=stock_minimum,
            )

            if result:
                notify(self.page, "Matériel ajouté avec succès.", True)
                self.clear_add_fields()
                self.refresh_list()
                self.page.update()
            else:
                notify(self.page, "Ajout impossible.", False)

        except ValueError:
            notify(self.page, "Quantité et stock minimum doivent être numériques.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def on_ajouter_quantite(self, e):
        try:
            id_materiel = int(self.id_materiel_field.value)
            quantite = int(self.quantite_mouvement_field.value)

            result = self.stock_service.ajouter_quantite(id_materiel, quantite)

            if result:
                notify(self.page, "Quantité ajoutée avec succès.", True)
                self.clear_mouvement_fields()
                self.refresh_list()
                self.page.update()
            else:
                notify(self.page, "Ajout de quantité impossible.", False)

        except ValueError:
            notify(self.page, "ID matériel et quantité doivent être numériques.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def on_retirer_quantite(self, e):
        try:
            id_materiel = int(self.id_materiel_field.value)
            quantite = int(self.quantite_mouvement_field.value)

            result = self.stock_service.retirer_quantite(id_materiel, quantite)

            if result:
                notify(self.page, "Quantité retirée avec succès.", True)
                self.clear_mouvement_fields()
                self.refresh_list()
                self.page.update()
            else:
                notify(self.page, "Retrait impossible : stock insuffisant ou matériel inexistant.", False)

        except ValueError:
            notify(self.page, "ID matériel et quantité doivent être numériques.", False)
        except Exception as ex:
            notify(self.page, f"Erreur : {ex}", False)

    def clear_add_fields(self):
        self.nom_field.value = ""
        self.categorie_field.value = ""
        self.quantite_field.value = ""
        self.stock_min_field.value = ""

    def clear_mouvement_fields(self):
        self.id_materiel_field.value = ""
        self.quantite_mouvement_field.value = ""