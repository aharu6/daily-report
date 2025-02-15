import flet as ft
from flet import AppBar,ElevatedButton,View,Page,Text
def main(page:ft.Page):
    def on_navigation_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/chart")
        elif selected_index == 1:
            page.go("/settings") 
        
    page.title = 'Hello World'
    text  = ft.Text('Hello World')  
    reset_button = ft.ElevatedButton(
        text = "Reset",
    )  
    text_field = ft.TextField()
    rail = ft.NavigationRail(
        selected_index = 0,
        label_type = ft.NavigationRailLabelType.ALL,
        min_width = 80,
        min_extended_width = 100,
        leading = ft.FloatingActionButton(
            icon = ft.icons.CREATE,text = "Create",
            #timelimeページを展開する,
            on_click = lambda e:page.go("/")
            ),
        group_alignment = -0.9,
        extended = True,
        on_change = on_navigation_change,
        destinations = [
            ft.NavigationRailDestination(icon = ft.icons.SHOW_CHART, label = 'Showchart'),
            ft.NavigationRailDestination(icon = ft.icons.SETTINGS, label = 'Settings'),
        ]
    )
    
    #リセットボタンを追加する
    #画面の再描画を行う
    
    #ページを更新する
    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    ft.Row(
                        [   
                            reset_button,
                            rail,
                            ft.VerticalDivider(),
                            ft.Text("Home"),
                            text_field,
                        ],
                        height = 600
                    )
                ],
            )
        )
        if page.route == "/chart":
            page.views.clear()
            page.views.append(
                View(
                    "/chart",
                    [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(),
                                ft.Text("Chart"),
                            ],
                            height = 600
                        )
                    ],
                )
            )
        if page.route == "/settings":
            page.views.clear()
            page.views.append(
                View(
                    "/settings",
                    [
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(),
                                ft.Text("Settings"),
                            ],
                            height = 600
                        )
                    ]
                )
            )
        page.update()
    
    
    def show_chart_page(e):
        page.go("/chart")
    
    def view_pop(e):
        page.views.pop()
        print("page_clear")
        
    def reset_page(e):
        view_pop(e)
        page.views.append(
            View(
                "/",
                [
                    ft.Row(
                        [   
                            reset_button,
                            rail,
                            ft.VerticalDivider(),
                            ft.Text("Home"),
                            text_field,
                        ],
                        height = 600
                    )
                ],
            )
        )
        page.update()
    
    reset_button.on_click = lambda e: reset_page(e)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.go(page.route)
    
ft.app(main)