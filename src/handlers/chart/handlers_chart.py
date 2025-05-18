import pandas as pd
import flet as ft
from flet import FilePicker, FilePickerResultEvent
import ast
import plotly
import plotly.express as px
import plotly.io as pio
from flet.plotly_chart import PlotlyChart
import chart_studio.plotly as py
from handlers.chart.download_handler import Chart_Download_Handler
from handlers.chart.period_handler import PeriodHandler
import datetime
import chardet
pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None)
# Chartページ用のハンドラ
class Handlers_Chart:
    @staticmethod
    def detect_encoding(file_path):
        with open(file_path,'rb') as f:
            result=chardet.detect(f.read())

        return result['encoding']
    @staticmethod
    def pick_file_result(e: ft.FilePickerResultEvent, selected_files, parent_instance,card):
        """_summary
        Args:
            e (ft.FilePickerResultEvent): _description_
            selected_files (_type_): _description_
            parent_instance (_type_): _description_
        """
        Handlers_Chart.show_progress_bar(card, parent_instance.page)
        if e.files:
            selected_files.text = ",".join(map(lambda x: x.name, e.files))
            file_paths = [f.path for f in e.files]
            file_name=[f.name for f in e.files]
            
            try:
                # ファイルの数だけ繰り返す
                dat = pd.concat(
                    [pd.read_csv(file_path,encoding=Handlers_Chart.detect_encoding(file_path=file_path)) 
                    for file_path in file_paths]
                )
                #病棟関係ない項目は複数locationデータを削除 selfなどの名前にしておく
                for index,row in dat.iterrows():
                    if row["task"]in["委員会","勉強会参加","WG活動","1on1","業務調整","休憩","その他"]:
                        dat.loc[index,"locate"]="['self']"
                    else:
                        pass
                new_rows = []
                for index, row in dat.iterrows():
                    tarn_row = ast.literal_eval(row["locate"])
                    for loc in range(len(tarn_row)):
                        new_row = row.copy()
                        new_row["locate"] = tarn_row[loc]
                        new_rows.append(new_row)
                parent_instance.dataframe=pd.DataFrame(new_rows)
            except Exception as e:
                print(f"An error occurred: {e}")    
                # 例外処理を追加
                dat= pd.concat(
                    [pd.read_csv(file_path,encoding=Handlers_Chart.detect_encoding(file_path=file_path)) 
                    for file_path in file_paths]
                )
                #病棟関係ない項目は複数locationデータを削除 selfなどの名前にしておく
                for index,row in dat.iterrows():
                    if row["task"]in["委員会","勉強会参加","WG活動","1on1","業務調整","休憩","その他"]:
                        dat.loc[index,"locate"]="['self']"
                    else:
                        pass    
                new_rows = []
                for index,row in dat.iterrows():
                    if isinstance(row["locate"],str):
                        try:
                            tarn_row =row["locate"]
                            new_row=row.copy()
                            new_row["locate"]=tarn_row
                            new_rows.append(new_row)
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            continue
                    else:
                        try:
                            tarn_row = ast.literal_eval(row["locate"])
                            for loc in range(len(tarn_row)):
                                new_row=row.copy()
                                new_row["locate"]=tarn_row[loc]
                                new_rows.append(new_row)
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            continue
                parent_instance.dataframe=pd.DataFrame(new_rows)


            #ファイル名の表示
            Handlers_Chart.pick_file_name(file_name,card)

    @staticmethod
    def pick_file_name(file_name,card):
        card_list=[
            ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        bgcolor=None,
                        header=ft.ListTile(
                            leading=ft.Icon(ft.icons.LIST),
                            title=ft.Text("読み込んだファイル一覧"),
                        ),
                        content=ft.Column(
                            controls=[
                                ft.ListTile(
                                    title=ft.Text(file_name[i]) if i < len(file_name) else ft.Text("Unknown")
                                )
                                for i in range(len(file_name))
                            ]
                        )
                    )
                ]
            ),
            ]
        card.controls=card_list
        card.update()
        
    @staticmethod
    def show_progress_bar(chart_field, page):
        chart_field.controls=[
            ft.Card(
                content=ft.Column(
                    [
                        ft.Text("Loading..."),
                        ft.ProgressBar(width=200, height=20),
                    ],
                ),
            )
        ]
        page.update()

    @staticmethod
    def ComponentChart_for_standard(dataframe, chart_field, page,parent_instance_standard):
        #表示期間の選択があれば、そこから日付を抽出して選択された期間にてdatagrameをフィルタリングする   
        try:
            start_date=datetime.datetime.strptime(chart_field.controls[1].controls[0].data,"%Y-%m-%dT%H:%M:%S.%f")
            end_date=datetime.datetime.strptime(chart_field.controls[1].controls[2].data,"%Y-%m-%dT%H:%M:%S.%f")
            chart_field.controls[1].controls[0].text=start_date.strftime("%Y-%m-%d")
            chart_field.controls[1].controls[2].text=end_date.strftime("%Y-%m-%d")
            Handlers_Chart.show_progress_bar(chart_field, page)
            df =dataframe
            df["date"]=pd.to_datetime(df["date"],format="%Y-%m-%d")
            
            #日付のフィルタリング start_dateからend_dateまでのデータを抽出
            df=df[df["date"].between(start_date,end_date)]
            #日付でフィルタリングしたデータを返す
            parent_instance_standard.all_df=df
            
            # bar_plot
            group_bubble = df.groupby(["locate","task","count"]).size().reset_index(name="times")
            #Countsが0の場合とそれ以外に分かれるので、それぞれを合計する
            group_bubble2 = group_bubble.groupby(["locate","task"]).sum(numeric_only=True).reset_index()
            #times*15 = かかった時間となるので計算しなおす
            group_bubble2["times"] = group_bubble2["times"]*15
            chart_width=int(len(group_bubble2["task"].unique()))*33
            if chart_width<1000:
                chart_width=1000
            bar_chart=px.bar(group_bubble2,x="task",y="times",width=chart_width)
            """
            fig_bubble = px.scatter(group_bubble2,x = "times",y = "count",color = "task",text = "task" ,
                            )
            fig_bubble.update_layout(yaxis =dict(title = "件数"),
                                    xaxis = dict(title = "かかった時間")
                                    )
            fig_bubble.update_traces(textposition='top center')
            """
            bar_chart.update_layout(yaxis =dict(title = "かかった時間"),
                                    xaxis = dict(title = "業務内容")
                                    )
            
            chart_field.controls = [
                #表示期間
                ft.ListTile(
                    title=ft.Text("表示期間"),
                    leading=ft.Icon(ft.icons.DATE_RANGE),
                    subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
                    ),
                ft.Row(
                        controls=[
                            ft.FilledButton(
                                text=start_date.strftime("%Y-%m-%d"),
                                on_click=lambda e:page.open(
                                    ft.DatePicker(
                                        on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event,),
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.TRANSPARENT,
                                    color=ft.colors.BLUE_900,
                                ),
                                data={}
                            ),
                            ft.Text("~",size=20),
                            ft.FilledButton(
                                text=end_date.strftime("%Y-%m-%d"),
                                on_click=lambda e:page.open(
                                    ft.DatePicker(
                                        on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event,),
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.TRANSPARENT,
                                    color=ft.colors.BLUE_900,
                                ),  
                                data={}
                            )

                        ],
                        spacing=0,
                    ),
                #グラフ
                (ft.Card(content = PlotlyChart(bar_chart,expand = True,original_size = False,isolated = True))),
                #ダウンロード
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    on_click=lambda _:Chart_Download_Handler.open_directory(page=page,barchart=bar_chart,chart_name="barchart"),
                    tooltip=ft.Tooltip("グラフを保存")
                    ),
                
                ]
            chart_field.update()


        except Exception as e:
            print(e)
            Handlers_Chart.show_progress_bar(chart_field, page)
            df =dataframe
            
            # bar_plot
            group_bubble = df.groupby(["locate","task","count"]).size().reset_index(name="times")
            #Countsが0の場合とそれ以外に分かれるので、それぞれを合計する
            group_bubble2 = group_bubble.groupby(["locate","task"]).sum(numeric_only=True).reset_index()
            #times*15 = かかった時間となるので計算しなおす
            group_bubble2["times"] = group_bubble2["times"]*15
            chart_width=int(len(group_bubble2["task"].unique()))*33
            if chart_width<1000:
                chart_width=1000
            bar_chart=px.bar(group_bubble2,x="task",y="times",width=chart_width)
            """
            fig_bubble = px.scatter(group_bubble2,x = "times",y = "count",color = "task",text = "task" ,
                            )
            fig_bubble.update_layout(yaxis =dict(title = "件数"),
                                    xaxis = dict(title = "かかった時間")
                                    )
            fig_bubble.update_traces(textposition='top center')
            """
            bar_chart.update_layout(yaxis =dict(title = "かかった時間"),
                                    xaxis = dict(title = "業務内容"),
                                    )
            
            chart_field.controls = [
                #表示期間
                ft.ListTile(
                    title=ft.Text("表示期間"),
                    leading=ft.Icon(ft.icons.DATE_RANGE),
                    subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
                    ),
                ft.Row(
                        controls=[
                            ft.FilledButton(
                                text="開始日",
                                on_click=lambda e:page.open(
                                    ft.DatePicker(
                                        on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.TRANSPARENT,
                                    color=ft.colors.BLUE_900,
                                ),
                                data={}
                            ),
                            ft.Text("~",size=20),
                            ft.FilledButton(
                                text="終了日",
                                on_click=lambda e:page.open(
                                    ft.DatePicker(
                                        on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                    )
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.TRANSPARENT,
                                    color=ft.colors.BLUE_900,
                                ),  
                                data={}
                            )

                        ],
                        spacing=0,
                    ),
                    #表示期間の表示
                ft.ListTile(),
                #グラフ
                (ft.Card(content = PlotlyChart(bar_chart,expand = True,original_size = False,isolated = True))),
                #ダウンロード
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    on_click=lambda _:Chart_Download_Handler.open_directory(page=page,barchart=bar_chart,chart_name="barchart"),
                    tooltip=ft.Tooltip("グラフを保存")
                    )
                ]
            page.update()
        

        
    @staticmethod
    def ComponentChart_for_location(dataframe, chart_field, page,chart2_info,parent_instance_locate):
        
        Handlers_Chart.show_progress_bar(chart_field, page)
        # データフレームを渡してグラフを生成する
        # まずグラフを描画するcardを病棟数分作成
        # 取得したデータフレームから病棟の数,名前を取得
        # locateは複数選択にてリスト形式になっているからバラす必要がある
        try:
            start_date=datetime.datetime.strptime(chart2_info.controls[1].controls[0].data,"%Y-%m-%dT%H:%M:%S.%f")
            end_date=datetime.datetime.strptime(chart2_info.controls[1].controls[2].data,"%Y-%m-%dT%H:%M:%S.%f")
            chart2_info.controls[1].controls[0].text=start_date.strftime("%Y-%m-%d")
            chart2_info.controls[1].controls[2].text=end_date.strftime("%Y-%m-%d")
            df =dataframe
            #日付のフィルタリングしたデータを返す
            parent_instance_locate.locate_df=df

            df["date"]=pd.to_datetime(df["date"],format="%Y-%m-%d")
            #日付のフィルタリング start_dateからend_dateまでのデータを抽出
            df=df[df["date"].between(start_date,end_date)]
            #算出したデータフレームから病棟数を算出し、病棟数分のcardを作成する
            # data =病棟名　でもつけて紐づけるできるように
            group_df_locate = (
                df.groupby(["locate", "task"]).size().reset_index(name="counts")
            )
            chart2_info.controls=[
                ft.ListTile(
                    title=ft.Text("表示期間"),
                    leading=ft.Icon(ft.icons.DATE_RANGE),
                    subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
                    ),
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            text=start_date.strftime("%Y-%m-%d"),
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),
                            data={}
                        ),
                        ft.Text("~",size=20),
                        ft.FilledButton(
                            text=end_date.strftime("%Y-%m-%d"),
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),  
                            data={}
                        )
                    ]
                )
            ]
            locate_chart_list=[]
            for locate in group_df_locate["locate"].unique():
                fig = px.pie(
                    group_df_locate[group_df_locate["locate"] == locate],
                    values="counts",
                    names="task",
                    title=locate,
                )

                locate_chart_list.extend(
                    [ft.Card(
                        content=ft.Column(
                            controls=[
                                PlotlyChart(
                                    fig, expand=True, original_size=False, isolated=True
                                ),
                                ft.Text(locate),
                                ft.ElevatedButton(
                                "保存",
                                icon=ft.icons.DOWNLOAD,
                                tooltip=ft.Tooltip("グラフを保存"),
                                on_click=lambda _: Chart_Download_Handler.open_directory(
                                    page=page, barchart=fig,
                                    chart_name="piechart"
                                    )
                                )
                            ],
                            width="30%",
                        ),
                        data=locate,
                        col={"sm": 10, "md": 6, "xl": 4},
                    ),
                    ]
                )
            chart_field.controls=locate_chart_list
            page.update()
        except Exception as e:
            print(f"An error occurred: {e}")

            df =dataframe

            # 算出したデータフレームから病棟数を算出し、病棟数分のcardを作成する
            # data =病棟名　でもつけて紐づけるできるように？
            group_df_locate = (
                df.groupby(["locate", "task"]).size().reset_index(name="counts")
            )
            chart2_info.controls=[
                ft.ListTile(
                    title=ft.Text("表示期間"),
                    leading=ft.Icon(ft.icons.DATE_RANGE),
                    subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
                    ),
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            text="開始日",
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),
                            data={}
                        ),
                        ft.Text("~",size=20),
                        ft.FilledButton(
                            text="終了日",
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),  
                            data={}
                        )
                    ]
                )
            ]
            locate_chart_list=[]
            for locate in group_df_locate["locate"].unique():
                fig = px.pie(
                    group_df_locate[group_df_locate["locate"] == locate],
                    values="counts",
                    names="task",
                    title=locate,
                )
                locate_chart_list.append(
                    ft.Card(
                        content=ft.Column(
                            controls=[
                                PlotlyChart(
                                    fig, expand=True, original_size=False, isolated=True
                                ),
                                ft.Text(locate),
                                ft.ElevatedButton(
                                "保存",
                                icon=ft.icons.DOWNLOAD,
                                tooltip=ft.Tooltip("グラフを保存"),
                                on_click=lambda _, chart=fig, locate_name=locate: Chart_Download_Handler.open_directory(
                                    page=page, barchart=chart,
                                    chart_name=f"piechart_{locate_name}"
                                    ),
                                )
                            ],
                            width="30%",
                        ),
                        data=locate,
                        col={"sm": 10, "md": 6, "xl": 4},
                    )
                )
            chart_field.controls=locate_chart_list
            page.update()   
        # その上にplotlyにて円グラフを作成する

    @staticmethod
    def ComponentChart_for_self(dataframe,chart_field,page,parent_instance_self_df):        
        try:
            start_date=datetime.datetime.strptime(chart_field.controls[1].controls[0].data,"%Y-%m-%dT%H:%M:%S.%f")
            end_date=datetime.datetime.strptime(chart_field.controls[1].controls[2].data,"%Y-%m-%dT%H:%M:%S.%f")
            chart_field.controls[1].controls[0].text=start_date.strftime("%Y-%m-%d")
            chart_field.controls[1].controls[2].text=end_date.strftime("%Y-%m-%d")
            Handlers_Chart.show_progress_bar(chart_field, page)
            df =dataframe

            df["date"]=pd.to_datetime(df["date"],format="%Y-%m-%d")
            #日付のフィルタリング start_dateからend_dateまでのデータを抽出
            df=df[df["date"].between(start_date,end_date)]
            #日付でフィルタリングしたデータを返す
            parent_instance_self_df.self_df=df

            group_by_person = df.groupby(["phName","task"]).size().reset_index(name="time")            #phNamaeごとの合計値を計算
            group_by_person["total_time"]=group_by_person.groupby("phName")["time"].transform("sum")
            group_by_person["percentage"]=(group_by_person["time"]/group_by_person["total_time"])*100
            graph_height=int(len(group_by_person["phName"].unique()))*33
            if graph_height<1000:
                graph_height=1000
            fig_bar = px.bar(group_by_person, height=graph_height,x="percentage", y="phName", color="task", barmode="stack", orientation="h")
            # まずグラフを描画するcardを作成
            chart_field.controls = [
                ft.ListTile(
                    title=ft.Text("表示期間"),
                    leading=ft.Icon(ft.icons.DATE_RANGE),
                    subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
                    ),
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            text=start_date.strftime("%Y-%m-%d"),
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),
                            data={}
                        ),
                        ft.Text("~",size=20),
                        ft.FilledButton(
                            text=end_date.strftime("%Y-%m-%d"),
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),  
                            data={}
                        )
                    ]
                ),
                #グラフ
                ft.Card(content = PlotlyChart(fig_bar,expand = True,original_size = False,isolated = True)),
                #ダウンロード
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip=ft.Tooltip("グラフを保存"),
                    on_click=lambda _: Chart_Download_Handler.open_directory(page=page,barchart=fig_bar,chart_name="selfchart"),
                )
            ]
            page.update()   

        except IndexError as e:
            print(e)
            Handlers_Chart.show_progress_bar(chart_field, page)
            #データフレームの作成
            df = dataframe
            
            # 個人ごとにデータをまとめ直す
            group_by_person = df.groupby(["phName","task"]).size().reset_index(name="time")
            #phNamaeごとの合計値を計算
            group_by_person["total_time"]=group_by_person.groupby("phName")["time"].transform("sum")
            graph_height=int(len(group_by_person["phName"].unique()))*33
            if graph_height<1000:
                graph_height=1000
            #各taskの割割合を計算
            group_by_person["percentage"]=(group_by_person["time"]/group_by_person["total_time"])*100
            # その上にplotlyにて棒グラフを作成する
            fig_bar = px.bar(group_by_person, x="percentage", y="phName", color="task", barmode="stack", orientation="h")
            fig_bar.update_layout(
                height=graph_height,
                xaxis=dict(title="業務"),
                yaxis=dict(title="薬剤師名"),
                legend=dict(
                    font=dict(size=10),
                )
            )
            # まずグラフを描画するcardを作成
            chart_field.controls = [
                ft.ListTile(
                    title=ft.Text("表示期間"),
                    leading=ft.Icon(ft.icons.DATE_RANGE),
                    subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
                    ),
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            text="開始日",
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),
                            data={}
                        ),
                        ft.Text("~",size=20),
                        ft.FilledButton(
                            text="終了日",
                            on_click=lambda e:page.open(
                                ft.DatePicker(
                                    on_change=lambda dp_event:PeriodHandler.select_period(e,dp_event),
                                )
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.TRANSPARENT,
                                color=ft.colors.BLUE_900,
                            ),  
                            data={}
                        )
                    ]
                ),
                #グラフ
                ft.Card(content = 
                    PlotlyChart(fig_bar,expand = True,original_size = False,isolated = True)
                ),
                #ダウンロード
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip=ft.Tooltip("グラフを保存"),
                    on_click=lambda _: Chart_Download_Handler.open_directory(page=page, barchart=fig_bar,chart_name="selfchart"),
                )
            ]
            page.update()
    """
    @staticmethod
    def create_dataframe(dataframe):
        new_rows = []
        for index, row in dataframe.iterrows():
            tarn_row = ast.literal_eval(row["locate"])
            for loc in range(len(tarn_row)):
                new_row = row.copy()
                new_row["locate"] = tarn_row[loc]
                new_rows.append(new_row)
        return pd.DataFrame(new_rows)"""