import flet as ft
from flet import Page, AppBar, View, Text, ScrollMode
import datetime
from components.components import (
    DateComponent,
    NameDropdown,
    EndDrawer,
    AmDropDown,
    PmDropDown,
    EditButton,
    DeleteButtons,
)
from handlers.handlersMain import Handlers_Main
from models.models import DataModel
from view.timeline_page import TimelinePage
from view.setting_page import SettingPage
from view.chart_page import ChartPage

# main
def main(page: ft.Page):

    page.title = "Daily Report"
    page.window.width = 1400
    page.window.height = 1000
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
            thickness=15,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )
    today = datetime.date.today()

    model = DataModel()

    def route_change(e):
        page.on_view_pop = view_pop
        page.views.clear()
        if page.route == "/":
            page.views.append(TimelinePage(page).create())
        elif page.route == "/chart":
            print("chart", page.views)
            page.views.append(ChartPage(page).create())
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
