import json
import flet as ft
import pandas as pd

class Handlers_setting:
    @staticmethod
    def delete_name(e, phNameList, page, panel):
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
            )
        )
        panel.controls[0].content.controls = controls
        page.update()
    
    @staticmethod
    def open_dialog(e,dialog,page):
        dialog.open = True
        page.update()

    @staticmethod
    def add_name(e, phNameList, name_field, page, diaog, panel):
        new_name = name_field.value.strip()
        phName_List = (
            json.loads(phNameList) if isinstance(phNameList, str) else phNameList
        )
        if new_name:
            phName_List.append({"name": new_name})
            page.client_storage.set("phName", json.dumps(phName_List))
            name_field.value = ""
            Handlers_setting.update_ListTile(panel, phNameList=phName_List, page=page)
            diaog.open = False
            page.update()
