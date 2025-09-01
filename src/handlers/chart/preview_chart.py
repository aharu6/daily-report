import tempfile
import webbrowser
import os
import flet as ft
from flet.plotly_chart import PlotlyChart
class PreviewChartHandler:
    @staticmethod
    #flet の内蔵ダイアログを使用した拡大表示
    def preview_chart(chart,page):
        dialog = ft.AlertDialog(
            title=ft.Text("Chart Preview"),
            content=ft.Container(
                content=PlotlyChart(
                    chart,
                    expand=True,
                    original_size=True,
                    isolated=True,
                ),
            ),
            actions=[
                ft.TextButton("Close",on_click=lambda e: page.close(dialog))
            ],
            modal=True
        )
        page.open(dialog)
