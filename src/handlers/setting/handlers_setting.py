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
                    trailing=ft.iconButton(
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
    def add_name(e, phNameList, name_field, page, dialog, panel):
        #半角と全角の空白は除去する
        new_name = name_field.value.strip()
        delspace1 = new_name.replace("　","")
        delspace2 = delspace1.replace(" ","")
        if delspace2:
            phName_List = (
                json.loads(phNameList) if isinstance(phNameList, str) else phNameList
            )
            phName_List.append({"name": delspace2})
            page.client_storage.set("phName", json.dumps(phName_List))
            name_field.value = ""
            Handlers_setting.update_ListTile(panel, phNameList=phName_List, page=page)
            dialog.open = False
            page.update()
            
    @staticmethod
    def update_datatable(panel,page):
        cells = []
        try:
            load_data = page.client_storage.get("timeline_data")
        except:
            load_data={}
        try:
            dat = json.loads(load_data) 
        except:
            dat = {}
        
        cells = [
            ft.DataRow(
                cells = [
                    ft.DataCell(ft.Text(i)),
                    ft.DataCell(ft.iconButton(
                        ft.icons.DELETE,
                        on_click = lambda e:Handlers_setting.delete_data(e,page,panel),
                        data = i,
                        ))
                ]
            )
            for i in list(dat.keys())
        ]
        panel.controls[1].content.rows = cells

    @staticmethod   
    def delete_data(e,page,panel):
        import datetime
        #該当のkey:date_name
        key = e.control.data
        #削除時の日付データを加える
        today = datetime.date.today()

        #client_storageから該当データを削除する
        try:
            dat = json.loads(page.client_storage.get("timeline_data"))
        except:
            dat = {}
        
        try:
            delete_drag_data = json.loads(page.client_storage.get("delete_drag"))
        except:
            delete_drag_data = {}

        dat[key]["delete"] = today.strftime("%Y-%m-%d")
        delete_drag_data.update({key:dat[key]})
        page.client_storage.set("delete_drag",json.dumps(delete_drag_data))
        
        del dat[key]
        #削除した新しいデータをclient_storageに保存
        page.client_storage.set("timeline_data",json.dumps(dat))
        #Datatableから該当の行を削除する
        Handlers_setting.update_datatable(panel,page)
        
        
        #病棟全体選択データの削除
        try:
            load_location_data=json.loads(page.client_storage.get("location_data"))
        except:
            load_location_data={}

        try:
            delete_location_data=json.loads(page.client_storage.get("delete_location"))
        except:
            delete_location_data={}

        load_location_data[key]["delete"]=today.strftime("%Y-%m-%d")
        delete_location_data.update({key:load_location_data[key]})
        page.client_storage.set("delete_location",json.dumps(delete_location_data))
        #削除した新しいデータをclient_storageに保存
        try:
            del load_location_data[key]
            page.client_storage.set("load_location_data",json.dumps(load_location_data))        
        except:
            pass
        
        #radiobuttonを用いた病棟単数選択データの削除
        try:
            load_radio_data=json.loads(page.client_storage.get("radio_selected_data"))
        except:
            load_radio_data={}
        
        try:
            delete_radio_data=json.loads(page.client_storage.get("delete_radio"))
        except:
            delete_radio_data={}
        
        load_radio_data[key]["delete"]=today.strftime("%Y-%m-%d")
        delete_radio_data.update({key:load_radio_data[key]})
        page.client_storage.set("delete_radio",json.dumps(delete_radio_data))
        #削除した新しいデータをclient_storageに保存
        try:        
            del load_radio_data[key]
            page.client_storage.set("radio_selected_data",json.dumps(load_radio_data))
        except:
            pass

        page.update()
        
    
