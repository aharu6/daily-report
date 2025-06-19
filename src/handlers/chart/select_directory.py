import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart
import os
import re
import pandas as pd
import threading
#select directory
#フォルダ選択した結果
class SelectDirectoryHandler:
    @staticmethod
    def _hide(message):
        message.visible = False
        message.update()
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
        # DatePickerウィジェットを作成し、選択した日付をstart_day_fieldに格納する
        start_day_field = ft.TextField(label="開始日", read_only=True)
        start_day_picker = ft.DatePicker(
            on_change=lambda e: (
                setattr(start_day_field, 'value', str(e.data)),
                start_day_field.update()
            )
        )
        start_day = ft.ElevatedButton(
            "開始日",
            on_click=lambda e: page.open(start_day_picker)
        )
        # 終了日も同様に作成
        end_day_field = ft.TextField(label="終了日", read_only=True)
        end_day_picker = ft.DatePicker(
            on_change=lambda e: (
                setattr(end_day_field, 'value', str(e.data)),
                end_day_field.update()
            )
        )
        end_day = ft.ElevatedButton(
            "終了日",
            on_click=lambda e: page.open(end_day_picker)
        )

        
        filtering_Name = ft.TextField(
            label="名前",
            hint_text="絞り込み対象名を入力。複数入力する場合はカンマ区切りで入力,例えば: 名前1, 名前2,名字のみ可能",
        )

        filtering_message = ft.Text("絞り込みが完了しました。", color=ft.colors.GREEN,visible=False)
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
                start_day_field,
                start_day,
                end_day_field,
                end_day,
                ft.Text("名前で絞り込み"),
                #名前
                filtering_Name,#カンマ区切りで入力してもらって、名前をリストに分解する
                #絞り込むのsubmitボタン
                ft.ElevatedButton(
                    "絞り込み",
                    on_click=lambda e:SelectDirectoryHandler.filter_files(
                        startDay=start_day_field,
                        endDay=end_day_field,
                        filteringName=filtering_Name,
                        fileList=csv_files,
                        filtering_message=filtering_message,
                        )),
                filtering_message,
            ]
            file_filer_content.update()
        except Exception as e:
            print(f"Error in get_directory_result: {e}")
        
    @staticmethod
    def filter_files(startDay,endDay,filteringName,fileList,filtering_message):
        #ここで絞り込み処理を行う
        #選択したファイル名を取得して、絞り込み処理を行う
        #絞り込んだファイル名を返す
        startDay= startDay.value if startDay.value else None
        #YYYY-MM-DD形式に変換する
        #date形式に変換する
        startDay = pd.to_datetime(startDay, errors='coerce')
        print(f"Start Day: {startDay}")
        print(type(startDay))
        endDay= endDay.value if endDay.value else None
        endDay = pd.to_datetime(endDay, errors='coerce')
        print(f"End Day: {endDay}")
        filteringName = filteringName.value if filteringName.value else None
        # filteringNameは複数入力の場合カンマ区切り、分ける
        if filteringName:
            filteringNameList = [name.strip() for name in filteringName.split(',')]
        else:
            filteringNameList = []

        #ここで絞り込み処理を行う
        #開始日から終了日までの期間に該当するファイルを絞り込む
        result_files= []
        for file in fileList:
            #ファイル名から日付を取得する
            file_date_str = re.search(r'\d{4}-\d{1,2}-\d{1,2}', file)
            print(f"Processing file: {file_date_str}")
            #file_date_strから日付を取得する
            if file_date_str:
                file_date = file_date_str.group(0)
                #date形式に変換する
                file_date = pd.to_datetime(file_date, errors='coerce')

                print(f"File Date: {file_date}")
                
                if startDay and endDay:
                    if startDay <= file_date <= endDay:
                        result_files.append(file)
                else:
                    pass
        print(f"Filtered files: {result_files}")
        filtering_message.visible = True
        filtering_message.update()
        threading.Timer(
            10,
            lambda: SelectDirectoryHandler._hide(filtering_message)
        ).start()