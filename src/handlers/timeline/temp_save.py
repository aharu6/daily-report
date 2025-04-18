#端末に保存するだけのボタンを作成する
#保存したらメッセージを表示する
import json
from handlers.timeline.hide_message import HideMessageHandler
from datetime import datetime
class Temp_Save:
    @staticmethod
    def on_save(
        e,
        times,
        amTime,
        select_day,
        columns,
        drag_data,
        count_dict,
        custumDrawerAm,
        custumDrawerPm,
        phName,
        page,
        comment_dict,
        message,
        update_location_data,
        radio_selected_data,
    ):
        if isinstance(select_day.data, str):
            select_day.data = datetime.strptime(select_day.data, "%Y-%m-%d")
            
        date = f"{select_day.data.year}-{select_day.data.month}-{select_day.data.day}"
        # 初期ベースの作成
            # 時間
        time_for_label = times
        # 初期ベースの作成
        set_data = [
            {
                "time": time_for_label[i],
                "task": "",
                "count": 0,
                "locate": "AM" if time_for_label[i] in amTime else "PM",
                "date": str(date),
                "PhName": "",
                "comment": "",
            }
            for i in range(len(columns))
        ]
            # リストを辞書形式に変換
        data_dict = {record["time"]: record for record in set_data}
            # 辞書データの更新
            # taskデータの書き込み
            # willacceptのみの記載の場合、前後のtaskを埋める挙動
            
        for time, task_data in drag_data.items():
            if time in data_dict:
                data_dict[time]["task"] = task_data["task"]
                
        
        # countデータの書き込み
        for time, count in count_dict.items():
            if time in data_dict:
                data_dict[time]["count"] = count["count"]

        # 病棟データの書き込み
        #　taskがある時のみ書き込む
        # AMの場合
        list_am_location_data = []
        for i in range(len(custumDrawerAm.content.controls)):
            if custumDrawerAm.content.controls[i].value == True:
                list_am_location_data.append(custumDrawerAm.content.controls[i].label)
            else:
                None

        for time in data_dict.keys():
            if list_am_location_data is not None:
                if data_dict[time]["locate"] == "AM":
                    if data_dict[time]["task"] != "":
                        data_dict[time]["locate"] = list_am_location_data
                    else:
                        pass
            else:
                None

            # PMの場合
        list_pm_location_data = []
        for i in range(len(custumDrawerPm.content.controls)):
            if custumDrawerPm.content.controls[i].value == True:
                list_pm_location_data.append(custumDrawerPm.content.controls[i].label)
            else:
                None

        for time in data_dict.keys():
            if list_pm_location_data is not None:
                if data_dict[time]["locate"] == "PM":
                    if data_dict[time]["task"] != "":
                        data_dict[time]["locate"] = list_pm_location_data
                    else:
                        pass
            else:
                None
                
        #ラジオボタンでの病棟選択データを反映
        #単数選択時もリスト形式に変換して保存する
        update_loc_list = []
        for time in data_dict.keys():
            if time in update_location_data:
                update_loc_list.append(update_location_data[time])
                data_dict[time]["locate"] = update_loc_list
            else:
                pass

        # phName データの書き込み
        for time in data_dict.keys():
            try:
                data_dict[time]["phName"] = phName.value
            except:
                data_dict[time]["phName"] = ""
        
        #pre_dataにdata_dictを追加
        #形式：日付と名前にて一意に
        #{date_phName}:data_dict} 
        try:
            data_key = f"{date}_{phName.value}"
        except:
            data_key = f"{date}_NoName"
        
        try:
            old_data = page.client_storage.get("timeline_data")
            save_data = json.loads(old_data)
            save_data[data_key] = data_dict
        except:
            save_data = {}  
            save_data[data_key] = data_dict
            
        # その他コメントの書き込み
        for time, comment_data in comment_dict.items():
            if time in data_dict:
                data_dict[time]["comment"] = comment_data["comment"]
        
        #変更後のデータを保管する
        #コメントのデータが入っている？
        #save_client_storageの時はwill_acceptを変換する前の状態にて保存すれば読み込み時に再度変換する必要なく楽かも
        page.client_storage.set(
            "timeline_data", json.dumps(save_data, ensure_ascii=False)
            )
        
        #locateデータ（全体選択）は別に保管しておく
            #初期ベースの作成
            #紐付けはdate_nameのdata_keyにて共通させる
        try:
            pre_old_location_data = page.client_storage.get("location_data")
            old_location_data = json.loads(pre_old_location_data)
            dict_location_data=old_location_data|{data_key:{
                "locate_AM":[],
                "locate_PM":[],
            }}
        except:
            dict_location_data = {
                data_key: {
                    "locate_AM": [],
                    "locate_PM": [],
                }
            }
        dict_location_data[data_key]["locate_AM"] = [
            control.label for control in custumDrawerAm.content.controls if control.value
        ]
        dict_location_data[data_key]["locate_PM"] = [
            control.label for control in custumDrawerPm.content.controls if control.value
        ]
        page.client_storage.set(
            "location_data",
            json.dumps(dict_location_data, ensure_ascii=False)
        )
        #radio_selected_dataの保存
        try:
            preload = page.client_storage.get("radio_selected_data")
            load_radio_data = json.loads(preload)
            # 新規データを追加していくと増えるだけだから、日付データにてフィルタして削除する
        except:
            load_radio_data = {}

        #radio_selected_dataのキーをdate_nameのキーに変更（削除時の挙動と合わせるため）
        selected_data = {data_key:radio_selected_data}
        #新規データを結合
        marge_radio_dict=load_radio_data|selected_data
        page.client_storage.set("radio_selected_data", json.dumps(marge_radio_dict, ensure_ascii=False))

                    
        
        #保存できたら完了メッセージを表示
        #メッセージは一定時間経過後に削除
        message.content.controls[0].visible = True
        message.content.controls[1].visible = True  
        page.update()
        HideMessageHandler.hide_message(message,page)

