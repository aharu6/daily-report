import flet as ft
from flet import View
import datetime
from handlers.handlersMain import Handlers_Main
from handlers.chart.handlers_chart import Handlers_Chart
from components.compoments_chart import FilePickCard,FileNameCard
import asyncio as aio
from handlers.chart.download_handler import Chart_Download_Handler

class ChartPage:
    def __init__(self, page):
        self.page = page

        # データフレームを定義しておく
        # ファイルのアップロードにてデータフレームの作成まで
        self.dataframe = None
        self.file_picker_Button = ft.TextButton(
            "ファイルを選択",
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=True),
        )
        self.select = ft.Row(
            controls=[
                FilePickCard(self.file_picker_Button).create(),
                FileNameCard().create(),
            ],
            alignment=ft.MainAxisAlignment.END,
        )

        self.file_picker = ft.FilePicker(
            on_result=lambda e: Handlers_Chart.pick_file_result(
                e, self.selected_files, self,
                self.select.controls[1],
            )
        )
        self.selected_files = ft.Text()
        self.page.overlay.append(self.file_picker)
        
        self.subtitle = ft.Text("集計", size = 20)
        self.horizon_subtitle = ft.Divider()
        self.chart1_field = ft.ResponsiveRow()

        self.chart1card = ft.Card(
            content=ft.TextButton(
                "グラフを生成",
                on_click=lambda _: Handlers_Chart.ComponentChart_for_standard(
                    dataframe=self.dataframe,chart_field= self.chart1_field,page= page,
                ),
            )
        )
        

        self.subtitle2 = ft.Text("病棟ごとの集計",size = 20)
        self.chart2_field = ft.ResponsiveRow(controls=[])
        self.chart2card = ft.Card(
            content=ft.TextButton(
                "グラフを生成",
                on_click=lambda _: Handlers_Chart.ComponentChart_for_location(
                    self.dataframe, self.chart2_field, page
                ),
            )
        )

        self.subtitle3 = ft.Text("個人ごとの集計",size = 20)
        self.chart3_field = ft.ResponsiveRow()
        # あとでファイルを選択していない状態でボタンを押したときにはエラーメッセージを表示するようにする
        self.chart3card = ft.Card(
            content=ft.TextButton(
                "グラフを生成",
                on_click=lambda _: Handlers_Chart.ComponentChart_for_self(
                    self.dataframe, self.chart3_field,page
                ),
            )
        )
    
    def create(self):
        return View(
            "/chart",
            [
                self.select,
                self.selected_files,
                self.subtitle,
                self.horizon_subtitle,
                self.chart1card,
                self.chart1_field,
                self.subtitle2,
                self.horizon_subtitle,
                self.chart2card,
                self.chart2_field,
                self.subtitle3,
                self.horizon_subtitle,
                self.chart3card,
                self.chart3_field,
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
            ],
            scroll=True,
        )
