import flet as ft
from flet import View
import datetime
from handlers.handlersMain import Handlers_Main
from handlers.handlers_chart import Handlers_Chart
from components.compoments_chart import ComponentChart
from tkinter import filedialog
class ChartPage:
    def  __init__(self,page):
        self.page = page
        self.file_picker = ft.FilePicker(
            on_result=lambda e: Handlers_Chart.pick_file_result(
                e, self.selected_files, self.bar_chart
            )
        )
        self.file_picker_Button = ft.ElevatedButton(
            "ファイルを選択",
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=True),
        )
        self.selected_files = ft.Text()
        self.bar_chart = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.colors.GREEN_100),
            left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Count"), title_size=20),
            bottom_axis=ft.ChartAxis(labels_size=40),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREEN_100, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREEN_100),
            max_y=10,
            interactive=True,
            expand=True,
        )
        self.page.overlay.append(self.file_picker)

        
        
    def create(self):
        return View(
            "/chart",
            [
                self.file_picker_Button,
                self.selected_files,
                self.bar_chart,
                # chartPage,
                ft.CupertinoNavigationBar(
                    selected_index=1,
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
            ]
        )