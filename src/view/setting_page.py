import flet as ft
from flet import View
from handlers.timeline.handlers import Handlers
from handlers.handlersMain import Handlers_Main
from handlers.setting.handlers_setting import Handlers_setting
from components.components_setting import Panel, Title
from models.models import DataModel


class SettingPage:
    def __init__(self, page):
        self.page = page
        self.title = Title(self)
        self.horizon = ft.Divider()
        self.model = DataModel()
        self.phNameList = self.model.load_data(page)
        self.panel = Panel(self).create(self.phNameList, page)
        Handlers_setting.update_ListTile(self.panel, self.phNameList, page)
        # panelのcontrolsの最後のlistTileにon_click関数を追加する
        self.panel.controls[0].content.controls[-1].on_click = (
            lambda e: Handlers_setting.open_dialog(e, self.dialog, page)
        )

        self.name_filed = ft.TextField(label="新しく追加する名前を入力してください")
        self.dialog = ft.AlertDialog(
            title=ft.Text("Add Name"),
            content=self.name_filed,
            actions=[
                ft.TextButton(
                    "追加",
                    on_click=lambda e: Handlers_setting.add_name(
                        e,
                        self.phNameList,
                        self.name_filed,
                        page,
                        self.dialog,
                        self.panel,
                    ),
                ),
                ft.TextButton(
                    "キャンセル",
                    on_click=lambda e: Handlers_setting.close_dialog(
                        e, self.dialog, page
                    ),
                ),
            ],
        )
        Handlers_setting.update_datatable(self.panel, page)
        

    def create(self):
        return View(
            "/settings",
            [
                self.title.create(),
                self.horizon,
                self.panel,
                self.dialog,
                ft.CupertinoNavigationBar(
                    selected_index=2,
                    bgcolor=ft.colors.BLUE_GREY_50,
                    inactive_color=ft.colors.GREY,
                    active_color=ft.colors.BLACK,
                    on_change=lambda e: Handlers_Main().on_navigation_change(
                        e, self.page
                    ),
                    destinations=[
                        ft.NavigationBarDestination(
                            icon=ft.icons.CREATE,
                            label="Create",
                            selected_icon=ft.icons.BORDER_COLOR,
                        ),
                        ft.NavigationBarDestination(
                            icon=ft.icons.SHOW_CHART,
                            label="Showchart",
                            selected_icon=ft.icons.AUTO_GRAPH,
                        ),
                        ft.NavigationBarDestination(
                            icon=ft.icons.SETTINGS,
                            selected_icon=ft.icons.SETTINGS_SUGGEST,
                            label="Settings",
                        ),
                    ],
                ),
            ],
            scroll=True,
        )
