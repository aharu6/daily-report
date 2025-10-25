import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart
import os
import re
import pandas as pd
import threading
import ast
from models.models import DataModel
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
            select_directory_path=e.path
            #ディレクトリ内のcsvファイルを全て取得
            csv_files = [f for f in os.listdir(e.path) if f.endswith('.csv')]

            Handlers_Chart.pick_file_name(file_name=csv_files,card=card)
        else:
            select_directory_path = None
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
            hint_text="絞り込み対象名を入力。複数入力する場合はカンマ区切りで入力,例えば: 名前1, 名前2, 名前3",
        )

        filtering_message = ft.Text("絞り込みが完了しました。集計を開始することができます。", color=ft.Colors.GREEN,visible=False)
        filtering_loading=ft.Container()
        #pick_file_nameに該当ファイル名を渡す
        #選択したファイルで結合dfを形成
        #dfを返す
        try:

            file_filer_content.height=1000
            file_filer_content.tabs=[
                ft.Tab(
                    text="絞り込みなし",
                    content=ft.Column()
                ),
                ft.Tab(
                    text="絞り込みあり",
                    content=ft.Column()
                )
            ]

            df_ready_message = ft.Text("選択したファイルを集計する準備ができました。集計を開始することができます。", color=ft.Colors.GREEN,visible = False)
            file_filer_content.tabs[0].content.controls = [
                ft.ElevatedButton("集計準備開始"),
                df_ready_message,
            ]
            am_locations=ft.ResponsiveRow(
                    controls=[
                        ft.Checkbox(
                            label=i,
                            col={"sm": 6, "md": 4, "xl": 2},
                            data = {"location":i,"time":"AM"}) 
                            for i in DataModel.locations()
                    ],
                    )
            pm_locations=ft.ResponsiveRow(
                    controls=[
                        ft.Checkbox(
                            label=i,
                            col={"sm": 6, "md": 4, "xl": 2},
                            data =  {"location":i,"time":"PM"})
                            for i in DataModel.locations()
                    ],
                )
            #絞り込みなしのタブ
            file_filer_content.tabs[0].content.controls[0].on_click=lambda e:SelectDirectoryHandler.concat_files_standard(
                csv_files=csv_files,
                select_directory_path=select_directory_path,
                parent_instance=parent_instance,
                df_ready_message=df_ready_message
            )
            #絞り込みありのタブ
            file_filer_content.tabs[1].content.controls = [
                ft.Text("ファイル絞り込み", size=20),
                ft.Text("絞り込みたい項目を入力してください"),
                #日付
                #開始日#終了日
                ft.Text("日付での絞り込み"),
                start_day_field,
                start_day,
                end_day_field,
                end_day,
                ft.Text("名前で絞り込み"),
                #名前
                filtering_Name,#カンマ区切りで入力してもらって、名前をリストに分解する
                ft.Text("病棟名での絞り込み"),
                ft.Text("AM"),
                am_locations,
                ft.Text("PM"),
                pm_locations,
                #絞り込むのsubmitボタン,
                filtering_loading,
                ft.ElevatedButton(
                    "絞り込み",
                    on_click=lambda e:SelectDirectoryHandler.filter_files(
                        startDay=start_day_field,
                        endDay=end_day_field,
                        filteringName=filtering_Name,
                        fileList=csv_files,
                        filtering_message=filtering_message,
                        card=card,
                        select_directory=select_directory_path,
                        parent_instance=parent_instance,
                        filtering_loading=filtering_loading,
                        am_locations=am_locations,
                        pm_locations=pm_locations
                    )),
                filtering_message,
            ]
            file_filer_content.update()
        except Exception as e:
            print(f"Error in get_directory_result: {e}")
        
    @staticmethod
    def filter_files(
        startDay,endDay,filteringName,fileList,filtering_message,card,select_directory,parent_instance,
        filtering_loading,am_locations,pm_locations):
        filtering_loading.content = ft.Column(
            controls=[
                ft.Text("絞り込み処理を行っています。しばらくお待ちください。"),
                ft.ProgressBar(width=200, height=20),
            ]
        )
        filtering_loading.update()
        #ここで絞り込み処理を行う
        #選択したファイル名を取得して、絞り込み処理を行う
        #絞り込んだファイル名を返す
        startDay= startDay.value if startDay.value else None
        #YYYY-MM-DD形式に変換する
        #date形式に変換する
        startDay = pd.to_datetime(startDay, errors='coerce')
        endDay= endDay.value if endDay.value else None
        endDay = pd.to_datetime(endDay, errors='coerce')
        filteringName = filteringName.value if filteringName.value else None
        # filteringNameは複数入力の場合カンマ区切り、分ける
        if filteringName:
            filteringNameList = [name.strip() for name in filteringName.split(',')]
        else:
            filteringNameList = []

        #ここで絞り込み処理を行う
        ##日付の絞り込み
        #開始日から終了日までの期間に該当するファイルを絞り込む
        result_day_files= []
        for file in fileList:
            #ファイル名から日付を取得する
            file_date_str = re.search(r'\d{4}-\d{1,2}-\d{1,2}', file)
            #file_date_strから日付を取得する
            if file_date_str:
                file_date = file_date_str.group(0)
                #date形式に変換する
                file_date = pd.to_datetime(file_date, errors='coerce')                
                if startDay and endDay:
                    if startDay <= file_date <= endDay:
                        result_day_files.append(file)
                elif startDay and not endDay:
                    if startDay <= file_date:
                        result_day_files.append(file)
                elif not startDay and endDay:
                    if file_date <= endDay:
                        result_day_files.append(file)
                else:
                    pass
        #名前で絞り込み
        result_name_files=[]
        if filteringNameList:
            for file in fileList:
                for name in filteringNameList:
                    if re.search(name,file):
                        result_name_files.append(file)
        else:
            pass

        #病棟名での絞り込み
        #各ファイルをそれぞれ開いて、AM:一行目、PM:18もしくは19行目
        #checkboxで取得したデータと照合
        #午前の病棟データ
        AM_location= [loc.data["location"] for loc in am_locations.controls if loc.value]
        PM_location= [loc.data["location"] for loc in pm_locations.controls if loc.value]
        result_location_files_am=[]
        result_location_files_pm=[]
        for file in fileList:
            if os.path.isfile(os.path.join(select_directory, file)):
                df = pd.read_csv(os.path.join(select_directory, file), encoding=Handlers_Chart.detect_encoding(file_path=os.path.join(select_directory, file)))
                #AMの病棟名で絞り込み
                if AM_location:
                    #df['locate]は文字列のリスト形式
                    #午前が含まれるのは0行目から15行目まで
                    #ユニークな文字列を取得する
                    am_locate=df["locate"].head(16).unique()
                    result_am=any(loc in l for l in am_locate for loc in AM_location)
                    if result_am== True:
                        result_location_files_am.append(file)
                #PMの病棟名で絞り込み
                if PM_location:
                    #df['locate]は文字列のリスト形式
                    #午後が含まれるのは16行目から55行目まで
                    pm_locate=df["locate"].tail(40).unique()
                    print(f"午後の病棟名: {pm_locate}filename: {file}")
                    result_pm=any(loc in l for l in pm_locate for loc in PM_location)
                    if result_pm== True:
                        result_location_files_pm.append(file)
                
    
        #日付、名前、午前病棟、午後病棟全て入力あれば合致したファイルのみを返す
        #日付だけなら、日付で絞り込んだファイルを返す
        #名前だけなら、名前で絞り込んだファイルを返す
        #午前病棟だけなら、午前病棟で絞り込んだファイルを返す
        #午後病棟だけなら、午後病棟で絞り込んだファイルを返す
        #リストが空の場合には全てのファイル名を入れておく
        #最後に&条件で全てに合致するファイルだけを返す
        if not result_day_files:
            result_day_files = [l for l in fileList]
        print(f"日付で絞り込んだファイル: {result_day_files}")
        if not result_name_files:
            result_name_files = [l for l in fileList]
        print(f"名前で絞り込んだファイル: {result_name_files}")
        if not result_location_files_am:
            result_location_files_am=[l for l in fileList]
        print(f"午前病棟で絞り込んだファイル: {result_location_files_am}")

        if not result_location_files_pm:
            result_location_files_pm=[l for l in fileList]

        print(f"午後病棟で絞り込んだファイル: {result_location_files_pm}")
        #全ての条件で絞り込んだファイルを取得する
        result_files = list(set(result_day_files) & set(result_name_files) & set(result_location_files_am) & set(result_location_files_pm))

        #絞り込んだファイルにて 「読み込んだファイル一覧」を更新する
        Handlers_Chart.pick_file_name(file_name=result_files, card=card)
        #絞り込んだデータで結合dfを作成する
        SelectDirectoryHandler.concat_files(file_names=result_files, select_directory=select_directory,parent_instance=parent_instance)
        #絞り込みが完了したことを通知するメッセージを表示する
        #locadingを非表示にする
        filtering_loading.content=None
        filtering_loading.update()
        filtering_message.visible = True
        filtering_message.update()
        threading.Timer(
            10,
            lambda: SelectDirectoryHandler._hide(filtering_message)
        ).start()
    
    @staticmethod
    def concat_files(file_names, select_directory,parent_instance):
        #選択したファイル名を取得して、結合処理を行う
        #結合したデータフレームを返す
        #選択したファイルのパスを取得
        file_paths = [os.path.join(select_directory, file_name) for file_name in file_names]
        #データフレームを結合する
        df=pd.concat(
            [pd.read_csv(file,encoding=Handlers_Chart.detect_encoding(file_path=file)) for file in file_paths if os.path.isfile(file)],
        )
        #病棟関係ない項目はlocationデータを削除　selfなどの名前にしておく
        for index,row in df.iterrows():
            if row["task"]in["委員会","勉強会参加","WG活動","1on1","業務調整","休憩"]:#その他は除外する
                df.loc[index,"locate"] = "['self']"
            else:
                pass
        new_rows=[]
        for index,row in df.iterrows():
            tarn_row=ast.literal_eval(row["locate"])
            for loc in range(len(tarn_row)):
                new_row=row.copy()
                new_row["locate"]=tarn_row[loc]
                new_rows.append(new_row)
        parent_instance.dataframe= pd.DataFrame(new_rows)
        print(f"Concatenated DataFrame:\n{parent_instance.dataframe.head()}")

    @staticmethod
    def concat_files_standard(csv_files, select_directory_path, parent_instance,df_ready_message):
        SelectDirectoryHandler.concat_files(
                        file_names=csv_files,
                        select_directory=select_directory_path,
                        parent_instance=parent_instance
                    )
        df_ready_message.visible= True
        df_ready_message.update()
        threading.Timer(
            10,
            lambda:SelectDirectoryHandler._hide(df_ready_message)
        ).start()