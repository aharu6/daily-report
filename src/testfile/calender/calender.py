import flet as ft
from flet import View
import datetime
import math
from create_calendar import CreateCalendar
from read_folder import ReadFolder  
from update_card import UpdateCard
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

    # タイトル
    page.add(ft.Text(f"calender", size=30, weight=ft.FontWeight.BOLD))

    file_picker = ft.FilePicker(
        on_result = lambda e:ReadFolder.read_folder(e=e)
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
        # 各タブ用のカレンダーを作成
        tab_calendar = CreateCalendar.create_calendar(current_year, current_month)
        
        # 年月表示用のテキスト
        date_text = ft.Text(f"{current_year}年{current_month}月", size=30, weight=ft.FontWeight.BOLD)
        
        # カレンダー更新時に年月表示,カードも更新する関数
        def update_calendar_and_text(e, is_forward=True):
            if is_forward:
                CreateCalendar.forward_month(e, page, tab_calendar)
            else:
                CreateCalendar.back_month(e, page, tab_calendar)
            # 年月表示を更新
            date_text.value = f"{tab_calendar.year}年{tab_calendar.month}月"
            date_text.update()

            #カードの更新
            #既存のカードを削除
            calendar_controls_content=len([control for control in tab_calendar.controls if not isinstance(control,ft.Card)])
            while len(tab_calendar.controls) > calendar_controls_content:
                tab_calendar.controls.pop()
            
            new_cards = UpdateCard.create_card_for_month(tab_calendar.year, tab_calendar.month)
            tab_calendar.controls.extend(new_cards)
            tab_calendar.update()


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
                                    ft.DataColumn(label=ft.Text("担当者名"), numeric=True),
                                    ft.DataColumn(label=ft.Text("病棟名"), numeric=True),
                                ],
                                rows=[
                                    # 担当者の名前が入る
                                    ft.DataRow(cells=[ft.DataCell(ft.Text("担当者1")), ft.DataCell(ft.Text(label))])
                                ]
                            )
                        ]
                    ),
                )
            )
        # タブのコンテンツを作成
        tab_content = ft.Column(controls=[arrow, tab_calendar])
        
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
    
    #clientstorageから保存データを呼び出し、取得
    #ファイルを読み込んで日付、名前、病棟名を抽出、datatableに追加する
    #保存データはclientstorageに保存

    page.add(read_folder_button,tabs,)

ft.app(main)
