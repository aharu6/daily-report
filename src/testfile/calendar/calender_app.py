import flet as ft
from flet import View
import datetime
import math
from create_calendar import CreateCalendar
from read_folder import ReadFolder  
from update_card import UpdateCard
from update_calendar import UpdateCalendar
def main(page: ft.Page):
    page.title = "calendar"
    page.window.width = 1400
    page.window.height = 1000
    page.scroll = True

    # 現在の日付を取得
    today = datetime.date.today()
    # 現在の年と月を取得
    current_year = today.year
    current_month = today.month

    #スケジュールデータを保存する変数
    schedule_data=[]
    #全てのタブのカレンダーを保存するリスト

    # タイトル
    page.add(ft.Text(f"calender", size=30, weight=ft.FontWeight.BOLD))

    file_picker = ft.FilePicker(
        on_result = lambda e:ReadFolder.read_folder(e=e, schedule_data=schedule_data, page=page),
    )
    
    page.overlay.append(file_picker)
    #フォルダ読み込みのボタンを作成
    read_folder_button=ft.ElevatedButton(
        text="読み込むフォルダを選択",
        on_click=lambda _:file_picker.get_directory_path(),
        icon=ft.icons.FOLDER_OPEN,
        
    )

    # 病棟ラベル
    locate_labels = [
        "ICU", "OR", "HR", "1E", "3A", "3B", "3C", "CCU",
        "4A", "4B", "4C", "4D", "HCU",
        "5A", "5B", "5C", "5D", "DI"
    ]

    # 各タブのカレンダーを作成する関数
    def create_tab_content(label):
        """_summary_

        Args:
            label (_type_): 病棟名

        Returns:
            _type_: _description_
        """
        # 各タブ用のカレンダーを作成
        tab_calendar = CreateCalendar.create_calendar(current_year, current_month)
        
        # 年月表示用のテキスト
        date_text = ft.Text(f"{current_year}年{current_month}月", size=30, weight=ft.FontWeight.BOLD)
        
        # カレンダー更新時に年月表示,カードも更新する関数
        def update_calendar_and_text(e, is_forward=True):
            if is_forward:
                CreateCalendar.forward_month(e=e, page=page, calendar=tab_calendar, card_name=label)
            else:
                CreateCalendar.back_month(e=e, page=page, calendar=tab_calendar, card_name=label)

            # 年月表示を更新
            date_text.value = f"{tab_calendar.year}年{tab_calendar.month}月"
            date_text.update()

            #カードの更新
            #既存のカードを削除
            calendar_controls_content=len([control for control in tab_calendar.controls if not isinstance(control,ft.Card)])
            while len(tab_calendar.controls) > calendar_controls_content:
                tab_calendar.controls.pop()

            new_cards = UpdateCard.create_card_for_month(year=tab_calendar.year, month=tab_calendar.month, label=label)
            tab_calendar.controls.extend(new_cards)
            tab_calendar.update()
            
            # カードの内容を更新 
            UpdateCard.update_cards_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, card_name=label,
                card=tab_calendar.controls[1:]
            )

            #カレンダーセルの色を更新
            UpdateCalendar.update_calendar_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls[1:],
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
        
        # 矢印ナビゲーション
        arrow = ft.Row([
            back_button,
            date_text,
            next_button
        ], alignment=ft.MainAxisAlignment.CENTER)

        def update_card_calender(e,schedule_data,page,label,tab_calendar):
            #カードの更新
            UpdateCard.update_cards_with_schedule_data(
                e=e,schedule_data=schedule_data,page=page,card_name=label,
                card=tab_calendar.controls
            )
            #カレンダーの更新
            UpdateCalendar.update_calendar_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, calendar=tabs.tabs[0].content.controls[2].controls[1:],
                card_name=locate_labels[0]) #更新ボタンを取得するページによってlocateは調節が必要かもしれない
            
        update_button=ft.ElevatedButton(
            text="更新",
            on_click=lambda e: update_card_calender(e=e,schedule_data=schedule_data,page=page,
                                                    label=label,tab_calendar=tab_calendar),
            icon=ft.icons.REFRESH,
            
        )
        # 日付ごとのカードの作成
        days_in_month= (datetime.date(current_year, current_month + 1, 1) - datetime.date(current_year, current_month, 1)).days
        for j in range(1, days_in_month + 1):
            tab_calendar.controls.append(
                ft.Card(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"{current_month}月{j}日"),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(label=ft.Text("name"), numeric=True),
                                    ft.DataColumn(label=ft.Text("AM or PM"), numeric=True),
                                ],
                                rows=[
                                    # 担当者の名前が入る
                                    ft.DataRow(cells=[ft.DataCell(ft.Text("name")), ft.DataCell(ft.Text("AM or PM"))])
                                ]
                            )
                        ],
                        data={"date": f"{current_year}-{current_month:01d}-{j:01d}", "locate": label},  # カードに日付
                    ),
                )
            )
        # タブのコンテンツを作成
        tab_content = ft.Column(controls=[arrow, update_button,tab_calendar])
        
        return tab_content

    #病棟ごとにタブを作成
    tabs=ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text=label, content=create_tab_content(label)) for label in locate_labels
        ],
        expand=True,
        animation_duration=300,
        indicator_color=ft.colors.BLUE,
    )
    # タブごとにカードを作成する
    # 月切り替えに応じてカードの日付を更新する
    
    #ファイルを読み込んで日付、名前、病棟名を抽出、datatableに追加する
    #保存データはclientstorageに保存
    #名前での絞り込み機構はどこに入れようか

    page.add(read_folder_button,tabs,)
    
    #読み込みによりschedule_dataが更新されるので、タブの内容を更新する
    UpdateCard.update_cards_with_schedule_data(
        schedule_data=schedule_data, e=None, page=page, card_name=locate_labels[0],  # 初回起動時はindex=0を選択しているので、渡すlabel(病棟名も)label[0]で良い
        card=tabs.tabs[0].content.controls[2].controls  # 最初のタブのカードリストを取得
        )
    # データがある場合にカレンダーに色をつける更新
    UpdateCalendar.update_calendar_with_schedule_data(
        e=None, schedule_data=schedule_data, page=page, calendar=tabs.tabs[0].content.controls[2].controls[1:],
        card_name=locate_labels[0],
    )
ft.app(main)
