from datetime import datetime
import json
import flet as ft
import pandas as pd

from handlers.timeline.hide_message import HideMessageHandler

class WriteCSVHandler:
    @staticmethod
    def write_csv_file(
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
        select_directory,
        save_error_message,
        require_location,
        require_name,
        save_message,
        update_location_data,
        radio_selected_data,
    ):
        if isinstance(select_day.data, str):
            select_day.data = datetime.strptime(select_day.data, "%Y-%m-%d")

        date = f"{select_day.data.year}-{select_day.data.month}-{select_day.data.day}"
        # 名前が入力されていない場合にはエラーを表示する
        if phName.value is None:
            save_error_message.content = ft.Text("名前を入力してください", color="red")
            page.update()
        else:
            save_error_message.content = None
            page.update()
            # 最後にデータベースに保管する

            # 入力された辞書データの長さ
            # first_key = list(drag_data.keys())[0]
            # first_value = drag_data[first_key]

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
            # AMの場合
            list_am_location_data = []
            for i in range(len(custumDrawerAm.content.controls)):
                if custumDrawerAm.content.controls[i].value == True:
                    list_am_location_data.append(
                        custumDrawerAm.content.controls[i].label
                    )
                else:
                    None
            for time in data_dict.keys():
                if list_am_location_data is not None:
                    if data_dict[time]["locate"] == "AM":
                        if data_dict[time]["task"] != "":
                            data_dict[time]["locate"] = list_am_location_data
                        else:
                            data_dict[time]["locate"] = []
                else:
                    None

                # PMの場合
            list_pm_location_data = []
            for i in range(len(custumDrawerPm.content.controls)):
                if custumDrawerPm.content.controls[i].value == True:
                    list_pm_location_data.append(
                        custumDrawerPm.content.controls[i].label
                    )
                else:
                    None

            # taskがある時のみ病棟データを書き込む
            for time in data_dict.keys():
                if list_pm_location_data is not None:
                    if data_dict[time]["locate"] == "PM":
                        if data_dict[time]["task"] != "":
                            data_dict[time]["locate"] = list_pm_location_data
                        else:
                            data_dict[time]["locate"] = []
                else:
                    None

                pass

            # ラジオボタンでの病棟選択データを反映,上書き
            # 単選択時もリスト形式に変換して保存する
            # 選択した時のみ上書きするように
            for time in data_dict.keys():
                update_loc_list = []
                if time in update_location_data:
                    update_loc_list.append(update_location_data[time])
                    data_dict[time]["locate"] = update_loc_list
                else:
                    pass

            # phName データの書き込み
            for time in data_dict.keys():
                if phName.value is not None:
                    data_dict[time]["phName"] = phName.value
                else:
                    data_dict[time]["phName"] = ""

            # その他コメントの書き込み
            for time, comment_data in comment_dict.items():
                if time in data_dict:
                    data_dict[time]["comment"] = comment_data["comment"]

            # 前のデータに追加していく形式へ
            # 追加前のデータ

            # pre_dataにdata_dictを追加
            # 形式：日付と名前にて一意に
            # {date_phName}:data_dict}
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

            # 変更後のデータを保管する
            # コメントのデータが入っている？
            # save_client_storageの時はwill_acceptを変換する前の状態にて保存すれば読み込み時に再度変換する必要なく楽かも
            # setなのでストレージがなくてもエラーにならない
            page.client_storage.set(
                "timeline_data", json.dumps(save_data, ensure_ascii=False)
            )
            # locateデータ（全体選択）は別に保管しておく
            # 初期ベースの作成
            try:
                pre_old_location_data=page.client_storage.get("location_data")
                old_location_data=json.loads(pre_old_location_data)
                dict_location_data=old_location_data|{str(date):{
                    "locate_AM":[],
                    "locate_PM":[],
                }}
            except:
                dict_location_data = {
                    str(date): {
                        "locate_AM": [],
                        "locate_PM": [],
                    }
                }

            dict_location_data[str(date)]["locate_AM"] = [
                control.label
                for control in custumDrawerAm.content.controls
                if control.value
            ]
            dict_location_data[str(date)]["locate_PM"] = [
                control.label
                for control in custumDrawerPm.content.controls
                if control.value
            ]
            page.client_storage.set(
                "location_data", json.dumps(dict_location_data, ensure_ascii=False)
            )

            #病棟選択データradio_selected_dataを保存
            #最初からデータフレームにて作成する
            #既存のデータフレームあれば読み込んで、追加、削除時は日付データでフィルタして削除するか
            #初回データの作成
            #radio_selected_data = pd.DataFrame([[date, "", ""]], columns=["date", "time", "locate"])
            #radio_selected_dataをデータフレームに変換
            # 行列を入れ替える
            #元データを呼び出す　なければ初期データフレームを作成
            try:
                preload=page.client_storage.get("radio_selected_data")
                load_radio_data=json.loads(preload)
                #新規データを追加していくと増えるだけだから、日付データにてフィルタして削除する
            except:
                load_radio_data = {}

            #radio_selected_dataのキーを日付に変更
            radio_selected_data = {date:radio_selected_data}
            #新規データを結合
            marge_radio_dict=load_radio_data|radio_selected_data
            page.client_storage.set("radio_selected_data", json.dumps(marge_radio_dict, ensure_ascii=False))


            # 辞書データをdfに変換
            df = pd.DataFrame.from_dict(data_dict, orient="index")
        
            # will_accept時のlocationデータはデフォルト入力データで入っているため、ラジオボタンでの選択内容に書き換える
            # df['task'] == "will_accept"の時、df['locate'] == "uncomplete"に変更する
            df.loc[df["task"] == "will_accept", "locate"] = "uncomplete"
            # uncompleteは前のlocateにて補完する
            df["locate"] = df["locate"].replace("uncomplete", method="ffill")
            # will_acceptは前のタスクにて補完する
            df["task"] = df["task"].replace("will_accept", method="ffill")
            # 選択したラジオボタンでのデータに書き込み直し

            # csvファイルの書き込み
            if (
                select_directory.result
                and select_directory.result.path
                and phName.value
                and list_am_location_data
                and list_pm_location_data
            ):
                try:
                    file_path = (
                        select_directory.result.path
                        + f"/{date}"
                        + f"{phName.value}"
                        + ".csv"
                    )
                except:
                    file_path = select_directory.result.path + f"/{date}.csv"

                # ファイル保存名に名前を使用しているので、名前が入力されていない場合にはエラーを表示する
                # 病棟データが何も入力されていないときも処理を中断する
                # 両者ともエラーメッセージをtrueに設定しなおす
                df.to_csv(file_path, index=False)
                # 保存できたら完了メッセージを表示
                save_message.content.controls[0].visible = True
                save_message.content.controls[1].visible = True
                page.update()
                # 時間経過後に消す 「csvファイルを保存しました」
                HideMessageHandler.hide_message(save_message, page)

            elif (
                not list_am_location_data or not list_pm_location_data
            ):  # 薬剤師名がないとき、病棟データが入力されていないとき
                # csvファイルは書き出さずにエラーメッセージのみ表示に再設定する
                require_location.visible = True
                page.update()
            else:  # 薬剤師名が入力されていない時
                require_name.visible = True
                page.update()

                """
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ["Time", "Task", "Count", "locate", "date", "PhName", "Comment"]
                    )
                    for time, record in data_dict.items():
                        writer.writerow(
                            [
                                record["time"],
                                record["task"],
                                record["count"],
                                record["locate"],
                                record["date"],
                                record["phName"],
                                record["comment"],
                            ]
                        )
                        
                    """
