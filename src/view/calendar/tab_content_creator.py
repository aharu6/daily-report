import flet as ft
import datetime
from .create_calendar import CreateCalendar
from .update_card import UpdateCard
from .update_calendar import UpdateCalendar

class TabContentCreator:
    @staticmethod
    def create_tab_content(label, page, schedule_data, switch_value):
        """タブのコンテンツを作成"""
        # 各タブ用のカレンダーを作成
        tab_calendar = CreateCalendar.create_calendar(
            datetime.datetime.now().year, 
            datetime.datetime.now().month
        )

        # 年月表示用のテキスト
        tab_header = ft.Text(
            f"{datetime.datetime.now().year}年{datetime.datetime.now().month}月", 
            size=30, 
            weight=ft.FontWeight.BOLD
        )

        # チェックボックス用の変数を初期化
        checkboxes = None

        # 個人名絞り込みの場合
        if label == "個人名絞り込み":
            if not schedule_data:
                try:
                    schedule_data = page.client_storage.get("schedule_data")
                    if schedule_data is None:
                        schedule_data = []
                except Exception as e:
                    schedule_data = []

            # ユニークな名前データを抽出してチェックボックスを作成
            unique_names = set(item["phName"] for item in schedule_data if "phName" in item)
            checkboxes = ft.ResponsiveRow(
                controls=[
                    ft.Checkbox(
                        label=name,
                        value=False,
                        data=name,
                    )
                    for name in unique_names
                ]
            )
            tab_calendar.controls.append(
                ft.Text("絞り込みを行う名前を選択、選択後は再度更新ボタンを押す"),
            )
            tab_calendar.controls.append(checkboxes)

        # カレンダー更新関数
        def update_calendar_and_text(e, is_forward=True):
            current_year = tab_calendar.year
            current_month = tab_calendar.month
            
            if is_forward:
                if current_month == 12:
                    next_year = current_year + 1
                    next_month = 1
                else:
                    next_year = current_year
                    next_month = current_month + 1
            else:
                if current_month == 1:
                    next_year = current_year - 1
                    next_month = 12
                else:
                    next_year = current_year
                    next_month = current_month - 1
            
            # 新しいカレンダーを作成
            new_calendar = CreateCalendar.create_calendar(next_year, next_month)
            
            # カレンダーを更新
            tab_calendar.controls.clear()
            tab_calendar.controls.extend(new_calendar.controls)
            tab_calendar.year = next_year
            tab_calendar.month = next_month
            
            # ヘッダーを更新
            tab_header.value = f"{next_year}年{next_month}月"
            
            # カードを追加（病棟絞り込みの場合のみ）
            if label != "個人名絞り込み":
                new_cards = UpdateCard.create_card_for_month(next_year, next_month, label)
                for index, card in enumerate(new_cards):
                    tab_calendar.controls.append(card)
            
            tab_calendar.update()
            tab_header.update()

        # ナビゲーションボタン
        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_size=30,
            on_click=lambda e: update_calendar_and_text(e, is_forward=False),
            tooltip="前の月",
        )
        next_button = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            icon_size=30,
            on_click=lambda e: update_calendar_and_text(e, is_forward=True),
            tooltip="次の月",
        )

        # 矢印ナビゲーション
        arrow_navigation = ft.Row(
            [back_button, tab_header, next_button],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # 更新ボタン
        def update_card_calendar(e):
            """カードとカレンダーの更新"""
            if label == "個人名絞り込み":
                # 個人名絞り込みの場合の処理
                selected_names = []
                for control in tab_calendar.controls:
                    if isinstance(control, ft.ResponsiveRow):
                        for checkbox in control.controls:
                            if isinstance(checkbox, ft.Checkbox) and checkbox.value:
                                selected_names.append(checkbox.data)
                
                # 選択された名前でフィルタリング
                filtered_data = [
                    item for item in schedule_data 
                    if item.get("phName") in selected_names
                ]
                
                # カレンダーの色を更新
                UpdateCalendar.update_calendar_with_schedule_data(
                    e, filtered_data, page, 
                    tab_calendar.controls[1:], # カレンダー部分のみ
                    label
                )
            else:
                # 病棟絞り込みの場合
                UpdateCard.update_cards_with_schedule_data(
                    schedule_data, e, page, label, tab_calendar.controls[1:]
                )
                UpdateCalendar.update_calendar_with_schedule_data(
                    e, schedule_data, page, 
                    tab_calendar.controls[1:], # カレンダー部分のみ
                    label
                )
            
            tab_calendar.update()

        update_button = ft.ElevatedButton(
            text="更新",
            icon=ft.icons.REFRESH,
            on_click=update_card_calendar,
        )

        # 病棟絞り込みの場合は初期カードを作成
        if label != "個人名絞り込み":
            new_cards = UpdateCard.create_card_for_month(
                tab_calendar.year, tab_calendar.month, label
            )
            for card in new_cards:
                tab_calendar.controls.append(card)

        # タブのコンテンツを作成
        tab_content = ft.Column(
            controls=[arrow_navigation, update_button, tab_calendar],
            scroll=ft.ScrollMode.AUTO,
        )

        return tab_content
