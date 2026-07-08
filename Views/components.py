import flet as ft
from pathlib import Path


PRIMARY_COLOR = "#1E88E5"
DARK_COLOR = "#0B1220"
BG_COLOR = "#F5F8FC"
WHITE = "#FFFFFF"


def title_text(text: str) -> ft.Text:
    return ft.Text(
        value=text,
        size=26,
        weight=ft.FontWeight.BOLD,
        color=PRIMARY_COLOR,
    )


def subtitle_text(text: str) -> ft.Text:
    return ft.Text(
        value=text,
        size=14,
        color="#555555",
    )


def primary_button(text: str, on_click=None, icon=None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(icon) if icon else ft.Container(),
                ft.Text(text),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        on_click=on_click,
        bgcolor=PRIMARY_COLOR,
        color=WHITE,
        height=45,
    )


def danger_button(text: str, on_click=None, icon=None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(icon) if icon else ft.Container(),
                ft.Text(text),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        on_click=on_click,
        bgcolor="#D32F2F",
        color=WHITE,
        height=45,
    )


def input_field(label: str, password: bool = False) -> ft.TextField:
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,
        border_radius=10,
        filled=True,
        bgcolor=WHITE,
    )


def card(content: ft.Control, width=None, height=None) -> ft.Container:
    return ft.Container(
        content=content,
        width=width,
        height=height,
        padding=20,
        bgcolor=WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color="#DDDDDD",
        ),
    )


def logo_ulc_icam(size: int = 60) -> ft.Control:
    logo_path = Path("Assets/logo.png")

    if logo_path.exists():
        return ft.Image(
            src=str(logo_path),
            width=size,
            height=size,
        )

    return ft.Container(
        width=size,
        height=size,
        border_radius=8,
        bgcolor=PRIMARY_COLOR,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "SG\nFAB",
            size=10,
            color=WHITE,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
    )


def notify(page: ft.Page, message: str, success: bool = True) -> None:
    page.snack_bar = ft.SnackBar(
        content=ft.Text(message),
        bgcolor="#2E7D32" if success else "#C62828",
    )
    page.snack_bar.open = True
    page.update()


def show_popup(
    page: ft.Page,
    title: str,
    message: str,
    status: str = "",
    success: bool = True,
):
    def close_popup(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Column(
            controls=[
                ft.Text(
                    "ℹ",
                    size=42,
                    color="#00AEEF" if success else "#C62828",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    title,
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        content=ft.Column(
            controls=[
                ft.Text(
                    message,
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(),
                ft.Text(
                    f"Statut : {status.upper()}" if status else "",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="#2E7D32" if success else "#C62828",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            tight=True,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[
            ft.TextButton("Fermer", on_click=close_popup),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    page.dialog = dialog
    dialog.open = True
    page.update()