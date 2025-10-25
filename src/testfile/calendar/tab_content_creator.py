import flet as ft
import datetime
from create_calendar import CreateCalendar
from update_card import UpdateCard
from update_calendar import UpdateCalendar
from calendar_updater import CalendarUpdater
class TabContentCreator:
    @staticmethod
    def create_tab_content(label,page, schedule_data,switch_value):
        """_summary_

        Args:
            label (_type_): 病棟名
        Returns:
            _type_: _description_
        """
        # 各タブ用のカレンダーを作成
        tab_calendar = CreateCalendar.create_calendar(datetime.datetime.now().year, datetime.datetime.now().month)

        # 年月表示用のテキスト
        tab_header = ft.Text(f"{datetime.datetime.now().year}年{datetime.datetime.now().month}月", size=30, weight=ft.FontWeight.BOLD)

        # チェックボックス用の変数を初期化
        checkboxes = None

        # label=="個人名絞り込み"の場合、先にチェックボックスを作成
        if label=="個人名絞り込み":
            #schedule_data=[] の場合はclientstorageからデータを取得する
            if not schedule_data:
                try:
                    schedule_data = page.client_storage.get("schedule_data")
                    if schedule_data is None:
                        schedule_data = []
                except Exception as e:
                    schedule_data = []
            else:
                schedule_data = schedule_data   #あればそのまま使用する

            #schedule_dataからユニークな名前データを抽出してチェックボックスを作成する
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
            tab_calendar.controls.append(
                checkboxes
            )

        # カレンダー更新時に年月表示,カードも更新する関数
        def update_calendar_and_text(e, is_forward=True,switch_value=switch_value):
            CalendarUpdater.update_calendar_and_text(
                e=e, is_forward=is_forward, page=page, tab_calendar=tab_calendar,
                label=label, schedule_data=schedule_data, tab_header=tab_header,
                switch_value=switch_value
            )           
        
        # 各タブ用のボタンを作成
        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_size=30,
            on_click=lambda e: update_calendar_and_text(e=e, is_forward=False,switch_value=switch_value),
            tooltip="前の月",
        )
        next_button = ft.IconButton(
            icon=ft.Icons.ARROW_FORWARD,
            icon_size=30,
            on_click=lambda e: update_calendar_and_text(e=e, is_forward=True,switch_value=switch_value),
            tooltip="次の月",
        )   
        #矢印ナビゲーション
        arrow_navigation = ft.Row(
            [
                back_button,
                tab_header,
                next_button
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        def update_card_calender(e, schedule_data, page, label, tab_calendar):
            """カードとカレンダーの更新"""
            CalendarUpdater.update_card_calendar(
                e=e, schedule_data=schedule_data, page=page, label=label, tab_calendar=tab_calendar,
                )
        
        #更新ボタン
        update_button=ft.ElevatedButton(
            text="更新",
            icon=ft.Icons.REFRESH,
        )
        # 日付ごとのカードの作成
        #label==病棟名と　個人名絞り込みで場合分けする
        if label=="個人名絞り込み":
            #更新ボタンの関数定義 - 動的に最新のチェックボックスを取得
            def update_with_current_checkboxes(e):
                # tab_calendarから最新のチェックボックスを動的に取得
                current_checkboxes = None
                for control in tab_calendar.controls:
                    if isinstance(control, ft.ResponsiveRow):
                        # ResponsiveRowの中にチェックボックスがあるかチェック
                        if control.controls and isinstance(control.controls[0], ft.Checkbox):
                            current_checkboxes = control
                            break
                
                if current_checkboxes:
                    CalendarUpdater.update_calendar_with_personal_data(
                        e=e, page=page, checkboxes=current_checkboxes, tab_calendar=tab_calendar
                    )
                else:
                    print("現在のチェックボックスが見つかりません")
            
            update_button.on_click = update_with_current_checkboxes
            #update_calender_with_schedule_data関数とpersonal_filter関数の両方が必要
            #update_calender_with_personal_data関数を呼び出す

        else:#病棟絞り込みの場合
            #更新ボタン関数
            update_button.on_click=lambda e: update_card_calender(
                e=e, schedule_data=schedule_data, page=page, label=label,
                tab_calendar=tab_calendar
            )

            #日付カード
            new_cards = UpdateCard.create_card_for_month(year=tab_calendar.year, month=tab_calendar.month, label=label)
            for index, card in enumerate(new_cards):
                tab_calendar.controls.append(
                    ft.Card(
                        content=ft.Column(
                            controls=[
                                ft.Text(f"{tab_calendar.month}月{index + 1}日"),
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(label=ft.Text("name"), numeric=True),
                                        ft.DataColumn(label=ft.Text("AM or PM"), numeric=True),
                                    ],
                                    rows=[
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(ft.Text("担当者名")),
                                                ft.DataCell(ft.Text("AM or PM"))
                                            ]
                                        )   # 仮のデータ行
                                    ]
                                )
                            ],
                            data={"date": f"{tab_calendar.year}-{tab_calendar.month:01d}-{index + 1:01d}", "locate": label},  # カードに日付
                        )
                    )
                )
        # タブのコンテンツを作成
        tab_content = ft.Column(controls=[arrow_navigation, update_button, tab_calendar])

        return tab_content