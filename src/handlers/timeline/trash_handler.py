import json
#ページ読み込み時に30日経過したゴミ箱データは削除する
class TrashDataHandler:
    @staticmethod
    def delete_trash_data(page,date):
        try:
            drag_data=page.client_storage.get("delete_drag")
            load=json.loads(drag_data)
            print(load)
        except:
            pass
        try:
            for key in load.keys():
                if "delete" in load[key].keys():
                    print(load[key]["delete"])
                    if (date-load[key]["delete"]).days>30:
                        del load[key]
        except:
            pass
