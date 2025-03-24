import json
import datetime
#ページ読み込み時に30日経過したゴミ箱データは削除する
class TrashDataHandler:
    @staticmethod
    def delete_trash_data(page):
        try:
            drag_data=page.client_storage.get("delete_drag")
            load=json.loads(drag_data)
        except:
            pass
        try:
            today=datetime.date.today()
            print(today)
            for key in load.keys():
                if "delete" in load[key].keys():
                    load_day=load[key]["delete"]
                    old_day = datetime.datetime.strptime(load_day, "%Y-%m-%d").date()
                    print(today-old_day)
                    if (today-load[key]["delete"]).days>30:
                        del load[key]
        except:
            pass
