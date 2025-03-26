import flet as ft
import json
class Trashdata_ExpantionPanel:
    @staticmethod
    def create_expantion_panel(page):
        try:
            data=page.client_storage.get("delete_drag")
            load=json.loads(data)
        except:
            load={}

        panel=[]
        try:
            for key in load.keys():
                panel.append(
                    ft.ListTile(
                        title=ft.Text(key),
                        subtitle=ft.Text(f"削除日: {load[key]['delete']}"),
                        trailing=ft.IconButton(
                            ft.icons.RESTORE,
                            data=key,
                            tooltip="復元する",
                        )
                    )
                )
        except:
            panel = [
                ft.ListTile(
                    title=ft.Text("削除されたデータはありません"),
                )
            ]
        return panel