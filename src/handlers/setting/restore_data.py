import json
class RestoreData:
    @staticmethod
    def restore_data(e,page):
    #元に戻すボタンを押した時にデータを復元する機能
    #timeline_dataの復元
        try:
            #元に戻す先
            load=json.loads(page.client_storage.get("timeline_data"))
            #日付＿名前の紐付けに直す deleteを除いたデータを作る
            #復活させる対象のデータ
            #"delete"を削除
            restore_data=e.control.data["data"]
            del restore_data['delete']
            #date_nameのキーを加えて元の形に戻しつつ、データを追加
            load[e.control.data["key"]]=restore_data
            page.client_storage.set("timeline_data",json.dumps(load))
            
        except:
            pass
        #↑をdelete_dragから削除
        try:
            load_delete=json.loads(page.client_storage.get("delete_drag"))
            del load_delete[e.control.data["key"]]
            page.client_storage.set("delete_drag",json.dumps(load_delete))
        except:
            pass


        #location_dataの復元
        try:
            location_data=json.loads(page.client_storage.get("location_data"))
            #復元させる対象の病棟データ
            restore_location_data=e.control.data["location_data"]
            del restore_location_data['delete']
            location_data[e.control.data["key"]]=restore_location_data
            page.client_storage.set("location_data",json.dumps(location_data))
        except:
            pass
        #↑をdelete_locationから削除
        try:
            delete_location_data=json.loads(page.client_storage.get("delete_location"))
            del delete_location_data[e.control.data["key"]]
            page.client_storage.set("delete_location",json.dumps(delete_location_data))
        except:
            pass


        #radio_dataの復元
        try:
            radio_data=json.loads(page.client_storage.get("radio_selected_data"))
            #復元させる対象のラジオデータ
            restore_radio_data=e.control.data["radio_data"]
            del restore_radio_data['delete']
            radio_data[e.control.data["key"]]=restore_radio_data
            page.client_storage.set("radio_selected_data",json.dumps(radio_data))
        except:
            pass
        #↑をdelete_radioから削除
        try:
            delete_radio_data=json.loads(page.client_storage.get("delete_radio"))
            del delete_radio_data[e.control.data["key"]]
            page.client_storage.set("delete_radio",json.dumps(delete_radio_data))
        except:
            pass
    
    #元に戻したデータ項目はlistTileから削除


