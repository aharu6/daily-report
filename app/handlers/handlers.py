import json
import datetime
import flet as ft
import csv
import pandas as pd
from models.models import DataModel
from handlers.drag_move import DragMoveHandler
from handlers.drag_move_add import DragMoveAddHandler
from handlers.handdrag_will_accept import Add_will_accept

class Handlers:
    @staticmethod
    def handle_change(e, today, Date,page):
        """_summary_
        選択した日付にてカレンダーを更新する
        デフォルトは今日の日付
        カレンダーは過去の日付も選択できるように
        Args:
            e (_type_): 日付選択
            today (_type_): _description_
            Date (_type_): _description_
            page (_type_): _description_
        """
        selected_date = e.control.value  # 例えば2021-01-01のような形式
        # 年月日を取得して表示用のテキストに変換
        Date.text = f"{selected_date.year}/{selected_date.month}/{selected_date.day}"
        Date.data = selected_date
        page.update() 

    @staticmethod
    def dropdown_changed(e, phName, dialog, page,require_error_message):
        """_summary_

        Args:
            e (_type_): _description_
            phName (_type_): _description_
            dialog (_type_): _description_
            page (_type_): _description_
        """
        if phName.value == "Add":
            dialog.open = True
            page.update()
        else:
            require_error_message.content = None
            page.update()

    @staticmethod
    def close_dialog(e, dialog, page):
        dialog.open = False
        page.update()

    @staticmethod
    def update_dropdown(phName, phNameList, page):
        """_summary_

        Args:
            phName (_type_): _description_
            phNameList (_type_): _description_
            page (_type_): _description_
        """
        if isinstance(phNameList, str):
            phNameList = json.loads(phNameList)
        options = []
        try:
            options = [ft.dropdown.Option(item["name"],data = item["name"]) for item in phNameList]
        except:
            options = [ft.dropdown.Option("名前が登録されていません",data = "noName")]

        options.append(ft.dropdown.Option("Add"))

        phName.options = options
        page.update()

    # delete_name関数
    # setting pageに移動予定
    @staticmethod
    def drawer_open(e, page, endDrawer):
        """_summary_

        Args:
            e (_type_): _description_
            page (_type_): _description_
            endDrawer (_type_): _description_
        """
        page.open(endDrawer)

    @staticmethod
    def delete_name(e, phNameList, page):
        """_summary_

        Args:
            e (_type_): _description_
            phNameList (_type_): _description_
            page (_type_): _description_
        """
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
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1

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
    def toggle_delete_button(page, columns):
        for  i in range(len(columns)):
            if columns[i].content.data["task"] != "":
                print(columns[i].content.content)
                columns[i].content.content.controls[0].visible = not columns[i].content.content.controls[0].visible
            
            #button.visible = not button.visible
        page.update()

    @staticmethod
    def delete_content(
        e,
        page,
        phNameList,
        phName,
        drag_data,
        count_dict,
        comment_dict,
        columns,
        draggable_data_for_move,
        comments,
        times,
        comment,
        draggable_data
    ):
        # _move関数でdelete_button.dataに入れたのはdragtargetで設定したカラムの番号
        # columns[i]でそのカラムの情報を取得し、見た目上削除
        # 正しくはcolumnsの初期化を行う。ドラッグする前の状態に戻す
        col_num = e.control.data["num"]
        # 同じ情報の新しいカラムに差し替える
        #columns[col_num].content.content.clean()
        #columns[col_num].content.content.update()
        
        columns[col_num].content.content = ft.Column(
            controls=[
                ft.Container(
                    width=50,
                    height=300,
                    bgcolor="#CBDCEB",
                    border_radius=5,
                ),
            ]
        )
        
        right_col_num = e.control.data["num"]+1
        try:
            right_key = columns[right_col_num].content.data["task"]
        except:
            pass
    
        page.add(columns[col_num].content.content)

        #右方向に広がるcontent.data["task"] == "will_accept"のコンテンツは全て削除
        #while文を使用する
        while right_key =="will_accept":
            columns[right_col_num].content.content = ft.Column(
                controls=[
                    ft.Container(
                        width = 50,
                        height = 300,
                        bgcolor = "#CBDCEB",
                        border_radius = 5,
                    ),
                ]
            )
            del drag_data[DataModel().times()[right_col_num]]
            if DataModel().times()[right_col_num] in count_dict:
                del count_dict[DataModel.times()[right_col_num]]
            if DataModel().times()[right_col_num] in comment_dict:
                del comment_dict[DataModel.times()[right_col_num]]
                
            columns[right_col_num].content.group = "timeline"
            columns[right_col_num].group = "timeline"
            
            columns[right_col_num].content.on_will_accept = lambda e: Add_will_accept.drag_will_accept(e, page,columns,drag_data)
            columns[right_col_num].on_will_accept = lambda e: Add_will_accept.drag_will_accept(e, page,columns,drag_data)
            
            right_col_num += 1
            right_key = columns[right_col_num].content.data["task"]
        else:
            pass
        page.update()
    
        # deletebuttons自体のデータが渡されている
        # contentのcoontent（見た目だけを更新する）

        # 同時に該当するdrag_dataのデータも削除する
        del drag_data[DataModel().times()[col_num]]
        # 該当のカウントデータも削除する
        if DataModel().times()[col_num] in count_dict:
            del count_dict[DataModel().times()[col_num]]
        # 該当のその他のデータも削除する
        if DataModel().times()[col_num] in comment_dict:
            del comment_dict[DataModel().times()[col_num]]

        # カラムのgroupを元に戻す
        columns[col_num].group = "timeline"
        columns[col_num].content.group = "timeline"
        # カラムのデータを初期化
        columns[col_num].content.data["task"] = ""
        
        # on_will_acceptを元に戻す
        columns[col_num].content.on_will_accept = lambda e: Add_will_accept.drag_will_accept(e, page,columns=columns,drag_data=drag_data)
        columns[col_num].on_will_accept = lambda e: Add_will_accept.drag_will_accept(e, page,columns=columns,drag_data=drag_data)
        
        
        #accept関数を元に戻す
        columns[col_num].content.on_accept = lambda e: Handlers.drag_accepted(
            e, 
            page=page, 
            draggable_data=draggable_data,
            columns=columns, 
            comments=comments,
            times=times,
            drag_data = drag_data, 
            comment = comment,
            count_dict = count_dict,
            comment_dict= comment_dict, 
            phNameList=phNameList,
            phName=phName,
            draggable_data_for_move=draggable_data_for_move
            )
        
        columns[col_num].on_accept = lambda e: Handlers.drag_accepted(
            e, 
            page=page, 
            draggable_data=draggable_data,
            columns=columns, 
            comments=comments,
            times=times,
            drag_data = drag_data, 
            comment = comment,
            count_dict = count_dict,
            comment_dict= comment_dict, 
            phNameList=phNameList,
            phName=phName,
            draggable_data_for_move=draggable_data_for_move
            )
        
        #カラムのデータは初期化したから何もないはず　空になる
        key = columns[col_num].content.data["task"]
        try:
            if right_key != key:
                #削除するとカラムのデータはなくなるので、右カラムと削除カラムにてdataが異なる
                #カラムの文字を再表示
                columns[right_col_num].content.content.controls[1].content.content.visible = True
        except:
            pass
        
        #カウンターを再表示、再追加
        #keyによってカウンターの追加、非追加が異なる
        #カウンター必要なkey
        
        #現在カラムのkeyは削除ずみ
        #右カラムのrightcolumn[key]を取得
        match right_key:
            case "その他":
                #
                pass
            case (
                "混注時間"
                | "休憩"
                | "委員会"
                | "WG活動"
                | "勉強会参加"
                | "1on1"
                | "カンファレンス"
                |"13:15業務調整"
            ):
                #カウンター表示不要
                pass
            case _:
                pass
        
        page.update()

    # カウンターの関数
    @staticmethod
    def counterPlus(e, count_field, count_dict, time):
        old_Count = int(count_field.value)
        new_Count = old_Count + 1
        # 更新した値にてカウンター内を更新
        count_field.value = new_Count
        count_field.update()
        # dict内の値を更新
        count_dict[time]["count"] = new_Count

    @staticmethod
    def counterMinus(e, count_field, count_dict, time):
        # +と同様
        old_Count = int(count_field.value)
        new_Count = old_Count - 1
        # update counter value
        count_field.value = new_Count
        count_field.update()
        # dict内の値を更新
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
        dlg.open = False
        page.update()

    @staticmethod
    def create_dialog_for_comment(e, comments, dlg, comment_dict, comment_field, page):
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
    def open_Drawer(e,customDrawerTile, customDrawer, page):
        customDrawerTile.visible = not customDrawerTile.visible
        customDrawer.visible = not customDrawer.visible
        page.update()

    # acceptしたらカラムのデータを更新する
    # 隣のカラムにmove関数を追加する
    @staticmethod
    def drag_accepted(
        e,
        page,
        draggable_data,
        columns,
        comments,
        times,
        drag_data,
        comment,
        count_dict,
        phNameList,
        phName,
        comment_dict,
        draggable_data_for_move,
    ):
        # print(e.target)
        src_id_str = e.src_id.replace("_", "")
        try:
            src_id_int = int(src_id_str)
            # 次カラム
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
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    visible=False,
                    icon_size=20,
                    icon_color="red",
                    on_click=lambda e: Handlers.delete_content(
                        e,
                        page,
                        phNameList,
                        phName,
                        drag_data,
                        count_dict,
                        comment_dict,
                        columns,
                        draggable_data_for_move,
                        comments,
                        DataModel().times(),  # delete_contentでの引数ではtimes
                        comment,
                        draggable_data,
                    ),
                    data = {"num":e.control.data["num"]}
                ),
                ft.Draggable(
                    group="timeline_accepted",
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
            # カラムがクリックされた時
        )
        #受け取ったらon_accept自体は働かないようにする
        #deletecontentのときには元に戻す
        #e.control.on_accept = None
        e.control.on_will_accept = None
        e.control.on_accept = None
        page.update()
        
        
        """
        for i in range(len(columns)):
            if columns[i].content.data["task"] == 'will_accept':
                columns[i].content.content = ft.Text(key, color="white")
                columns[i].content.width  =50
                columns[i].content.height  =140
                columns[i].content.bgcolor = Handlers.change_color(key)
                columns[i].content.data["task"] = key
                
                
                #will_accept = noneにする
                columns[i].content.on_will_accept = None
                #ドラッグデータの保存
                drag_data[columns[i].content.data["time"]] = {"task":key}
                if comment:
                    comments[columns[i].content.data["num"]].data = {
                        "time":columns[i].content.data["time"],
                        "num":columns[i].content.data["num"]
                    }
                    
            else:pass

        #columns全てで実施する
        #columns data≒"will_accept"があったcolumnsのみcontentsを更新する
        """
        
        # ドラッグ時にコンテンツを更新する用
        columns[e.control.data["num"]].content.data["task"] = key
        """
        # moveにて新規src_idが追加された場合、その情報をdrag_dataに追加
        # elseに向けて辞書データを更新しておく
        draggable_data[e.src_id] = {"task": key}
        draggable_data[next_id] = {"task": key}
        """
        
        left_column_num = e.control.data["num"] - 1
        # left_keyの初期化
        left_key = None

        try:
            left_key = columns[left_column_num].content.data["task"]
        except:
            pass
        
        #隣のからむにwill

        # 現在のカラムの番号はnum = e.control.data["num"]
        # 左のカラム　num -1 のカラムの情報を取得
        # 一番左のカラムだけ表示、後は非表示にする（カウンターはそもそも作成しない）
        """
        try:
            if left_key == key:
                e.control.content.controls[1].content.content.visible = True
                e.control.content.update()
            elif left_key != key:
                e.control.content.controls[1].content.content.visible = True
                e.control.content.update()

        except:
            pass
        """
        
        #Dataが渡されたcolumnsにのみcontentsを更新する
        
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
            
            case _:
                pass
            
            
            # その他の場合にはカウンターを表示する
            # 左カラムに同じデータはある場合にはカウンターは作成しない
            #case _:
            #   if left_key == key:
            #       pass
            #   else:
            #      e.control.content.controls.append(
            #          Handlers.create_counter(e.control.data["time"], count_dict)
            #      )
        
        # move関数を追加しない
        #再クリックしたときのみmove関数を追加する

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
        select_day,
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
        save_error_message,
    ):
        date = f"{select_day.data.year}-{select_day.data.month}-{select_day.data.day}"
        #名前が入力されていない場合にはエラーを表示する
        if phName.value == None:
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
            # willacceptのみの記載の場合、前後のtaskを埋める挙動を書かないといけない
            
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
                try:
                    data_dict[time]["phName"] = phName.value
                except:
                    data_dict[time]["phName"] = ""
                    
                    
            #前のデータに追加していく形式へ
            #追加前のデータ
            
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
                
            #変更後のデータを保管する
            page.client_storage.set(
                "timeline_data", json.dumps(save_data, ensure_ascii=False)
                )
                        
            # その他コメントの書き込み
            for time, comment_data in comment_dict.items():
                if time in data_dict:
                    data_dict[time]["comment"] = comment_data["comment"]

            # csvファイルの書き込み
            if select_directory.result and select_directory.result.path:
                try:
                    file_path = select_directory.result.path + f"/{date}"+f"{phName.value}"+".csv"
                except:
                    file_path = select_directory.result.path + f"/{date}.csv"
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
