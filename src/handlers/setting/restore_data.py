import json
class RestoreData:
    @staticmethod
    def restore_data(e,page):
    #元に戻すボタンを押した時にデータを復元する機能
        try:
            #元に戻す先
            data=page.client_storage.get("timeline_data")
            load=json.loads(data)
            #日付＿名前の紐付けに直す deleteを除いたデータを作る
            #復活させる対象のデータ
            #"delete"を削除
            resave_data=e.control.data["data"]
            del resave_data['delete']
            #date_nameのキーを加えて元の形に戻しつつ、データを追加
            load[e.control.data["key"]]=resave_data
            page.client_storage.set("timeline_data",json.dumps(load))
            
        except:
            pass
        #↑をdelete_dragから削除
        try:
            delete_data=page.client_storage.get("delete_drag")
            load_delete=json.loads(delete_data)
            del load_delete[e.control.data["key"]]
            page.client_storage.set("delete_drag",json.dumps(load_delete))
        except:
            pass
    
    
    #元に戻したデータ項目はlistTileから削除
    

