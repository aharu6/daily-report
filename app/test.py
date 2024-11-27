import flet as ft

def main(page):
    rail = ft.NavigationRail(
        selected_index = 0,
        expand = True,
        destinations = [
            ft.NavigationRailDestination(icon = ft.icons.EDIT,selected_icon = ft.icons.BORDER_COLOR,label = "Edit")
        ]
    )
    
    page.add(rail,ft.Divider(),ft.Text("Hello World"))
ft.app(target = main)