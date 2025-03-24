import flet as ft
import datetime
from models.models import DataModel
from handlers.timeline.handlers import Handlers


class DateComponent:
    def __init__(self, page, today, handle_change):
        self.page = page
        self.today = today
        self.handle_change = handle_change

    def create(self):
        return ft.TextButton(
            text=f"{self.today.year}/{self.today.month}/{self.today.day}",
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    on_change=self.handle_change,
                )
            ),
            data=self.today,
        )

    """
    ft.ElevatedButton(
            text=f"{self.today.year}/{self.today.month}/{self.today.day}",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    on_change=self.handle_change,
                )
            ),
            data = self.today,
        )
        
        ft.Column(
            [
                ft.Icon(ft.icons.CALENDAR_MONTH),
                ft.ElevatedButton(
                    text=f"{self.today.year}/{self.today.month}/{self.today.day}",
                    on_click = lambda e: self.page.open(
                        ft.DatePicker(
                            on_change =lambda e: self.handle_change,
                        )
                    ),
                    data = self.today,
                ),
            ],
            width = 130,
            data = self.today,
        )

"""


class NameDropdown:
    def __init__(self, page, phNameList, dropdown_changed):
        self.page = page
        self.phNameList = phNameList
        self.on_change = dropdown_changed

    def create(self):
        return ft.Dropdown(
            width=130,
            options=[],
            on_change=self.on_change,
            label="Name",
            label_style=ft.TextStyle(color="#2a4d7b"),
            border_color=ft.colors.BLUE_GREY_100,
            color="#2a4d7b",
        )


class EndDrawer:
    def __init__(self, page):
        self.page = page

    def create(self):
        return ft.NavigationDrawer(
            position=ft.NavigationDrawerPosition.END,
            controls=[],
        )


# データ読み出し用のドロワー
class ReloadDrawer:
    def __init__(self, page):
        self.page = page

    def create(self):
        return ft.NavigationDrawer(
            position=ft.NavigationDrawerPosition.END,
            controls=[
                ft.Container(
                    ft.ListTile(title=ft.Text("この端末に保管されているデータ"))
                ),
                ft.Card(content = ft.Column()),
            ],
        )


# checkbox選択されたときに表示は削除する
# 選択が全て外されたときに再表示はどこでするか
from handlers.timeline.require_location import RequireLocationMessage

class AmDropDown:
    def create(self, require_location, page,am_total):
        return ft.ResponsiveRow(
            [
                ft.Checkbox(
                    label="ICU",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="ICU",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="OR",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="OR",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="HR",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="HR",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="1E",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="1E",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="3A",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="3A",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="3B",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="3B",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="3C",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="3C",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="CCU",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="CCU",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="4A",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="4A",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="4B",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="4B",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="4C",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="4C",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="4D",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="4D",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="HCU",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="HCU",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="5A",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="5A",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
                ft.Checkbox(
                    label="5B",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="5B",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="5C",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="5C",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="5D",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="5D",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="5D",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="5D",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total,
                    ),
                ),
                ft.Checkbox(
                    label="DI",
                    col={"sm": 6, "md": 4, "xl": 2},
                    data="5D",
                    on_change=lambda e: RequireLocationMessage.am_change_require_location(
                        e=e, require_location=require_location, page=page,total_num=am_total
                    ),
                ),
            ]
        )


class PmDropDown:
    def create(self, require_location, page,pm_total_num):
        return ft.ResponsiveRow(
            [
            ft.Checkbox(
                label="ICU",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="ICU",
            ),
            ft.Checkbox(
                label="OR",
                col={"sm": 6, "md": 4, "xl": 2},
                data="OR",
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
            ),
            ft.Checkbox(
                label="HR",
                col={"sm": 6, "md": 4, "xl": 2},
                data="HR",
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
            ),
            ft.Checkbox(
                label="1E",
                col={"sm": 6, "md": 4, "xl": 2},
                data="1E",
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
            ),
            ft.Checkbox(
                label="3A",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="3A",
            ),
            ft.Checkbox(
                label="3B",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="3B",
            ),
            ft.Checkbox(
                label="3C",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="3C",
            ),
            ft.Checkbox(
                label="CCU",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="CCU",
            ),
            ft.Checkbox(
                label="4A",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="4A",
            ),
            ft.Checkbox(
                label="4B",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="4B",
            ),
            ft.Checkbox(
                label="4C",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="4C",
            ),
            ft.Checkbox(
                label="4D",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="4D",
            ),
            ft.Checkbox(
                label="HCU",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="HCU",
            ),
            ft.Checkbox(
                label="5A",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="5A",
            ),
            ft.Checkbox(
                label="5B",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="5B",
            ),
            ft.Checkbox(
                label="5C",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="5C",
            ),
            ft.Checkbox(
                label="5D",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="5D",
            ),
            ft.Checkbox(
                label="5D",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="5D",
            ),
            ft.Checkbox(
                label="DI",
                col={"sm": 6, "md": 4, "xl": 2},
                on_change=lambda e: RequireLocationMessage.pm_change_require_location(
                e=e, require_location=require_location, page=page, total_num=pm_total_num,
                ),
                data="DI",
            ),
            ]
        )


# editButton
class EditButton:
    def __init__(self, page, toggle_delete_button):
        self.page = page
        self.toggle_delete_button = toggle_delete_button

    def create(self, e):
        return ft.IconButton(
            icon=ft.icons.EDIT, on_click=lambda e: self.toggle_delete_button
        )


class DeleteButtons:
    def __init__(
        self,
        page,
        delete_content,
        phNameList,
        phName,
        drag_data,
        count_dict,
        comment_dict,
        columns,
        draggable_data_for_move,
        comments,
        times,
        comment,
        draggable,
        update_location_data,
    ):
        self.page = page
        self.delete_content = delete_content
        self.phNameList = phNameList
        self.phName = phName
        self.drag_data = drag_data
        self.count_dict = count_dict
        self.comment_dict = comment_dict
        self.columns = columns
        self.draggable_data_for_move = draggable_data_for_move
        self.comments = comments
        self.times = times
        self.comment = comment
        self.draggable_data = draggable
        self.update_location_data = (update_location_data,)

    def create(self):
        return ft.IconButton(
            icon=ft.icons.DELETE,
            visible=False,
            icon_color="red",
            icon_size=20,
            on_click=lambda e: self.delete_content(
                e,
                self.page,
                self.phNameList,
                self.phName,
                self.drag_data,
                self.count_dict,
                self.comment_dict,
                self.columns,
                self.draggable_data_for_move,
                self.comments,
                self.times,
                self.comment,
                self.draggable_data,
                self.update_location_data,
            ),
        )


class CreateCounter:
    def __init__(self, page, count_field,count_dict):
        self.page = page
        self.count_field = count_field
        self.count_dict = count_dict

    def create(self, e):
        return ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: self.counterPlus(
                        e, self.count_field, self.count_dict
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                self.count_field,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: self.counterMinus(
                        e, self.count_field, self.cont_dict
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedReactangleBorder(radius=5)),
                ),
            ]
        )
