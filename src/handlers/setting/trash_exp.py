import flet as ft
import json
from handlers.setting.restore_data import RestoreData

class Trashdata_ExpantionPanel:
    @staticmethod
    def create_expantion_panel(page):
        try:
            data=page.client_storage.get("delete_drag")
            load=json.loads(data)
        except:
            load={}
        try:
            location_data=json.loads(page.client_storage.get("delete_location"))
            radio_data=json.loads(page.client_storage.get("delete_radio"))
        except:
            location_data={}
            radio_data={}
        panel=[]    
        try:
            for key in load.keys():
                panel.append(
                    ft.ListTile(
                        title=ft.Text(key),
                        subtitle=ft.Text(f"削除日: {load[key]['delete']}      戻したい場合はここをクリック"),
                        trailing=ft.IconButton(
                            ft.icons.RESTORE,
                            tooltip="削除したデータを復元します",
                        ),
                        data={
                                "key":key,
                                "data":load[key],
                                "location_data":location_data[key],
                                "radio_data":radio_data[key]
                                },
                        on_click=lambda e: RestoreData.restore_data(e=e,page=page)
                    )
                )
        except:
            panel = [
                ft.ListTile(
                    title=ft.Text("削除されたデータはありません"),
                )
            ]
        return panel