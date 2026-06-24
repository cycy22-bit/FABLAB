import flet as ft


PRIMARY_COLOR = "#1E88E5"
BG_COLOR = "#F5F8FC"


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
        text=text,
        icon=icon,
        on_click=on_click,
        bgcolor=PRIMARY_COLOR,
        color="white",
        height=45,
    )


def danger_button(text: str, on_click=None, icon=None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        bgcolor="#D32F2F",
        color="white",
        height=45,
    )


def input_field(label: str, password: bool = False) -> ft.TextField:
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,
        border_radius=10,
        filled=True,
        bgcolor="white",
    )


def card(content: ft.Control, width=None, height=None) -> ft.Container:
    return ft.Container(
        content=content,
        width=width,
        height=height,
        padding=20,
        bgcolor="white",
        border_radius=15,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=1,
            color="#DDDDDD",
        ),
    )


def notify(page: ft.Page, message: str, success: bool = True) -> None:
    page.snack_bar = ft.SnackBar(
        content=ft.Text(message),
        bgcolor="#2E7D32" if success else "#C62828",
    )
    page.snack_bar.open = True
    page.update()