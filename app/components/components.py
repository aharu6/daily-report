import flet as ft
import datetime
from models.models import DataModel
from handlers.handlers import Handlers


class DateComponent:
    def __init__(self, page, today, handle_change):
        self.page = page
        self.today = today
        self.handle_change = handle_change

    def create(self):
        return ft.ElevatedButton(
            text=f"{self.today.year}/{self.today.month}/{self.today.day}",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    on_change=self.handle_change,
                )
            ),
            data = self.today,
        )


class NameDropdown:
    def __init__(self, page, phNameList, dropdown_changed):
        self.page = page
        self.phNameList = phNameList
        self.on_change = dropdown_changed

    def create(self):
        return ft.Dropdown(
            width=130,
            options=[],
            on_change=self.on_change,
            label="Name",
            border_color=ft.colors.BLUE_GREY_100
        )


class EndDrawer:
    def __init__(self, page):
        self.page = page

    def create(self):
        return ft.NavigationDrawer(
            position=ft.NavigationDrawerPosition.END,
            controls=[],
        )


        
# データ読み出し用のドロワー
class ReloadDrawer:
    def __init__(self,page):
        self.page = page
        
    def create(self):
        return ft.NavigationDrawer(
            position = ft.NavigationDrawerPosition.END,
            controls = [
                    ft.Container(ft.ListTile(
                        title = ft.Text("この端末に保管されているデータ")
                    ))
                    ],
        )
        
class AmDropDown:
    def create(self):
        return ft.ResponsiveRow(
            [
                ft.Checkbox(label="ICU",col = {"sm": 6, "md": 4, "xl": 2},data = "ICU"),
                ft.Checkbox(label="3A",col = {"sm": 6, "md": 4, "xl": 2},data = "3A"),
                ft.Checkbox(label="3B",col = {"sm": 6, "md": 4, "xl": 2},data = "3B"),
                ft.Checkbox(label="3C",col = {"sm": 6, "md": 4, "xl": 2},data = "3C"),
                ft.Checkbox(label="CCU",col = {"sm": 6, "md": 4, "xl": 2},data = "CCU"),
                ft.Checkbox(label="4A",col = {"sm": 6, "md": 4, "xl": 2},data = "4A"),
                ft.Checkbox(label="4B",col = {"sm": 6, "md": 4, "xl": 2},data = "4B"),
                ft.Checkbox(label="4C",col = {"sm": 6, "md": 4, "xl": 2},data  = "4C"),
                ft.Checkbox(label="4D",col = {"sm": 6, "md": 4, "xl": 2},data = "4D"),
                ft.Checkbox(label="HCU",col = {"sm": 6, "md": 4, "xl": 2},data = "HCU"),
                ft.Checkbox(label="5A",col = {"sm": 6, "md": 4, "xl": 2},data = "5A"),
                ft.Checkbox(label="5B",col = {"sm": 6, "md": 4, "xl": 2},data = "5B"),
                ft.Checkbox(label="5C",col = {"sm": 6, "md": 4, "xl": 2},data = "5C"),
                ft.Checkbox(label="5D",col = {"sm": 6, "md": 4, "xl": 2},data = "5D"),
            ]
        )


class PmDropDown:
    def create(self):
        return ft.ResponsiveRow(
            [
                ft.Checkbox(label="ICU",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="3A",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="3B",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="3C",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="CCU",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="4A",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="4B",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="4C",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="HCU",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="5A",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="5B",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="5C",col = {"sm": 6, "md": 4, "xl": 2}),
                ft.Checkbox(label="5D",col = {"sm": 6, "md": 4, "xl": 2}),
            ]
        )


# editButton
class EditButton:
    def __init__(self, page, toggle_delete_button):
        self.page = page
        self.toggle_delete_button = toggle_delete_button

    def create(self, e):
        return ft.IconButton(
            icon=ft.icons.EDIT, on_click=lambda e: self.toggle_delete_button
        )


class DeleteButtons:
    def __init__(self, page, delete_content):
        self.page = page
        self.delete_content = delete_content

    def create(self):
        return ft.IconButton(
            icon=ft.icons.DELETE,
            visible=False,
            icon_color="red",
            icon_size=20,
            on_click=lambda e: self.delete_content(e),
        )


class CreateCounter:
    def __init__(self, page, count_field):
        self.page = page
        self.count_field = count_field

    def create(self, e):
        return ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: self.counterPlus(
                        e, self.count_field, count_dict
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                self.count_field,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: self.counterMinus(
                        e, self.count_field, cont_dict
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedReactangleBorder(radius=5)),
                ),
            ]
        )
