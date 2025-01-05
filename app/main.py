import flet as ft
from flet import Page, AppBar, View, Text, ScrollMode
import json
import calendar
import csv
import pandas as pd
import sqlite3
import datetime
import sys
from tkinter import filedialog
from components.components import (
    DateComponent,
    NameDropdown,
    EndDrawer,
    AmDropDown,
    PmDropDown,
    EditButton,
    DeleteButtons,
)
from handlers.handlers import Handlers
from handlers.handlersMain import Handlers_Main
from handlers.handlers_chart import Handlers_Chart
from models.models import DataModel
from view.timeline_page import TimelinePage
from view.setting_page import SettingPage


# main
def main(page: ft.Page):

    page.title = "Daily Report"
    page.window.width = 1400
    page.window.height = 800
    page.scroll = True

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.HOVERED: ft.colors.BLUE_GREY_50,
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.BLUE_GREY_50,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.HOVERED: None,
                ft.MaterialState.DEFAULT: ft.colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )
    today = datetime.date.today()

    model = DataModel()

    file_picker = ft.FilePicker(
        on_result=lambda e: Handlers_Chart.pick_file_result(
            e, selected_files, bar_chart
        )
    )
    page.overlay.append(file_picker)

    selected_files = ft.Text()
    file_picker_Button = ft.ElevatedButton(
        "ファイルを選択",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )

    bar_chart = ft.BarChart(
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

    def route_change(e):
        page.on_view_pop = view_pop
        page.views.clear()
        if page.route == "/":
            page.views.append(TimelinePage(page).create())
        elif page.route == "/chart":
            print("chart", page.views)
            page.views.append(
                View(
                    "/chart",
                    [
                        file_picker_Button,
                        selected_files,
                        bar_chart,
                        # chartPage,
                        ft.CupertinoNavigationBar(
                            selected_index=1,
                            bgcolor=ft.colors.BLUE_GREY_50,
                            inactive_color=ft.colors.GREY,
                            active_color=ft.colors.BLACK,
                            on_change=lambda e: Handlers_Main().on_navigation_change(
                                e, page
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
                )
            )
        if page.route == "/settings":
            page.views.append(SettingPage(page).create())
        page.update()

    def view_pop(e):
        page.views.pop()
        page.views.clear()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.BLUE_GREY_50,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        on_change=lambda e: Handlers_Main().on_navigation_change(e, page),
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
                selected_icon=ft.icons.BOOKMARK,
                label="Settings",
            ),
        ],
    )
    page.go(page.route)


ft.app(main)
