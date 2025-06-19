import flet as ft
from flet import View
import asyncio
from handlers.handlersMain import Handlers_Main
# main
def main(page: ft.Page):

    page.title = "業務見える化日誌"
    page.window.width = 1400
    page.window.height = 1000
    page.scroll = True

    def show_progress_bar():
        page.views.clear()
        page.views.append(
            View(
                "/loading",
                controls=[
                    ft.Column(
                        [
                            ft.Text("Loading..."),
                            ft.ProgressBar(width=200, height=20),
                        ],
                        alignment="certer",
                        horizontal_alignment="center",
                    )
                ],
            )
        )
        page.update()
    
    show_progress_bar()  # プログレスバーを表示
    
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
        # ページ生成処理
        page.views.clear()
        if page.route == "/":
            from view.timeline_page import TimelinePage
            page.views.append(TimelinePage(page).create())
        elif page.route == "/chart":
            from view.chart_page import ChartPage
            page.views.append(ChartPage(page).create())
        elif page.route == "/settings":
            from view.setting_page import SettingPage
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
    
    page.go("/")


ft.app(main)
