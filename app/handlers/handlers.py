import json
import datetime
import flet as ft
import csv
import pandas as pd
from models.models import DataModel


class Handlers:
    @staticmethod
    def handle_change(e, today, Date):
        selected_date = e.control.value  # 例えば2021-01-01のような形式

        # 文字列を日付オブジェクトに変換
        today = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()

        # 年月日を取得して表示用のテキストに変換
        Date.text = f"{today.year}/{today.month}/{today.day}"
        Date.update()

    @staticmethod
    def dropdown_changed(e, phName, dialog, page):
        if phName.value == "Add":
            dialog.open = True
            page.update()
        else:
            page.update()

    @staticmethod
    def close_dialog(e, dialog, page):
        dialog.open = False
        page.update()

    @staticmethod
    def update_dropdown(phName, phNameList, page):
        if isinstance(phNameList, str):
            phNameList = json.loads(phNameList)
        options = []
        try:
            options = [ft.dropdown.Option(item["name"]) for item in phNameList]
        except:
            options = [ft.dropdown.Option("名前が登録されていません")]

        options.append(ft.dropdown.Option("Add"))

        phName.options = options
        page.update()

    # delete_name関数
    # setting pageに移動予定
    @staticmethod
    def drawer_open(e, page, endDrawer):
        page.open(endDrawer)

    @staticmethod
    def delete_name(e, phNameList, page):
        new_phNameList = phNameList.remove(e.control.data)
        page.set("phName", json.dumps(new_phNameList, ensure_ascli=False))
        page.update()

    # カラムの業務内容ごとの色分け
    # 384B70
    # 507687
    # 508D4E
    # 72BAA9
    @staticmethod
    def change_color(key):
        match key:
            case "情報収集＋指導":
                return "#384B70"
            case "指導記録作成":
                return "#384B70"
            case "混注時間":
                return "#384B70"
            case "薬剤セット数":
                return "#384B70"
            case "持参薬を確認":
                return "#384B70"
            case "薬剤服用歴等について保険薬局へ照会":
                return "#384B70"
            case "処方代理修正":
                return "#384B70"
            case "TDM実施":
                return "#384B70"
            case "カンファレンス":
                return "#384B70"
            case "医師からの相談":
                return "#384B70"
            case "看護師からの相談":
                return "#384B70"
            case "その他の職種からの相談":
                return "#384B70"
            case "委員会":
                return "#507687"
            case "勉強会参加":
                return "#507687"
            case "WG活動":
                return "#507687"
            case "1on1":
                return "#507687"
            case "ICT/AST":
                return "#507687"
            case "褥瘡":
                return "#507687"
            case "TPN評価":
                return "#507687"
            case "手術後使用薬剤確認":
                return "#508D4E"
            case "手術使用薬剤準備":
                return "#508D4E"
            case "周術期薬剤管理関連":
                return "#508D4E"
            case "麻酔科周術期外来":
                return "#508D4E"
            case "手術使用麻薬確認・補充":
                return "#508D4E"
            case "術後疼痛管理チーム回診":
                return "#508D4E"
            case "脳卒中ホットライン対応":
                return "#508D4E"
            case "13:15業務調整":
                return "#72BAA9"
            case "休憩":
                return "#72BAA9"
            case "その他":
                return "#72BAA9"
            case "管理業務":
                return "#72BAA9"

    @staticmethod
    def change_choice_button(e, selectColumns, page):
        # visible falseで重くなるようであればclearの使用を検討する
        # selectColumns[0].controls.clear()
        print(e.data)
        match int(e.data):
            case 0:  # 病棟担当
                selectColumns[0].visible = True  # 情報収集　指導
                selectColumns[1].visible = True  # 指導記録作成
                selectColumns[2].visible = True  # 混注時間
                selectColumns[3].visible = True  # 薬剤セット数
                selectColumns[4].visible = True  # 持参薬を確認
                selectColumns[5].visible = True  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = True  # 処方代理修正
                selectColumns[7].visible = True  # TDM実施
                selectColumns[8].visible = True  # カンファレンス
                selectColumns[9].visible = True  # 医師からの相談
                selectColumns[10].visible = True  # 看護師からの相談
                selectColumns[11].visible = True  # その他の職種からの相談

                # 非表示
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 褥瘡
                selectColumns[18].visible = False  # TPN評価
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 手術使用麻薬確認・補充
                selectColumns[24].visible = False  # 術後疼痛管理チーム回診
                selectColumns[25].visible = False  # 脳卒中ホットライン対応
                selectColumns[26].visible = False  # 13:15業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務

                page.update()
            case 1:  # 12階
                # 表示
                selectColumns[19].visible = True  # TPN評価
                selectColumns[20].visible = True  # 手術使用薬剤確認
                selectColumns[21].visible = True  # 手術使用薬剤準備
                selectColumns[22].visible = True  # 周術期薬剤管理関連
                selectColumns[23].visible = True  # 手術使用麻薬確認・補充
                selectColumns[24].visible = True  # 術後疼痛管理チーム回診
                selectColumns[25].visible = True  # 脳卒中ホットライン対応
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット数
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 褥瘡
                selectColumns[18].visible = False  # TPN評価

                selectColumns[26].visible = False  # 13:15業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務

                page.update()

            case 2:  # 役職者
                selectColumns[29].visible = True  # 管理業務
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット数
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 褥瘡
                selectColumns[18].visible = False  # TPN評価
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 手術使用麻薬確認・補充
                selectColumns[24].visible = False  # 術後疼痛管理チーム回診
                selectColumns[25].visible = False  # 脳卒中ホットライン対応
                selectColumns[26].visible = False  # 13:15業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他

                page.update()

            case 3:  # off
                # 表示
                selectColumns[12].visible = True  # 委員会
                selectColumns[13].visible = True  # 勉強会参加
                selectColumns[14].visible = True  # WG活動
                selectColumns[15].visible = True  # 1on1

                selectColumns[26].visible = True  # 13:15業務調整
                selectColumns[27].visible = True  # 休憩
                selectColumns[28].visible = True  # その他
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット数
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談

                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 褥瘡
                selectColumns[18].visible = False  # TPN評価
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 手術使用麻薬確認・補充
                selectColumns[24].visible = False  # 術後疼痛管理チーム回診
                selectColumns[25].visible = False  # 脳卒中ホットライン対応

                selectColumns[29].visible = False  # 管理業務

                page.update()
            case 4:  # ICT/AST
                # 表示
                selectColumns[16].visible = True  # ICT/AST
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット数
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = True  # 委員会
                selectColumns[13].visible = True  # 勉強会参加
                selectColumns[14].visible = True  # WG活動
                selectColumns[15].visible = True  # 1on1

                selectColumns[17].visible = False  # 褥瘡
                selectColumns[18].visible = False  # TPN評価
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 手術使用麻薬確認・補充
                selectColumns[24].visible = False  # 術後疼痛管理チーム回診
                selectColumns[25].visible = False  # 脳卒中ホットライン対応
                selectColumns[26].visible = False  # 13:15業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務

            case 5:  # NST
                # 表示
                selectColumns[17].visible = True  # 褥瘡
                selectColumns[18].visible = True  # TPN評価

                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット数
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST

                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 手術使用麻薬確認・補充
                selectColumns[24].visible = False  # 術後疼痛管理チーム回診
                selectColumns[25].visible = False  # 脳卒中ホットライン対応
                selectColumns[26].visible = False  # 13:15業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務

                page.update()

    @staticmethod
    def toggle_delete_button(page, delete_buttons):
        for button in delete_buttons:
            button.visible = not button.visible
        page.update()

    @staticmethod
    def delete_content(
        e,
        page,
        phNameList,
        phName,
        delete_buttons,
        drag_data,
        count_dict,
        comment_dict,
        columns,
        draggable_data_for_move,
        comments,
        times,
        comment,
    ):
        # _move関数でdelete_button.dataに入れたのはdragtargetで設定したカラムの番号
        # columns[i]でそのカラムの情報を取得し、見た目上削除
        # 正しくはcolumnsの初期化を行う。ドラッグする前の状態に戻す
        col_num = delete_buttons[e.control.data["num"]].data["num"]
        print(col_num)
        # 同じ情報の新しいカラムに差し替える
        columns[col_num].content.content = ft.Container(
            width=50,
            height=300,
            bgcolor=ft.colors.BLUE_50,
            border_radius=5,
        )
        # アップデートしてからmove関数をセットする
        # おそらくセットしている時のeを渡しているから変なことになる
        # deletebuttons属しているカラムのデータを渡していない
        # deletebuttons自体のデータが渡されている
        # contentのcoontent（見た目だけを更新する）
        # 中身のDraggtargetのonaccept,on_moveは残っていた

        # 同時に該当するdrag_dataのデータも削除する
        del drag_data[DataModel().times()[col_num]]
        # 該当のカウントデータも削除する
        if DataModel().times()[col_num] in count_dict:
            del comment_dict[DataModel.times()[col_num]]
        # 該当のその他のデータも削除する
        if DataModel().times()[col_num] in comment_dict:
            del comment_dict[DataModel().times()[col_num]]

        # カラムのgroupを元に戻す
        columns[col_num].content.group = "timeline"
        page.update()

    # カウンターの関数
    @staticmethod
    def counterPlus(e, count_field, count_dict, time):
        print(e)
        old_Count = int(count_field.value)
        new_Count = old_Count + 1
        # 更新した値にてカウンター内を更新
        count_field.value = new_Count
        count_field.update()
        # dict内の値を更新
        count_dict[time]["count"] = new_Count
        print(count_dict)

    @staticmethod
    def counterMinus(e, count_field, count_dict, time):
        # +と同様
        old_Count = int(count_field.value)
        new_Count = old_Count - 1
        # update counter value
        count_field.value = new_Count
        count_field.update()
        # dict内の値を更新
        print(e.control.data)
        count_dict[time]["count"] = new_Count

    @staticmethod
    def create_counter(e, count_dict):
        # eは入力したカラムの時間を取得
        # 初期は０
        count = 0
        time = e
        count_field = ft.TextField(
            count,
            width=40,
            text_align=ft.TextAlign.CENTER,
            text_size=10,
            border_color=None,
        )
        count_dict[e] = {"count": count}
        return ft.Column(
            [
                ft.IconButton(
                    ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size=25,
                    on_click=lambda e: Handlers.counterPlus(
                        e, count_field, count_dict, time
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                count_field,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: Handlers.counterMinus(
                        e, count_field, count_dict, time
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
            ]
        )

    @staticmethod
    def dlg_close(e, dlg, page):
        print("close")
        dlg.open = False
        page.update()

    @staticmethod
    def create_dialog_for_comment(e, comments, dlg, comment_dict, comment_field, page):
        print(e.control.data["time"])
        comment_time = comments[e.control.data["num"]].data["time"]
        comment_num = comments[e.control.data["num"]].data["num"]
        dlg.data = {"time": comment_time, "num": comment_num}
        # TextFiledの初期化
        if comment_time in comment_dict:
            comment_field.value = comment_dict[comment_time]["comment"]
        else:
            comment_field.value = ""
        page.open(dlg)

    @staticmethod
    def dlg_open(e, dlg):
        dlg.visible = True

    @staticmethod
    def add_name(e, phNameList, name_field, page, phName, dialog):
        new_name = name_field.value.strip()
        phName_List = (
            json.loads(phNameList) if isinstance(phNameList, str) else phNameList
        )
        if new_name:
            phName_List.append({"name": new_name})
            page.client_storage.set("phName", phName_List)
            name_field.value = ""
            Handlers.update_dropdown(phName, phName_List, page)
            dialog.open = False
            page.update()

    @staticmethod
    def add_comment_for_dict(e, dlg, comment_dict, comment_field, page):
        comment_time = dlg.data["time"]
        comment_num = dlg.data["num"]
        if comment_time in comment_dict:
            del comment_dict[comment_time]
            comment_dict[comment_time] = {"comment": comment_field.value}
        else:
            comment_dict[comment_time] = {"comment": comment_field.value}

        dlg.open = False
        page.update()

    @staticmethod
    def open_Drawer(e, customDrawer, page):
        print("open")
        customDrawer.visible = not customDrawer.visible
        page.update()

    @staticmethod
    def drag_move(
        e,
        page,
        draggable_data,
        delete_buttons,
        columns,
        comments,
        times,
        drag_data,
        comment,
        count_dict,
    ):
        print(e.control.group)
        src_id_str = e.src_id.replace("_", "")
        try:
            src_id_int = int(src_id_str)
            # 次カラム
            print("nowid", e.src_id)
            print(f"_{src_id_int + 4}")
            next_id = f"_{src_id_int + 4}"
        except:
            pass

        if page.get_control(e.src_id):
            src = page.get_control(e.src_id)
            try:
                key = src.data["task"]["task"]
            except:
                key = src.data["task"]

        elif e.src_id in draggable_data and "task":
            key = draggable_data[e.src_id]["task"]

        elif page.get_control(e.target):
            src = page.get_control(e.target)
            key = src.data["task"]["task"]

        e.control.content = ft.Column(
            controls=[
                delete_buttons[e.control.data["num"]],
                ft.Draggable(
                    group="timeline",
                    content=ft.Container(
                        content=ft.Text(key, color="white"),
                        width=50,
                        height=140,
                        bgcolor=Handlers.change_color(key),
                    ),
                    data={
                        "time": e.control.data["time"],
                        "num": e.control.data["num"],
                        "task": key,
                    },
                ),
            ],
            height=300,
            spacing=0,
            data={
                "time": e.control.data["time"],
                "num": e.control.data["num"],
                "task": key,
            },
        )

        # ドラッグ時にコンテンツを更新する用
        columns[e.control.data["num"]].content.data["task"] = key

        # delete_buttonsに渡すdata
        delete_buttons[e.control.data["num"]].data = {"num": e.control.data["num"]}
        e.control.update()
        left_column_num = e.control.data["num"] - 1
        # left_keyの初期化
        left_key = None
        try:
            left_key = columns[left_column_num].content.data["task"]
        except:
            pass

        # 現在のカラムの番号はnum = e.control.data["num"]
        # 左のカラム　num -1 のカラムの情報を取得
        # 一番左のカラムだけ表示、後は非表示にする（カウンターはそもそも作成しない）
        try:
            if left_key == key:
                e.control.content.controls[1].content.content.visible = False
                e.control.content.update()
            elif left_key != key:
                e.control.content.controls[1].content.content.visible = True
                e.control.content.update()
        except:
            pass

        match key:
            # key==その他の場合にはコメントボタンを追加する
            case "その他":
                # すでに左のカラムにコンテンツがある場合にはコメントボタンは作成しない
                e.control.content.controls.append(comments[e.control.data["num"]])
            # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
            case (
                "混注時間"
                | "休憩"
                | "委員会"
                | "WG活動"
                | "勉強会参加"
                | "1on1"
                | "カンファレンス"
            ):
                pass
            # その他の場合にはカウンターを表示する
            # 左カラムに同じデータはある場合にはカウンターは作成しない
            case _:
                if left_key == key:
                    pass
                else:
                    e.control.content.controls.append(
                        Handlers.create_counter(e.control.data["time"], count_dict)
                    )
        e.control.update()

        # moveにて新規src_idが追加された場合、その情報をdrag_dataに追加
        # elseに向けて辞書データを更新しておく
        draggable_data[e.src_id] = {"task": key}
        draggable_data[next_id] = {"task": key}

        # 左ではなくて、現在のカラム番号と左のカラム番号を比較する
        # 右のカラムも比較して、同じ業務内容の場合、右は非表示に
        # 左のみ残して表示する
        right_column_num = e.control.data["num"] + 1
        if right_column_num:
            right_key = columns[right_column_num].content.data["task"]
        try:
            if right_key == key:
                columns[right_column_num].content = ft.Column(
                    controls=[
                        delete_buttons[right_column_num],
                        ft.Draggable(
                            group="timeline",
                            content=ft.Container(
                                width=50,
                                height=140,
                                bgcolor=Handlers.change_color(key),
                            ),
                        ),
                    ],
                    height=300,
                    spacing=0,
                    data={
                        "time": times[right_column_num],
                        "num": right_column_num,
                        "task": key,
                    },
                )
                columns[right_column_num].update()
        except:
            pass
        # ドラッグデータの保存
        drag_data[e.control.data["time"]] = {"task": key}
        if comment:
            comments[e.control.data["num"]].data = {
                "time": e.control.data["time"],
                "num": e.control.data["num"],
            }

        # 右隣と左隣のカラムにmove関数を追加する
        columns[left_column_num].content.on_move = lambda e: Handlers.drag_move(
            e,
            page,
            draggable_data,
            delete_buttons,
            columns,
            comments,
            times,
            drag_data,
            comment,
            count_dict,
        )
        columns[left_column_num].update()
        columns[right_column_num].content.on_move = lambda e: Handlers.drag_move(
            e,
            page,
            draggable_data,
            delete_buttons,
            columns,
            comments,
            times,
            drag_data,
            comment,
            count_dict,
        )
        columns[right_column_num].update()

        # 受け取ったらdragtargetのgroupを変更して再ドラッグ不可にする
        e.control.group = "timeline_accepted"
        page.update()

    # acceptしたらカラムのデータを更新する
    # 隣のカラムにmove関数を追加する
    @staticmethod
    def drag_accepted(
        e,
        page,
        draggable_data,
        delete_buttons,
        columns,
        comments,
        times,
        drag_data,
        comment,
        count_dict,
    ):
        # print(e.target)
        src_id_str = e.src_id.replace("_", "")
        try:
            src_id_int = int(src_id_str)
            # 次カラム
            print("nowid", e.src_id)
            print(f"_{src_id_int + 4}")
            next_id = f"_{src_id_int + 4}"
        except:
            pass
        if page.get_control(e.src_id):
            src = page.get_control(e.src_id)
            try:
                if isinstance(src.data["task"], dict):
                    key = src.data["task"]["task"]
                else:
                    key = src.data["task"]
            except:
                key = src.data["task"]

        elif e.src_id in draggable_data and "task":
            key = draggable_data[e.src_id]["task"]

        elif page.get_control(e.target):
            src = page.get_control(e.target)
            try:
                if isinstance(src.data["task"], dict):
                    key = src.data["task"]["task"]
                else:
                    key = src.data["task"]
            except:
                key = src.data["task"]

        e.control.content = ft.Column(
            controls=[
                delete_buttons[e.control.data["num"]],
                ft.Draggable(
                    group="timeline",
                    content=ft.Container(
                        content=ft.Text(key, color="white"),
                        width=50,
                        height=140,
                        bgcolor=Handlers.change_color(key),
                    ),
                    data={
                        "time": e.control.data["time"],
                        "num": e.control.data["num"],
                        "task": key,
                    },
                ),
            ],
            height=300,
            spacing=0,
            data={
                "time": e.control.data["time"],
                "num": e.control.data["num"],
                "task": key,
            },
            # カラムがクリックされた時に隣のカラムにon_move関数をセットできるようにしたい
        )

        # ドラッグ時にコンテンツを更新する用
        columns[e.control.data["num"]].content.data["task"] = key
        print("columns", columns[e.control.data["num"]].content.data["task"])
        # moveにて新規src_idが追加された場合、その情報をdrag_dataに追加
        # elseに向けて辞書データを更新しておく
        draggable_data[e.src_id] = {"task": key}
        draggable_data[next_id] = {"task": key}

        left_column_num = e.control.data["num"] - 1
        # left_keyの初期化
        left_key = None

        try:
            left_key = columns[left_column_num].content.data["task"]
        except:
            pass

        # 現在のカラムの番号はnum = e.control.data["num"]
        # 左のカラム　num -1 のカラムの情報を取得
        # 一番左のカラムだけ表示、後は非表示にする（カウンターはそもそも作成しない）
        try:
            if left_key == key:
                e.control.content.controls[1].content.content.visible = False
                e.control.content.update()
            elif left_key != key:
                e.control.content.controls[1].content.content.visible = True
                e.control.content.update()

        except:
            pass

        match key:
            # key==その他の場合にはコメントボタンを追加する
            case "その他":
                # すでに左のカラムにコンテンツがある場合にはコメントボタンは作成しない
                e.control.content.controls.append(comments[e.control.data["num"]])
            # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
            case (
                "混注時間"
                | "休憩"
                | "委員会"
                | "WG活動"
                | "勉強会参加"
                | "1on1"
                | "カンファレンス"
            ):
                pass
            # その他の場合にはカウンターを表示する
            # 左カラムに同じデータはある場合にはカウンターは作成しない
            case _:
                if left_key == key:
                    pass
                else:
                    e.control.content.controls.append(
                        Handlers.create_counter(e.control.data["time"], count_dict)
                    )

        # move関数を追加する
        e.control.on_move = lambda e: Handlers.drag_move(
            e,
            page,
            draggable_data,
            delete_buttons,
            columns,
            comments,
            times,
            drag_data,
            comment,
            count_dict,
        )

        # 左隣カラムと右隣カラムにもmove関数をオフにする
        columns[left_column_num].content.on_move = None
        columns[left_column_num].update()

        right_column_num = e.control.data["num"] + 1
        columns[right_column_num].content.on_move = None
        columns[right_column_num].update()

        # ドラッグデータの保存
        drag_data[e.control.data["time"]] = {"task": key}
        if comment:
            comments[e.control.data["num"]].data = {
                "time": e.control.data["time"],
                "num": e.control.data["num"],
            }

        # 受け取ったらdragtargetのgroupを変更して再ドラッグ不可にする
        e.control.group = "timeline_accepted"
        page.update()

    @staticmethod
    def write_csv_file(
        e,
        times,
        amTime,
        today,
        columns,
        drag_data,
        count_dict,
        amDropDown,
        pmDropDown,
        custumDrawerAm,
        custumDrawerPm,
        phName,
        page,
        comment_dict,
        select_directory,
    ):
        # 最後にデータベースに保管する

        # 入力された辞書データの長さ
        # print(len(drag_data.keys()))
        # first_key = list(drag_data.keys())[0]
        # first_value = drag_data[first_key]
        # print(first_key)

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
                "date": str(today),
                "PhName": "",
                "comment": "",
            }
            for i in range(len(columns))
        ]
        # リストを辞書形式に変換
        data_dict = {record["time"]: record for record in set_data}
        # 辞書データの更新
        # taskデータの書き込み
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
                list_am_location_data.append(custumDrawerAm.content.controls[i].label)

        for time in data_dict.keys():
            if list_am_location_data is not None:
                if data_dict[time]["locate"] == "AM":
                    data_dict[time]["locate"] = list_am_location_data
            else:
                None

            # PMの場合
        list_pm_location_data = []
        for i in range(len(custumDrawerPm.content.controls)):
            if custumDrawerPm.content.controls[i].value == True:
                list_pm_location_data.append(custumDrawerPm.content.controls[i].label)

        for time in data_dict.keys():
            if list_pm_location_data is not None:
                if data_dict[time]["locate"] == "PM":
                    data_dict[time]["locate"] = list_pm_location_data
            else:
                None

        list_pm_location_data = []
        for time in data_dict.keys():
            if list_pm_location_data is not None:
                if data_dict[time]["locate"] == "PM":
                    data_dict[time]["locate"] = list_pm_location_data
            else:
                None

        # phName データの書き込み
        for time in data_dict.keys():
            if phName.value != None:
                data_dict[time]["phName"] = phName.value
            else:
                data_dict[time]["phName"] = ""
        page.client_storage.set(
            "timeline_data", json.dumps(data_dict, ensure_ascii=False)
        )
        # その他コメントの書き込み
        for time, comment_data in comment_dict.items():
            if time in data_dict:
                data_dict[time]["comment"] = comment_data["comment"]

        # csvファイルの書き込み
        if select_directory.result and select_directory.result.path:
            file_path = select_directory.result.path + f"/{today}.csv"
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
