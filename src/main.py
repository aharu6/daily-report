import flet as ft
from flet import Page, AppBar, View, Text

from handlers.handlersMain import Handlers_Main
from view.timeline_page import TimelinePage
from view.setting_page import SettingPage
from view.chart_page import ChartPage

# main
def main(page: ft.Page):

    page.title = "業務日誌"
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

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            # 遅延生成: 必要なときにのみページを生成
            page.views.append(TimelinePage(page).create())
        elif page.route == "/chart":
            # 遅延生成: 必要なときにのみページを生成
            page.views.append(ChartPage(page).create())
        elif page.route == "/settings":
            # 遅延生成: 必要なときにのみページを生成
            page.views.append(SettingPage(page).create())
        page.update()

    def view_pop(e):
        page.views.pop()
        # 不要なリソースを解放
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
                icon=ft.icons.TIMELINE,
                label="Timeline",
                selected_icon=ft.icons.BORDER_COLOR,
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.AUTO_GRAPH,
                label="Chart",
                selected_icon=ft.icons.AUTO_GRAPH,
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.SETTINGS,
                label="Settings",
            ),
        ],
    )
    # 初期ページを遅延生成
    page.go("/")


ft.app(main)
