import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart,TASK_COLOR_MAP
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import pandas as pd
from handlers.chart.download_handler import Chart_Download_Handler
from handlers.chart.download_dataframe import DataframeDownloadHandler
class Handlers_analyze:
    #各タスクがどの時間帯に集中しているかを分析。　ヒートマップ
    @staticmethod
    def time_task_analysis(dataframe, result_field, page,all_df):  
        Handlers_Chart.show_progress_bar(result_field, page)

        def _extract_time_task(df):
            df = df[["task","time"]]
            df = df.groupby(["task","time"]).size().reset_index(name="counts")
            #時間順にデータを並び替える
            df["sort_time"]=df["time"].astype(str).fillna("")
            df["sort_time"]=df["sort_time"].str.strip().str.split(" ").str[0]
            #sort_time列のデータ型をdatetimeに変換
            df["sort_time"]=pd.to_datetime(df["sort_time"],format="%H:%M",errors="coerce")
            #sort_time列を元に時間順にソート    
            df.sort_values("sort_time",inplace=True)
            return df
        
        df = _extract_time_task(all_df if all_df is not None else dataframe)
        heat_height = int(len(df["task"].unique())) * 33
        heat_width = int(len(df["time"].unique())) * 33
        if heat_width < 1000:
            heat_width = 1000

        fig=px.density_heatmap(
            df,
            x="time",
            y="task",
            z="counts",
            title="時間ごとに業務が記録された回数",
            labels={"time": "Time", "task": "Task", "counts": "Task Count"},
            height=heat_height,
            width=heat_width,
        )
        fig.update_layout(
            xaxis=dict(title="時間"),
            yaxis=dict(title="業務内容"),
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
            Handlers_Chart._create_preview_button(chart=fig,page=page), # グラフのプレビュー用ボタン
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="グラフを保存",
                on_click=lambda _:Chart_Download_Handler.open_directory(page=page,barchart=fig,chart_name="heatmap"),

            ),
            #データフレーム
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("業務内容")),
                    ft.DataColumn(ft.Text("時間")),
                    ft.DataColumn(ft.Text("時間に記録された回数")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row.task)),
                            ft.DataCell(ft.Text(row.time)),
                            ft.DataCell(ft.Text(str(row.counts)))
                        ]
                    )
                    for row in df.itertuples(index=False, name="Row")
                ]
            )
        ]
        result_field.update()
    #業務内容ごとの件数
    @staticmethod
    def task_par_count(dataframe, result_field, page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        def _extract_task_count(df):
            df = df[["task","count"]]
            df = df.groupby(["task"])["count"].sum().reset_index(name="counts")
            try:
                df.drop(index=["無菌調製関連業務"],inplace=True)
                df.drop(index=["混注時間"],inplace=True)
                df.drop(index=["休憩"],inplace=True)
                df.drop(index=["委員会"],inplace=True)
                df.drop(index=["WG活動"],inplace=True)
                df.drop(index=["勉強会参加"],inplace=True)
                df.drop(index=["1on1"],inplace=True)
                df.drop(index=["カンファレンス"],inplace=True)
            except KeyError:
                pass
            return df
        
        task_count = _extract_task_count(all_df if all_df is not None else dataframe)
            
        result_field.controls=[
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("業務内容")),
                    ft.DataColumn(ft.Text("件数")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row.task)),
                            ft.DataCell(ft.Text(str(row.counts))),
                        ]
                    )
                    for row in task_count.itertuples(index=False, name="Row")
                ]
            ),
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="データフレームを保存",
                on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=task_count,name="task_count"),
            )
        ]
        result_field.update()

    #件数あたりの時間 件数あたりに要した時間の算出
    @staticmethod
    def count_par_time(dataframe, result_field, page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        def _compute_time_per_count(df):
            df = df[["task","count"]]
            time_per_task = df.groupby(["task"]).size().reset_index(name="times")
            time_per_task["times"] = time_per_task["times"] *15

            count_per_task = df.groupby(["task"])["count"].sum().reset_index(name="counts")
            df = pd.merge(time_per_task,count_per_task,on="task")

            avg_row = df.mean(numeric_only=True)
            avg_row["task"] = "平均"
            df = pd.concat([df,pd.DataFrame([avg_row])],ignore_index=True)
            df["time_per_task"] = df["times"] / df["counts"]
            return df
        
        df =_compute_time_per_count(all_df if all_df is not None else dataframe)

        result_field.controls = [
            ft.Text("1件あたりに要した時間の算出", size=20),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("業務内容")),
                    ft.DataColumn(ft.Text("件数")),
                    ft.DataColumn(ft.Text("総時間")),
                    ft.DataColumn(ft.Text("件数あたりの時間")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row.task)),
                        ft.DataCell(ft.Text(str(row.counts))),
                        ft.DataCell(ft.Text(str(row.times))),
                        ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                    ])
                    for row in df.itertuples(index=False, name="Row")
                ]
            ),
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="データフレームを保存",
                on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=time_per_task,name="time_per_task"),
            )
        ]
        page.update()

    #各タスクがどの場所（locate列）で行われたかを集計。
    @staticmethod
    def task_par_location(dataframe, result_field, page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)

        def _extract_location(df):
            df = df[["locate","task"]]
            df = df.groupby(["locate","task"]).size().reset_index(name="counts")
            try:
                df.drop(index =df[df["locate"]=="self"].index,inplace=True) #self列は除外する)
            except KeyError:
                pass
            return df
        
        df = _extract_location(all_df if all_df is not None else dataframe)

        graph_width=int(len(df["locate"].unique()))*77
        if graph_width<1000:
            graph_width=1000
            
        fig=px.bar(
            df,
            x="locate",
            y="counts",
            color="task",
            title="場所ごとに記録された業務内容と記録回数",
            labels={"locate": "Location", "counts": "Task Count", "task": "Task"},
            barmode="stack",
            width=graph_width,
            height=1400,
            hover_data={"locate":True,"task":True,"counts":True}
        )
        fig.update_layout(
            xaxis=dict(title="病棟"),
            yaxis=dict(title="記録回数")
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
            Handlers_Chart._create_preview_button(chart=fig,page=page), # グラフのプレビュー用ボタン
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="グラフを保存",
                on_click=lambda _:Chart_Download_Handler.open_directory(page=page,barchart=fig,chart_name="task_location"),
            )
        ]
        result_field.update()

    #date列を基に、日付ごとのタスクの分布を分析
    @staticmethod
    def date_task_analysis(dataframe,result_field,page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)

        def _extract_date(df):
            date_df = df[df["date"].notna()]
            date_df = date_df[["date","task"]]
            date_df = pd.to_datetime(date_df["date"],errors="coerce")
            date_df = date_df.groupby([date_df,df["task"]]).size().reset_index(name="counts")
            return date_df
        
        df = _extract_date(all_df if all_df is not None else dataframe)
        graph_width = int(len(df[0].unique())) * 33
        if graph_width < 1000:
            graph_width = 1000

        fig=px.bar(
            df,
            x="date",
            y="counts",
            color="task",
            title="日付ごとに記録された業務内容と記録回数",
            labels={"date": "Date", "counts": "Task Count", "task": "Task"},
            barmode="stack",
            width=graph_width,
            height=1400,
        )
        fig.update_layout(
            xaxis=dict(title="日付"),
            yaxis=dict(title="記録回数")
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
            Handlers_Chart._create_preview_button(chart=fig,page=page), # グラフのプレビュー用ボタン
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="グラフを保存",
                on_click=lambda _:Chart_Download_Handler.open_directory(page=page,barchart=fig,chart_name="task_date"),
            ),
            #データフレーム
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("日付")),
                    ft.DataColumn(ft.Text("業務内容")),
                    ft.DataColumn(ft.Text("記録回数")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row.date.strftime("%Y-%m-%d"))),
                            ft.DataCell(ft.Text(row.task)),
                            ft.DataCell(ft.Text(str(row.counts)))
                        ]
                    )
                    for row in date_group_df.itertuples(index=False, name="Row")
                ]
            ),
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="データフレームを保存",
                on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=date_group_df,name="task_date"),
            )
        ]
        result_field.update()

    @staticmethod
    def comment_analysis(dataframe,result_field,page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        def _extract_comments(df):
            comment_df=df[df["comment"].notna()]
            comment_df=comment_df[["time","locate","date","phName","comment"]]
            comment_df=comment_df.reset_index(drop=True)
            return comment_df
        
        df = _extract_comments(all_df if all_df is not None else dataframe)

        result_field.controls=[
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("日付")),
                    ft.DataColumn(ft.Text("時間")),
                    ft.DataColumn(ft.Text("場所")),
                    ft.DataColumn(ft.Text("記録者")),
                    ft.DataColumn(ft.Text("コメント")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row.date)),
                            ft.DataCell(ft.Text(row.time)),
                            ft.DataCell(ft.Text(row.locate)),
                            ft.DataCell(ft.Text(row.phName)),
                            ft.DataCell(ft.Text(row.comment))
                        ]
                    )
                    for row in df.itertuples(index=False, name="Row")
                ]
            ),
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="データフレームを保存",
                on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=comment_df,name="comment"),
            )
        ]
        result_field.update()
    
    
    @staticmethod
    def self_analysis(dataframe,result_field,page,self_df):
        Handlers_Chart.show_progress_bar(result_field, page)

        def _calculate_for_phName(dataframe):
            df = dataframe[["phName","task","count"]]
            times=df.groupby(["phName","task"]).size().reset_index(name="task_total")
            countdf = df.groupby(["phName","task"])["count"].sum().reset_index(name="counts_total")
            df = pd.merge(times,countdf,on=["phName","task"])
            #*15にすることで実際の時間に変換　(1入力15ふん）
            df["times"] = df["task_total"] * 15
            #１業務あたりの時間列を追加
            df["time_per_task"]=df["times"]/df["task_total"]
            #1件あたりの時間列を追加
            df["time_per_count"]=df["times"]/df["counts_total"]
            return df
        
        df = _calculate_for_phName(self_df if self_df is not None else dataframe)
        result_field.controls=[
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("薬剤師名")),
                    ft.DataColumn(ft.Text("業務内容")),
                    ft.DataColumn(ft.Text("件数")),
                    ft.DataColumn(ft.Text("時間")),
                    ft.DataColumn(ft.Text("件数あたりの時間")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(row.phName)),
                            ft.DataCell(ft.Text(row.task)),
                            ft.DataCell(ft.Text(str(row.counts_total))),
                            ft.DataCell(ft.Text(str(row.times))),
                            ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                        ]
                    )
                    for row in df.itertuples(index=False, name="Row")
                ]
            ),
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="データフレームを保存",
                on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=df,name="self_analysis"),
            )
        ]
        result_field.update()
            
    @staticmethod   
    def calculate_for_phName(dataframe):
        df = dataframe[["phName","task","count"]]
        task_count=df.groupby("phName").size().reset_index(name="task_count")
        countdf = df.groupby("phName")["count"].sum().reset_index(name="count_total")
        df = pd.merge(task_count,countdf,on="phName")
        #*15にすることで実際の時間に変換　(1入力15ふん）
        df["times"] = df["task_count"] * 15
        #１業務あたりの時間列を追加
        df["time_per_task"]=df["times"]/df["task_count"]
        #1件あたりの時間列を追加
        df["time_per_count"]=df["times"]/df["count_total"]
        print(df)
        #一番下に平均値を追加
        avg_row=df.mean(numeric_only=True)
        avg_row["phName"]="平均"
        df=pd.concat([df,pd.DataFrame([avg_row])],ignore_index=True)
        return df

    @staticmethod
    def self_analysis_total_time(dataframe,result_field,page,self_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        if self_df is not None:
            df = Handlers_analyze.calculate_for_phName(self_df)    
            result_field.controls=[
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("薬剤師名")),
                        ft.DataColumn(ft.Text("総時間")),
                        ft.DataColumn(ft.Text("業務数")),
                        ft.DataColumn(ft.Text("件数")),
                        ft.DataColumn(ft.Text("1業務あたりの時間")),
                        ft.DataColumn(ft.Text("1件あたりの時間")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(row.phName)),
                                ft.DataCell(ft.Text(str(row.times))),
                                ft.DataCell(ft.Text(str(row.task_count))),
                                ft.DataCell(ft.Text(str(row.count_total))),
                                ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                                ft.DataCell(ft.Text(f"{row.time_per_count:.2f}")),
                            ]
                        )
                        for row in df.itertuples(index=False, name="Row")
                    ]
                ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=time_for_phname_total,name="self_analysis_total_time"),
                )
            ]
            result_field.update()

        else:
            df = Handlers_analyze.calculate_for_phName(dataframe)

            result_field.controls=[
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("薬剤師名")),
                        ft.DataColumn(ft.Text("総時間")),
                        ft.DataColumn(ft.Text("業務数")),
                        ft.DataColumn(ft.Text("件数")),
                        ft.DataColumn(ft.Text("1業務あたりの時間")),
                        ft.DataColumn(ft.Text("1件あたりの時間")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(row.phName)),
                                ft.DataCell(ft.Text(str(row.times))),
                                ft.DataCell(ft.Text(str(row.task_count))),
                                ft.DataCell(ft.Text(str(row.count_total))),
                                ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                                ft.DataCell(ft.Text(f"{row.time_per_count:.2f}")),
                            ]
                        )
                        for row in df.itertuples(index=False, name="Row")
                    ]
                ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=time_for_phname_total,name="self_analysis_total_time"),
                )
            ]
            result_field.update()

    #病棟ごとの時間数・件数・１件あたりの時間・平均値
    @staticmethod
    def locate_analysis(dataframe,result_field,page,locate_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        if locate_df is not None:
            df=locate_df
            timedf=df.groupby(["locate","task"]).size().reset_index(name="times")
            try:
                timedf.drop(index=timedf[timedf["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            #*15にすることで実際の時間に変換　(1入力15ふん）
            timedf["times"]=timedf["times"]*15
            #業務数列
            taskdf=dataframe.groupby(["locate","task"]).size().reset_index(name="task_count")
            try:
                taskdf.drop(index=taskdf[taskdf["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            #カウント数列を算出
            countdf=dataframe.groupby(["locate","task"])["count"].sum().reset_index(name="count_total")
            try:
                countdf.drop(index=countdf[countdf["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            loc_df=pd.merge(
                timedf,
                taskdf,
                on=["locate","task"],
                how="left"
            )
            loc_df=pd.merge(
                loc_df,
                countdf,
                on=["locate","task"],
                how="left"
            )
            #集計
            total_df=loc_df.groupby("locate")["times"].sum().reset_index(name="total_times")
            #locateごとの総業務数
            total_df["task_count"]=loc_df.groupby("locate")["task_count"].transform("sum")
            #locateごとの総件数
            total_df["count_total"]=loc_df.groupby("locate")["count_total"].transform("sum")
            #１業務あたりの時間列を追加
            total_df["time_per_task"]=total_df["total_times"]/total_df["task_count"]
            #1件あたりの時間列を追加
            total_df["time_per_count"]=total_df["total_times"]/total_df["count_total"]
            #一番下に平均値を追加
            avg_row=total_df.mean(numeric_only=True)
            avg_row["locate"]="平均"
            total_df=pd.concat([total_df,pd.DataFrame([avg_row])],ignore_index=True)    

            result_field.controls=[
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("病棟名")),
                        ft.DataColumn(ft.Text("総時間")),
                        ft.DataColumn(ft.Text("業務数")),
                        ft.DataColumn(ft.Text("件数")),
                        ft.DataColumn(ft.Text("1業務あたりの時間")),
                        ft.DataColumn(ft.Text("1件あたりの時間")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(row.locate)),
                                ft.DataCell(ft.Text(str(row.total_times))),
                                ft.DataCell(ft.Text(str(row.task_count))),
                                ft.DataCell(ft.Text(str(row.count_total))),
                                ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                                ft.DataCell(ft.Text(f"{row.time_per_count:.2f}")),
                            ]
                        )
                        for row in total_df.itertuples(index=False, name="Row")
                    
                            ]
                        ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=total_df,name="locate_analysis")
                                                                                            
                )
                    ]
            result_field.update()
        else:
            timedf=dataframe.groupby(["locate","task"]).size().reset_index(name="times")
            try:
                timedf.drop(index=timedf[timedf["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            #*15にすることで実際の時間に変換　(1入力15ふん）
            timedf["times"]=timedf["times"]*15
            #業務数列
            taskdf=dataframe.groupby(["locate","task"]).size().reset_index(name="task_count")
            try:
                taskdf.drop(index=taskdf[taskdf["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            #カウント数列を算出
            countdf=dataframe.groupby(["locate","task"])["count"].sum().reset_index(name="count_total")
            try:
                countdf.drop(index=countdf[countdf["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            loc_df=pd.merge(
                timedf,
                taskdf,
                on=["locate","task"],
                how="left"
            )
            loc_df=pd.merge(
                loc_df,
                countdf,
                on=["locate","task"],
                how="left"
            )
            #集計
            total_df=loc_df.groupby("locate")["times"].sum().reset_index(name="total_times")
            #locateごとの総業務数
            total_df["task_count"]=loc_df.groupby("locate")["task_count"].transform("sum")
            #locateごとの総件数
            total_df["count_total"]=loc_df.groupby("locate")["count_total"].transform("sum")
            #１業務あたりの時間列を追加
            total_df["time_per_task"]=total_df["total_times"]/total_df["task_count"]
            #1件あたりの時間列を追加
            total_df["time_per_count"]=total_df["total_times"]/total_df["count_total"]
            #一番下に平均値を追加
            avg_row=total_df.mean(numeric_only=True)
            avg_row["locate"]="平均"
            total_df=pd.concat([total_df,pd.DataFrame([avg_row])],ignore_index=True)    

            result_field.controls=[
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("病棟名")),
                        ft.DataColumn(ft.Text("総時間")),
                        ft.DataColumn(ft.Text("業務数")),
                        ft.DataColumn(ft.Text("件数")),
                        ft.DataColumn(ft.Text("1業務あたりの時間")),
                        ft.DataColumn(ft.Text("1件あたりの時間")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(row.locate)),
                                ft.DataCell(ft.Text(str(row.total_times))),
                                ft.DataCell(ft.Text(str(row.task_count))),
                                ft.DataCell(ft.Text(str(row.count_total))),
                                ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                                ft.DataCell(ft.Text(f"{row.time_per_count:.2f}")),
                            ]
                        )
                        for row in total_df.itertuples(index=False, name="Row")
                    
                            ]
                        ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=total_df,name="locate_analysis")
                                                                                            
                )
                    ]
            result_field.update()