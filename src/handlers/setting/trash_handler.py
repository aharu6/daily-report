import json
import datetime
#設定ページ読み込み時に30日経過したゴミ箱データは削除する
#delete_dragデータは設定ページと紐づいている
class TrashDataHandler:
    @staticmethod
    def delete_trash_data(page):
        try:
            drag_data=page.client_storage.get("delete_drag")
            load=json.loads(drag_data)

            location_data=json.loads(page.client_storage.get("delete_location"))

            radio_data=json.loads(page.client_storage.get("delete_radio"))

        except:
            pass
        try:
            today=datetime.date.today()
            for key in load.keys():
                if "delete" in load[key].keys():
                    load_day=load[key]["delete"]
                    old_day = datetime.datetime.strptime(load_day, "%Y-%m-%d").date()
                    if (today-old_day).days>30:
                        del load[key]
                if "delete" in location_data[key].keys():
                    load_day=location_data[key]["delete"]
                    old_day = datetime.datetime.strptime(load_day, "%Y-%m-%d").date()
                    if (today-old_day).days>30:
                        del location_data[key]
                if "delete" in radio_data[key].keys():
                    load_day=radio_data[key]["delete"]
                    old_day = datetime.datetime.strptime(load_day, "%Y-%m-%d").date()
                    if (today-old_day).days>30:
                        del radio_data[key]
                        
            page.client_storage.set("delete_drag",json.dumps(load))
            page.client_storage.set("delete_location",json.dumps(location_data))
            page.client_storage.set("delete_radio",json.dumps(radio_data))
        except:
            pass
