import flet as ft
import datetime
from create_calendar import CreateCalendar
from update_card import UpdateCard
from update_calendar import UpdateCalendar
from calendar_updater import CalendarUpdater

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
            CalendarUpdater.update_calendar_and_text(
                e=e, is_forward=is_forward, page=page, tab_calendar=tab_calendar,
                label=label, schedule_data=schedule_data, tab_header=tab_header
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

        def update_card_calender(e, schedule_data, page, label, tab_calendar):
            """カードとカレンダーの更新"""
            CalendarUpdater.update_card_calendar(
                e=e, schedule_data=schedule_data, page=page, label=label, tab_calendar=tab_calendar
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