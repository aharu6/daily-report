import flet as ft
import datetime
from create_calendar import CreateCalendar
from update_card import UpdateCard
from update_calendar import UpdateCalendar

class TabContentCreator:
    @staticmethod
    def create_tab_content(label,page, schedule_data,):
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

        # カレンダー更新時に年月表示,カードも更新する関数
        def update_calendar_and_text(e, is_forward=True):
            if is_forward:
                CreateCalendar.forward_month(e=e, page=page, calendar=tab_calendar, card_name=label)
            else:
                CreateCalendar.back_month(e=e, page=page, calendar=tab_calendar, card_name=label)

            # 年月表示を更新
            tab_header.value = f"{tab_calendar.year}年{tab_calendar.month}月"
            tab_header.update()

            #カードの更新
            #既存のカードを削除
            calendar_controls_content = len([control for control in tab_calendar.controls if not isinstance(control, ft.Card)])
            while len(tab_calendar.controls) > calendar_controls_content:
                tab_calendar.controls.pop()

            # 新しいカードを作成・追加
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
                                                ft.DataCell(ft.Text("AM/PM"))
                                            ]
                                        )   # 仮のデータ行
                                    ]
                                )
                            ],
                            data={"date": f"{tab_calendar.year}-{tab_calendar.month:01d}-{index + 1:01d}", "locate": label},
                        )
                    )
                )
            tab_calendar.update()

            # カードの内容を更新 
            UpdateCard.update_cards_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, card_name=label,
                card=tab_calendar.controls[calendar_controls_content:]
            )

            #カレンダーセルの色を更新
            UpdateCalendar.update_calendar_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls[calendar_controls_content:],
                card_name=label,
            )           
        # 各タブ用のボタンを作成
        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_size=30,
            on_click=lambda e: update_calendar_and_text(e, False),
            tooltip="前の月",
        )
        next_button = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            icon_size=30,
            on_click=lambda e: update_calendar_and_text(e, True),
            tooltip="次の月",
        )   
        #矢印ナビゲーション
        arrow_navigation = ft.Row([
            back_button,
            tab_header,
            next_button
        ],alignment=ft.MainAxisAlignment.CENTER)

        def update_card_calender(e,schesule_data,page,label,tab_calendar):
            """_summary_

            Args:
                e (_type_): _description_
                schedule_data (_type_): _description_
                page (_type_): _description_
                label (_type_): _description_
                tab_calendar (_type_): _description_
            """
            #カードの更新
            UpdateCard.update_cards_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, card_name=label,
                card=tab_calendar.controls[1:]
            )

            #カレンダーセルの色を更新
            UpdateCalendar.update_calendar_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls[1:],
                card_name=label,
            )
        
        #更新ボタン
        update_button=ft.ElevatedButton(
            text="更新",
            on_click=lambda e: update_card_calender(e, schedule_data, page, label, tab_calendar)    ,
            icon=ft.icons.REFRESH,
        )
        # 日付ごとのカードの作成
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
                                            ft.DataCell(ft.Text("AM/PM"))
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