import flet as ft
from flet import View
class SettingPage:
    def __init__(self, driver):
        self.driver = driver
    def create(self):
        return ft.Container(
                ft.Text("Setting Page")
            )
        