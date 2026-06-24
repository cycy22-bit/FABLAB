import flet as ft
from .components import title_text, subtitle_text, input_field, primary_button, card, notify


class LoginView:
    def __init__(self, page: ft.Page, auth_service, on_login_success):
        self.page = page
        self.auth_service = auth_service
        self.on_login_success = on_login_success

        self.email_field = input_field("Email")
        self.password_field = input_field("Mot de passe", password=True)

    def build(self) -> ft.Control:
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            bgcolor="#F5F8FC",
            content=card(
                ft.Column(
                    controls=[
                        title_text("SG-FabLab"),
                        subtitle_text("Connexion au système de gestion du FabLab"),
                        self.email_field,
                        self.password_field,
                        primary_button("Se connecter", self.on_login_clicked, ft.Icons.LOGIN),
                    ],
                    spacing=18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=420,
            ),
        )

    def on_login_clicked(self, e):
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()

        if not email or not password:
            notify(self.page, "Veuillez remplir tous les champs.", success=False)
            return

        try:
            result = self.auth_service.se_connecter(email, password)

            if result:
                notify(self.page, "Connexion réussie.", success=True)
                self.on_login_success(result)
            else:
                notify(self.page, "Email ou mot de passe incorrect.", success=False)

        except Exception as ex:
            notify(self.page, f"Erreur de connexion : {ex}", success=False)