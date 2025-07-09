import flet as ft
from flet import View
import datetime
import math
from create_calendar import CreateCalendar
from read_folder import ReadFolder  
from update_card import UpdateCard
from update_calendar import UpdateCalendar
from tab_content_creator import TabContentCreator

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

    folder_name=ft.Text(
        "選択中のフォルダ名",
    )
    #起動時、前回読み込んだフォルダがある場合には名前を表示する
    try:
        folder_name.value=f"選択中のフォルダ名{page.client_storage.get("folder_name")}"
    except:
        pass

    file_picker = ft.FilePicker(
        on_result = lambda e:ReadFolder.read_folder(e=e, schedule_data=schedule_data, page=page,folder_name=folder_name),
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

    #内容ごとに
    tabs=ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text=label, content=TabContentCreator.create_tab_content(label=label, page=page, schedule_data=schedule_data)) for label in locate_labels
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
    def handle_filter_change(e,tabs):
        if e.control.value==True:
            tabs.tabs=[
                ft.Tab(text=label, content=TabContentCreator.create_tab_content(label, page, schedule_data)) for label in locate_labels
            ]
        elif e.control.value==False:
            tabs.tabs=[ft.Tab(text="個人名絞り込み")]
        tabs.update()
    
    #　病棟絞り込みと名前絞り込み機能の切り替え
    change_filter=ft.Switch(
        label="病棟絞り込み",
        value=True,
        on_change=lambda e:handle_filter_change(e=e,tabs=tabs)
    )

    page.add(read_folder_button,folder_name,change_filter,tabs,)
    
    #読み込みによりschedule_dataが更新されるので、タブの内容を更新する
    UpdateCard.update_cards_with_schedule_data(
        schedule_data=schedule_data, e=None, page=page, card_name=locate_labels[0],  # 初回起動時はindex=0を選択しているので、渡すlabel(病棟名も)label[0]で良い
        card=tabs.tabs[0].content.controls[2].controls  # 最初のタブのカードリストを取得
        )
    # データがある場合にカレンダーに色をつける更新
    UpdateCalendar.update_calendar_with_schedule_data(
        e=None, 
        schedule_data=schedule_data, 
        page=page, 
        calendar=tabs.tabs[0].content.controls[2].controls[1:],
        card_name=locate_labels[0],#初回起動時はtab==ICUなのでlocate_labels[0]を渡す
    )
ft.app(main)
