import flet as ft
from flet import View
from components.components_setting import Panel


class SettingPage:
    def __init__(self, page):
        self.page = page
        self.panel = Panel(page).create()

    def create(self):
        return ft.Container(ft.Text("Setting Page"), self.panel)
