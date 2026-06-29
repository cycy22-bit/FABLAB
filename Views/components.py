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


def logo_ulc_icam(size: int = 42) -> ft.Control:
    logo_path = Path("Assets/logo_ulc_icam.png")

    if logo_path.exists():
        return ft.Image(
            src=str(logo_path),
            width=size,
            height=size,
            fit=ft.ImageFit.CONTAIN,
        )

    return ft.Container(
        width=size,
        height=size,
        border_radius=8,
        bgcolor=PRIMARY_COLOR,
        alignment=ft.alignment.center,
        content=ft.Text(
            "ULC\nICAM",
            size=9,
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