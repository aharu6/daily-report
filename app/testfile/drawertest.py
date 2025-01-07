import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_dismissal(e):
        page.add(ft.Text("End drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.control.selected_index}"))
        # page.close(end_drawer)

    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.NavigationDrawerDestination(icon=ft.icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"),
            ft.NavigationDrawerDestination(icon=ft.Icon(ft.icons.ADD_COMMENT), label="Item 2"),
        ],
    )

    page.add(ft.ElevatedButton("Show end drawer", on_click=lambda e: page.open(end_drawer)))


ft.app(main)