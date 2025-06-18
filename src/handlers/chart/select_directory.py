import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart
import os
#select directory
#フォルダ選択した結果
class SelectDirectoryHandler:
    @staticmethod
    def get_directory_result(e:ft.FilePickerResultEvent,page,card,parent_instance,selected_files,file_filer_content):
        Handlers_Chart.show_progress_bar(card,parent_instance.page)
        if e.path:
            page.client_storage.set("selected_directory", e.path)
            page.update()
            print(f"Selected directory: {e.path}")
            #ディレクトリ内のcsvファイルを全て取得
            csv_files = [f for f in os.listdir(e.path) if f.endswith('.csv')]

            Handlers_Chart.pick_file_name(file_name=csv_files,card=card)
        else:
            print("No directory selected")

        #ファイル絞り込みボタンを表示する
        #pick_file_nameに該当ファイル名を渡す
        #選択したファイルで結合dfを形成
        #dfを返す
        try:
            file_filer_content.controls.clear()
            file_filer_content.controls = [
                ft.Text("ファイル絞り込み", size=20),
                ft.Text("絞り込みたい項目を入力してください"),
                #日付
                #開始日#終了日
                ft.ElevatedButton(
                    "開始日",
                    on_click = lambda e :page.open(
                        ft.DatePicker()
                    )
                ),
                ft.ElevatedButton(
                    "終了日",
                    on_click = lambda e :page.open(
                        ft.DatePicker()
                    )
                ),
                ft.Text("名前で絞り込み"),
                #名前
                ft.TextField(
                    label="名前",
                    hint_text="絞り込み対象名を入力。複数入力する場合はカンマ区切りで入力"
                ),#カンマ区切りで入力してもらって、名前をリストに分解する
                #絞り込むのsubmitボタン
                ft.ElevatedButton("絞り込み",on_click=lambda e:SelectDirectoryHandler.filter_files())
            ]
            file_filer_content.update()
        except Exception as e:
            print(f"Error in get_directory_result: {e}")
        
    @staticmethod
    def filter_files():
        #ここで絞り込み処理を行う
        #選択したファイル名を取得して、絞り込み処理を行う
        #絞り込んだファイル名を返す
        print("Filtering files...")