import json
import datetime
import flet as ft
import csv
import pandas as pd
from models.models import DataModel


class Handlers_setting:
    @staticmethod
    def delete_name(e, phNameList, page, panel):
        print("delete_name")
        print(e.control.data)
        # e.control.dataに該当する名前をphNamelistから削除
        new_phNameList = [item for item in phNameList if item["name"] != e.control.data]
        page.client_storage.set("phName", json.dumps(new_phNameList))
        Handlers_setting.update_ListTile(panel, new_phNameList, page)

    @staticmethod
    def update_ListTile(panel, phNameList, page):
        controls = []
        if isinstance(phNameList, str):
            phNameList = json.loads(phNameList)

        try:

            controls = [
                ft.ListTile(
                    title=ft.Text(f"{item['name']}"),
                    trailing=ft.IconButton(
                        ft.icons.DELETE,
                        on_click=lambda e: Handlers_setting.delete_name(
                            e, phNameList, page, panel
                        ),
                        data=item["name"],
                    ),
                )
                for item in phNameList
            ]

        except:
            controls = [
                ft.ListTile(
                    title=ft.Text("名前が登録されていません"),
                )
            ]

        controls.append(
            ft.ListTile(
                title=ft.Text("名前を追加"),
                on_click=lambda e: DataModel().add_name(page, panel),
            )
        )
        panel.controls[0].content.controls = controls
        page.update()
