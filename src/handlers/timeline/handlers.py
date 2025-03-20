import json
from handlers.timeline.hide_message import HideMessageHandler
import flet as ft
from flet import BoxShape
import pandas as pd
from models.models import DataModel
from handlers.timeline.handdrag_will_accept import Add_will_accept
from handlers.timeline.make_popup import MakePopup


class Handlers:
    @staticmethod
    def handle_change(e, Date, page):
        """_summary_
        選択した日付にてカレンダーを更新する
        デフォルトは今日の日付
        カレンダーは過去の日付も選択できるように
        Args:
            e (_type_): 日付選択
            Date (_type_): _description_
            page (_type_): _description_
        """
        selected_date = e.control.value  # 例えば2021-01-01のような形式
        # 年月日を取得して表示用のテキストに変換
        Date.text = f"{selected_date.year}/{selected_date.month}/{selected_date.day}"
        Date.data = selected_date
        page.update()

    @staticmethod
    def dropdown_changed(e, phName, dialog, page, require_error_message):
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
            options = [
                ft.dropdown.Option(item["name"], data=item["name"])
                for item in phNameList
            ]
        except:
            options = [ft.dropdown.Option("名前が登録されていません", data="noName")]

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
            case "薬剤使用状況の把握等（情報収集）":
                return "#384B70"
            case "服薬指導＋指導記録作成":
                return "#384B70"
            case "混注時間":
                return "#384B70"
            case "薬剤セット・確認":
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
            case "業務調整":
                return "#72BAA9"
            case "休憩":
                return "#72BAA9"
            case "その他":
                return "#72BAA9"
            case "管理業務":
                return "#72BAA9"
            case "NST":
                return "#507687"
            case "問い合わせ応需":
                return "#DDA853"
            case "マスター作成・変更":
                return "#DDA853"
            case "薬剤情報評価":
                return "#DDA853"
            case "後発品選定":
                return "#DDA853"
            case "会議資料作成":
                return "#DDA853"
            case "配信資料作成":
                return "#DDA853"
            case "フォーミュラリー作成":
                return "#DDA853"
            case "外来処方箋修正":
                return "#DDA853"
            case "勉強会資料作成・開催":
                return "#DDA853"
            case "お役立ち情報作成":
                return "#DDA853"

    @staticmethod
    def change_choice_button(e, selectColumns, page):
        # visible falseで重くなるようであればclearの使用を検討する
        # selectColumns[0].controls.clear()
        match int(e.data):
            case 0:  # 病棟担当
                selectColumns[0].visible = True  # 情報収集　指導
                selectColumns[1].visible = True  # 指導記録作成
                selectColumns[2].visible = True  # 混注時間
                selectColumns[3].visible = True  # 薬剤セット・確認
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
                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務
                selectColumns[30].visible = False  # NST
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成

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
                selectColumns[3].visible = False  # 薬剤セット・確認
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

                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務
                selectColumns[30].visible = False  # NST
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成

                page.update()

            case 2:  # 役職者
                selectColumns[29].visible = True  # 管理業務
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
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
                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他

                selectColumns[30].visible = False  # NST
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成

                page.update()

            case 3:  # その他

                # 表示
                selectColumns[12].visible = True  # 委員会
                selectColumns[13].visible = True  # 勉強会参加
                selectColumns[14].visible = True  # WG活動
                selectColumns[15].visible = True  # 1on1

                selectColumns[26].visible = True  # 業務調整
                selectColumns[27].visible = True  # 休憩
                selectColumns[28].visible = True  # その他
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
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
                selectColumns[30].visible = False  # NST
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成

                page.update()
            case 4:  # ICT/AST
                # 表示
                selectColumns[16].visible = True  # ICT/AST
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
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
                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務
                selectColumns[30].visible = False  # NST
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成

                page.update()

            case 5:  # NST
                # 表示
                selectColumns[17].visible = True  # 褥瘡
                selectColumns[18].visible = True  # TPN評価
                selectColumns[30].visible = True  # NST

                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
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
                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成

                page.update()

            case 6:  # DI
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
                # 表示
                selectColumns[4].visible = True  # 持参薬を確認
                # 非表示
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # 　WG活動
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
                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務
                selectColumns[30].visible = False  # NST

                # 表示
                selectColumns[31].visible = True  # 問い合わせ応需
                selectColumns[32].visible = True  # マスター作成・変更
                selectColumns[33].visible = True  # 薬剤情報評価
                selectColumns[34].visible = True  # 後発品選定
                selectColumns[35].visible = True  # 会議資料作成
                selectColumns[36].visible = True  # 配信資料作成
                selectColumns[37].visible = True  # フォーミュラリー作成
                selectColumns[38].visible = True  # 外来処方箋修正
                selectColumns[39].visible = True  # 勉強会資料作成・開催
                selectColumns[40].visible = True  # お役立ち情報作成

                page.update()

    @staticmethod
    def toggle_delete_button(e, page, columns):
        e.control.selected = not e.control.selected
        # 全てのselect columnsを選択不可能にする
        for i in range(len(columns)):
            # columns[i].disabled = not columns[i].disabled
            # disabled効かない
            # 特定のグループ名にして、falseの中で分ける？
            # seeletcolumnの方ではなくて、columnsの方
            if columns[i].content.group == "timeline":
                columns[i].content.group = "delete_toggle"
            elif columns[i].content.group == "delete_toggle":
                columns[i].content.group = "timeline"

        for i in range(len(columns)):
            if columns[i].content.data is not None:
                task = columns[i].content.data["task"]
                match task:
                    case "will_accept":
                        pass
                    case "":
                        pass
                    case _:
                        try:
                            # 初回ドラッグコンテンツ用のdeletebutton visible
                            # 全てのカラムで押すたびにtrueとfalseを揃える
                            # ゴミ箱アイコンがonのときにはドラッグできないように編集する
                            columns[i].content.content.controls[0].visible = (
                                not columns[i].content.content.controls[0].visible
                            )
                        except:
                            # reload時のdeletebutton visible
                            pass

                # button.visible = not button.visible
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
        draggable_data,
        update_location_data,
        customDrawerAm,
        customDrawerPm,
        radio_selected_data,
        date,
    ):
        from handlers.timeline.drag_leave import DragLeave

        # _move関数でdelete_button.dataに入れたのはdragtargetで設定したカラムの番号
        # columns[i]でそのカラムの情報を取得し、見た目上削除
        # 正しくはcolumnsの初期化を行う。ドラッグする前の状態に戻す
        col_num = e.control.data["num"]
        # 同じ情報の新しいカラムに差し替える
        # columns[col_num].content.content.clean()
        # 削除した時点ではまだdeletebuttonがonになっている状態だから、draggableのgroup delete_toggleになるはず
        columns[col_num].content = ft.DragTarget(
            group="delete_toggle",
            content=ft.Container(
                width=50,
                height=370,
                bgcolor="#CBDCEB",
                border_radius=5,
            ),
            on_will_accept=lambda e: Add_will_accept.drag_will_accept(
                e, page, columns, drag_data
            ),
            on_accept=lambda e: Handlers.drag_accepted(
                e=e,
                page=page,
                draggable_data_for_move=draggable_data_for_move,
                columns=columns,
                comments=comments,
                times=times,
                drag_data=drag_data,
                comment=comment,
                count_dict=count_dict,
                phNameList=phNameList,
                phName=phName,
                comment_dict=comment_dict,
                draggable_data=draggable_data,
                update_location_data=update_location_data,
                customDrawerAm=customDrawerAm,
                customDrawerPm=customDrawerPm,
                radio_selected_data=radio_selected_data,
                date=date,
            ),
            on_leave=lambda e: DragLeave.drag_leave(e, page),
            data={"time": times[col_num], "num": col_num, "task": ""},
        )

        right_col_num = e.control.data["num"] + 1
        try:
            right_key = columns[right_col_num].content.data["task"]
        except:
            right_key = None

        page.add(columns[col_num].content.content)

        model = DataModel()

        # 右方向に広がるcontent.data["task"] == "will_accept"のコンテンツは全て削除
        # while文を使用する
        while right_key == "will_accept":
            columns[right_col_num].content = ft.DragTarget(
                group="delete_toggle",
                content=ft.Container(
                    width=50,
                    height=370,
                    bgcolor="#CBDCEB",
                    border_radius=5,
                ),
                data={"time": times[right_col_num], "num": right_col_num, "task": ""},
                on_accept=lambda e: Handlers.drag_accepted(
                    e=e,
                    page=page,
                    draggable_data_for_move=draggable_data_for_move,
                    columns=columns,
                    comments=comments,
                    times=times,
                    drag_data=drag_data,
                    comment=comment,
                    count_dict=count_dict,
                    phNameList=phNameList,
                    phName=phName,
                    comment_dict=comment_dict,
                    draggable_data=draggable_data,
                    update_location_data=update_location_data,
                    customDrawerAm=customDrawerAm,
                    customDrawerPm=customDrawerPm,
                    radio_selected_data=radio_selected_data,
                    date=date,
                ),
                on_leave=lambda e: DragLeave.drag_leave(e, page),
                on_will_accept=lambda e: Add_will_accept.drag_will_accept(
                    e, page, columns, drag_data
                ),
            )
            del drag_data[model.times()[right_col_num]]
            if model.times()[right_col_num] in count_dict:
                del count_dict[model.times()[right_col_num]]
            if model.times()[right_col_num] in comment_dict:
                del comment_dict[model.times()[right_col_num]]

            right_col_num += 1
            right_key = columns[right_col_num].content.data["task"]
        else:
            pass
        page.update()

        # deletebuttons自体のデータが渡されている
        # contentのcoontent（見た目だけを更新する）

        # 同時に該当するdrag_dataのデータも削除する
        del drag_data[model.times()[col_num]]
        # 該当のカウントデータも削除する
        if model.times()[col_num] in count_dict:
            del count_dict[model.times()[col_num]]
        # 該当のその他のデータも削除する
        if model.times()[col_num] in comment_dict:
            del comment_dict[model.times()[col_num]]

        # カラムのgroupを元に戻す

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
        delspace1=new_name.replace("　","")
        delspace2=delspace1.replace(" ","")
        try:
            phName_List = (
                json.loads(phNameList) if isinstance(phNameList, str) else phNameList
                )
        except:
            phName_List = []

        if delspace2:
            phName_List.append({"name": delspace2})
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
    def open_Drawer(e, customDrawerTile, customDrawer, page):
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
        customDrawerAm,
        customDrawerPm,
        update_location_data,
        radio_selected_data,
        date,
    ):
        model = DataModel()

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
                        e=e,
                        page=page,
                        phNameList=phNameList,
                        phName=phName,
                        drag_data=drag_data,
                        count_dict=count_dict,
                        comment_dict=comment_dict,
                        columns=columns,
                        draggable_data_for_move=draggable_data_for_move,
                        comments=comments,
                        times=model.times(),  # delete_contentでの引数ではtimes
                        comment=comment,
                        draggable_data=draggable_data,
                        update_location_data=update_location_data,
                        customDrawerAm=customDrawerAm,
                        customDrawerPm=customDrawerPm,
                        radio_selected_data=radio_selected_data,
                        date=date,
                    ),
                    data={"num": e.control.data["num"]},
                ),
                ft.Draggable(
                    group="timeline_accepted",
                    content=ft.Container(
                        content=ft.Text(
                            key, color="white", text_align=ft.TextAlign.CENTER
                        ),
                        width=50,
                        height=130,
                        bgcolor=Handlers.change_color(key),
                        border_radius=ft.border_radius.only(top_left=5, bottom_left=5),
                        shape=BoxShape.RECTANGLE,
                    ),
                    data={
                        "time": e.control.data["time"],
                        "num": e.control.data["num"],
                        "task": key,
                    },
                ),
                ft.PopupMenuButton(
                    items=[
                        MakePopup.add_popup(
                            time=e.control.data["time"],
                            update_location_data=update_location_data,
                            num=e.control.data["num"],
                            columns=columns,
                            page=page,
                            radio_selected_data=radio_selected_data,
                            date=date,
                        ),
                    ],
                    tooltip="編集",
                    icon=ft.icons.MORE_VERT,
                    icon_size=20,
                    on_open=lambda e: MakePopup.pop_up_reload(
                        e=e,
                        customDrawerAm=customDrawerAm,
                        customDrawerPm=customDrawerPm,
                        page=page,
                    ),
                    data={
                        "time": e.control.data["time"],
                    },
                ),
                ft.Container(),
            ],
            height=370,
            spacing=0,
            data={
                "time": e.control.data["time"],
                "num": e.control.data["num"],
                "task": key,
            },
            # カラムがクリックされた時
        )
        # 受け取ったらon_accept自体は働かないようにする
        # deletecontentのときには元に戻す
        # e.control.on_accept = None
        e.control.on_will_accept = None
        e.control.on_accept = None

        # ドラッグ時にコンテンツを更新する用
        columns[e.control.data["num"]].content.data["task"] = key
        """
        # moveにて新規src_idが追加された場合、その情報をdrag_dataに追加
        # elseに向けて辞書データを更新しておく
        draggable_data[e.src_id] = {"task": key}
        draggable_data[next_id] = {"task": key}
        """
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

        # Dataが渡されたcolumnsにのみcontentsを更新する

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
                | "業務調整"
            ):
                pass

            case _:
                e.control.content.controls.append(
                    Handlers.create_counter(e.control.data["time"], count_dict)
                )

            # その他の場合にはカウンターを表示する
            # 左カラムに同じデータはある場合にはカウンターは作成しない
            # case _:
            #   if left_key == key:
            #       pass
            #   else:
            #      e.control.content.controls.append(
            #          Handlers.create_counter(e.control.data["time"], count_dict)
            #      )

        # move関数を追加しない
        # 再クリックしたときのみmove関数を追加する

        # ドラッグデータの保存
        drag_data[e.control.data["time"]] = {"task": key}
        if e.control.data["task"] == "その他":
            comments[e.control.data["num"]].data = {
                "time": e.control.data["time"],
                "num": e.control.data["num"],
            }
        # 受け取ったらdragtargetのgroupを変更して再ドラッグ不可にする
        e.control.group = "timeline_accepted"
        page.update()

    from handlers.timeline.hide_message import HideMessageHandler

    