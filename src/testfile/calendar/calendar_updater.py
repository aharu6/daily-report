import flet as ft
from create_calendar import CreateCalendar
from update_card import UpdateCard
from update_calendar import UpdateCalendar

class CalendarUpdater:
    @staticmethod
    def update_calendar_and_text(e, is_forward, page, tab_calendar, label, schedule_data, tab_header):
        """カレンダー更新時に年月表示、カードも更新する関数
        
        Args:
            e: イベント
            is_forward (bool): True=次の月, False=前の月
            page: ページオブジェクト
            tab_calendar: カレンダーオブジェクト
            label (str): 病棟名
            schedule_data: スケジュールデータ
            tab_header: 年月表示用テキスト
        """
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
                                            ft.DataCell(ft.Text("AM or PM"))
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

    @staticmethod
    def update_card_calendar(e, schedule_data, page, label, tab_calendar):
        """カードとカレンダーの更新
        
        Args:
            e: イベント
            schedule_data: スケジュールデータ
            page: ページオブジェクト
            label (str): 病棟名
            tab_calendar: カレンダーオブジェクト
        """
        # カード以外のコントロール数を取得
        calendar_controls_content = len([control for control in tab_calendar.controls if not isinstance(control, ft.Card)])
        
        #カードの更新
        UpdateCard.update_cards_with_schedule_data(
            e=e, schedule_data=schedule_data, page=page, card_name=label,
            card=tab_calendar.controls[calendar_controls_content:]
        )

        #カレンダーセルの色を更新
        UpdateCalendar.update_calendar_with_schedule_data(
            e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls[calendar_controls_content:],
            card_name=label,
        )
