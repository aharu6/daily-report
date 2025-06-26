import flet as ft
from flet import View
import datetime
import math
from create_calendar import CreateCalendar
from read_folder import ReadFolder  

def main(page: ft.Page):
    page.title = "calendar"
    page.window.width = 1400
    page.window.height = 1000
    page.scroll = True
    back_month_button=ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_size=30,
        on_click=lambda e: page.add(ft.Text("前の月を表示する処理をここに追加")),
        tooltip="前の月",
    )
    next_month_button=ft.IconButton(
        icon=ft.icons.ARROW_FORWARD,
        icon_size=30,
        on_click=lambda e: page.add(ft.Text("次の月を表示する処理をここに追加")),
        tooltip="次の月",
    )   

    # 現在の日付を取得
    today = datetime.date.today()
    # 現在の年と月を取得
    current_year = today.year
    current_month = today.month

    # カレンダーを作成
    calendar = CreateCalendar.create_calendar(current_year, current_month)
    # ページにカレンダーを追加
    page.add(ft.Text(f"calender", size=30, weight=ft.FontWeight.BOLD))
    arrow=ft.Row([
        back_month_button,
        ft.Text(f"{current_year}年{current_month}月", size=30, weight=ft.FontWeight.BOLD),
        next_month_button
    ])
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

    #日付ごとにカードを作成、データフレームを作成する
    card_rows=ft.Column()
    #月の日付でカードを作成する
    #月の日付でカードを作成する

    days_in_month=(datetime.date(current_year, current_month + 1, 1) - datetime.date(current_year, current_month, 1)).days
    for i in range(1, days_in_month + 1):
        card_rows.controls.append(
            ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Text(i),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(label=ft.Text(""), numeric=True),
                                ft.DataColumn(label=ft.Text("記録者"), numeric=True),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[ft.DataCell(ft.Text("病棟名")), ft.DataCell(ft.Text("名前"))],
                                )
                            ]
                        )
                    ]
                ),
            )
        )
        
    #clientstorageから保存データを呼び出し、取得
    #ファイルを読み込んで日付、名前、病棟名を抽出、datatableに追加する
    #保存データはclientstorageに保存

    page.add(arrow, calendar,read_folder_button,card_rows,)

ft.app(main)
