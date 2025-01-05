import flet as ft
import datetime
import json
from models.models import DataModel
from handlers.handlers_setting import Handlers_setting


class Title:
    def __init__(self, page):
        self.page = page

    def create(self):
        return ft.Text(
            "保存データの削除など",
            size=20,
            weight=ft.FontWeight.BOLD,
        )


class Panel:
    def __init__(self, page):
        self.page = page

    def create(self, phNameList, page):
        # phNameLIst が文字列の場合、リストに変換
        if isinstance(phNameList, str):
            phNameList = json.loads(phNameList)

        return ft.ExpansionPanelList(
            elevation=8,
            divider_color="#D6EFD8",
            controls=[
                ft.ExpansionPanel(
                    bgcolor=None,
                    header=ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON),
                        title=ft.Text("ユーザー名の編集"),
                    ),
                    content=ft.Column(
                        # 名前があれば保存しているデータを呼び出す
                        # なければadd_nameを表示
                        controls=[]
                        + (
                            [
                                ft.ListTile(
                                    title=ft.Text("名前が登録されていません"),
                                )
                            ]
                            if not phNameList
                            else []
                        ),
                    ),
                ),
                ft.ExpansionPanel(
                    bgcolor=None,
                    header=ft.ListTile(
                        leading=ft.Icon(ft.icons.STORAGE),
                        title=ft.Text("保存データの削除"),
                    ),
                ),
            ],
        )
