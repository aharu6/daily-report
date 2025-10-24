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
        if all_df is not None:
            df=all_df
            task_per_time_heatmap=df.groupby(["task","time"]).size().reset_index(name="counts")
            heat_height=int(len(task_per_time_heatmap["task"].unique()))*33
            heat_width=int(len(task_per_time_heatmap["time"].unique()))*33
            if heat_width<1000:
                heat_width=1000
            #時間順にデータを並び替える
            task_per_time_heatmap["sort_time"]=task_per_time_heatmap["time"].astype(str).fillna("")
            task_per_time_heatmap["sort_time"]=task_per_time_heatmap["sort_time"].str.strip().str.split(" ").str[0]
            #sort_time列のデータ型をdatetimeに変換
            task_per_time_heatmap["sort_time"]=pd.to_datetime(task_per_time_heatmap["sort_time"],format="%H:%M",errors="coerce")
            #sort_time列を元に時間順にソート    
            task_per_time_heatmap.sort_values("sort_time",inplace=True)
            
            fig=px.density_heatmap(
                task_per_time_heatmap,
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
                        for row in task_per_time_heatmap.itertuples(index=False, name="Row")
                    ]
                )
            ]
            result_field.update()
        else:

            df=dataframe
            task_per_time_heatmap=df.groupby(["task","time"]).size().reset_index(name="counts")
            
            heat_height=int(len(task_per_time_heatmap["task"].unique()))*33
            heat_width=int(len(task_per_time_heatmap["time"].unique()))*33
            if heat_width<1000:
                heat_width=1000
            #時間順にデータを並び替える
            task_per_time_heatmap["sort_time"]=task_per_time_heatmap["time"].astype(str).fillna("")
            task_per_time_heatmap["sort_time"]=task_per_time_heatmap["sort_time"].str.strip().str.split(" ").str[0]
            #sort_time列のデータ型をdatetimeに変換
            task_per_time_heatmap["sort_time"]=pd.to_datetime(task_per_time_heatmap["sort_time"],format="%H:%M",errors="coerce")
            #sort_time列を元に時間順にソート    
            task_per_time_heatmap.sort_values("sort_time",inplace=True)
            
            fig=px.density_heatmap(
                task_per_time_heatmap,
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
                        for row in task_per_time_heatmap.itertuples(index=False, name="Row")
                    ]
                ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=task_per_time_heatmap,name="time_task_analysis"),
                )
            ]
            result_field.update()


    #業務内容ごとの件数
    @staticmethod
    def task_par_count(dataframe, result_field, page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        if all_df is not None:
            df=all_df
            task_count=df.groupby(["task"])["count"].sum().reset_index(name="counts")
            #件数を集計していない項目はデータフレームより除外する
            try:
                task_count.drop(index=["無菌調製関連業務"],inplace=True)
                task_count.drop(index=["混注時間"],inplace=True)
                task_count.drop(index=["休憩"],inplace=True)
                task_count.drop(index=["委員会"],inplace=True)
                task_count.drop(index=["WG活動"],inplace=True)
                task_count.drop(index=["勉強会参加"],inplace=True)
                task_count.drop(index=["1on1"],inplace=True)
                task_count.drop(index=["カンファレンス"],inplace=True)
            except KeyError:
                pass
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
        else:
            task_count=dataframe.groupby(["task"])["count"].sum().reset_index(name="counts")
            #件数を集計していない項目はデータフレームより除外する
            try:
                task_count.drop(index=["無菌調製関連業務"],inplace=True)
                task_count.drop(index=["混注時間"],inplace=True)
                task_count.drop(index=["休憩"],inplace=True)
                task_count.drop(index=["委員会"],inplace=True)
                task_count.drop(index=["WG活動"],inplace=True)
                task_count.drop(index=["勉強会参加"],inplace=True)
                task_count.drop(index=["1on1"],inplace=True)
                task_count.drop(index=["カンファレンス"],inplace=True)
            except KeyError:
                pass
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
        """_summary_

        Args:
            dataframe (_type_): _description_
            result_field (_type_): グラフかデータフレームを表示する=ft.ResponsiveRow(controls=)
            page (_type_): _description_
        """
        Handlers_Chart.show_progress_bar(result_field, page)
        if all_df is not None:
            df=all_df
            time_per_task=df.groupby(["task"]).size().reset_index(name="times")
            #times列に*15することで、実際の時間に変換（１入力あたり１５分のため）
            time_per_task["times"]=time_per_task["times"]*15
            #count列を合計しておく
            count_per_task=df.groupby(["task"])["count"].sum().reset_index(name="counts")
            time_per_task["counts"]=count_per_task["counts"]

            #平均値列を追加
            avg_row = time_per_task.mean(numeric_only=True)
            avg_row["task"] = "平均"
            time_per_task = pd.concat([time_per_task, pd.DataFrame([avg_row])], ignore_index=True)

            # 新しいtime/taskにて1件あたりに要した時間を計算
            time_per_task["time_per_task"] = time_per_task["times"] / time_per_task["counts"]

            # データフレームとして表示する
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
                        for row in time_per_task.itertuples(index=False, name="Row")
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
        else:
            df=dataframe
            time_per_task=df.groupby(["task"]).size().reset_index(name="times")
            #times列に*15することで、実際の時間に変換（１入力あたり１５分のため）
            time_per_task["times"]=time_per_task["times"]*15
            #count列を合計しておく
            count_per_task=df.groupby(["task"])["count"].sum().reset_index(name="counts")
            time_per_task["counts"]=count_per_task["counts"]

            #平均値列を追加
            avg_row = time_per_task.mean(numeric_only=True)
            avg_row["task"] = "平均"
            time_per_task = pd.concat([time_per_task, pd.DataFrame([avg_row])], ignore_index=True)

            # 新しいtime/taskにて1件あたりに要した時間を計算
            time_per_task["time_per_task"] = time_per_task["times"] / time_per_task["counts"]

            # データフレームとして表示する
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
                        for row in time_per_task.itertuples(index=False, name="Row")
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
        if all_df is not None:
            df=all_df
            locate_df=df.groupby(["locate","task"]).size().reset_index(name="counts")
            #self列は除外する
            try:
                locate_df.drop(index=locate_df[locate_df["locate"]=="self"].index,inplace=True)
            except KeyError:
                pass

            graph_width=int(len(locate_df["locate"].unique()))*77
            if graph_width<1000:
                graph_width=1000
            
            fig=px.bar(
                locate_df,
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
        else:
            df=dataframe
            locate_df=df.groupby(["locate","task"]).size().reset_index(name="counts")
            try:
                locate_df.drop(index=locate_df[locate_df["locate"]=="self"].index,inplace=True) #self列は除外する
            except KeyError:
                pass
            graph_width=int(len(locate_df["locate"].unique()))*77
            if graph_width<1000:
                graph_width=1000

            print(locate_df)

            #ft.CarChart用のデータ準備
            bar_groups=[]
            unique_locations=locate_df["locate"].unique()
            unique_tasks=locate_df["task"].unique()

            #
            for i,location in enumerate(unique_locations):
                location_data=locate_df[locate_df["locate"]==location]
                bars=[]

                #積み上げ用の累積値を計算
                cumulative_y=0
                for j,task in enumerate(unique_tasks):
                    task_data=location_data[location_data["task"]==task]
                    count=task_data["counts"].sum() if not task_data.empty else 0
                    
                    if count>0:
                        bars.append(
                            ft.BarChartRod(
                                from_y=0,
                                to_y=count,
                                width=20,
                                color=TASK_COLOR_MAP,
                                tooltip=f"{task}:{count}"
                            )
                        )

                if bars:
                    bar_groups.append(
                        ft.BarChartGroup(
                            x=i,
                            bar_rods=bars,
                        )
                    )

            #x軸のラベル
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Text(location)
                    )
                    for i,location in enumerate(unique_locations)
                ],
                labels_size=40,
            )

            #y axis
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i*10,
                        label=ft.Text(str(i*10))
                    )
                    for i in range(0,int(locate_df["counts"].max()/10)+2)
                ],
                labels_size=40,
            )

            bar_chart=ft.BarChart(
                bar_groups=bar_groups,
                left_axis=left_axis,
                border=ft.border.all(1,ft.colors.BLACK),
                bottom_axis=bottom_axis,
                horizontal_grid_lines=ft.ChartGridLines(
                    color=ft.colors.GREEN_300,
                    width=1,
                    dash_pattern=[3,3]

                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.5,ft.colors.GREY),
                max_y=locate_df["counts"].max()*1.1,
                expand=True,

            )
            result_field.controls=[
                ft.Container(
                    content=bar_chart,
                    height=600,
                ),
                Handlers_Chart._create_preview_button(chart=bar_chart,page=page), # グラフのプレビュー用ボタン
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="グラフを保存",
                    on_click=lambda _:Chart_Download_Handler.open_directory(page=page,barchart=bar_chart,chart_name="task_location"),
                )
            ]
            result_field.update()

    #date列を基に、日付ごとのタスクの分布を分析
    @staticmethod
    def date_task_analysis(dataframe,result_field,page,all_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        if all_df is not None:
            df=all_df
            #date列をdatetime型に変換
            df["date"]=pd.to_datetime(df["date"])
            #date列を基に、日付ごとのタスクの分布を分析
            date_group_df=df.groupby(["date","task"]).size().reset_index(name="counts")
            #counts は時間になる*15をすると作業時間となる
            #dateごとのタスクを積み上げ棒グラフで可視化
            graph_width=int(len(date_group_df["date"].unique()))*33
            if graph_width<1000:
                graph_width=1000
            fig=px.bar(
                date_group_df,
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
        else:
            df=dataframe
            #date列をdatetime型に変換
            df["date"]=pd.to_datetime(df["date"])
            #date列を基に、日付ごとのタスクの分布を分析
            date_group_df=df.groupby(["date","task"]).size().reset_index(name="counts")
            #counts は時間になる*15をすると作業時間となる
            #dateごとのタスクを積み上げ棒グラフで可視化
            graph_width=int(len(date_group_df["date"].unique()))*33
            if graph_width<1000:
                graph_width=1000
            fig=px.bar(
                date_group_df,
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
        if all_df is not None:
            df=all_df
            comment_df=df[df["comment"].notna()]
            comment_df=comment_df[["time","locate","date","phName","comment"]]
            comment_df=comment_df.reset_index(drop=True)
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
                        for row in comment_df.itertuples(index=False, name="Row")
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
        else:
            comment_df=dataframe[dataframe["comment"].notna()]
            comment_df=comment_df[["time","locate","date","phName","comment"]]
            comment_df=comment_df.reset_index(drop=True)
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
                        for row in comment_df.itertuples(index=False, name="Row")
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
        if self_df is not None:
            df=self_df
            time_for_phName_times=df.groupby(["phName","task"]).size().reset_index(name="times")
            #*15にすることで実際の時間に変換　(1入力15ふん）
            time_for_phName_times["times"]=time_for_phName_times["times"]*15
            #薬剤師ごとの件数を算出
            count_phName=dataframe.groupby(["phName","task"])["count"].sum().reset_index(name="counts")
            #薬剤師ごとの件数と時間の合計
            per_phName_df=pd.merge(
                count_phName,
                time_for_phName_times,
                on=["phName","task"],
                how="left"
            )
            #１件あたりの平均値を算出
            per_phName_df["time_per_task"]=per_phName_df["times"]/per_phName_df["counts"]
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
                                ft.DataCell(ft.Text(str(row.counts))),
                                ft.DataCell(ft.Text(str(row.times))),
                                ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                            ]
                        )
                        for row in per_phName_df.itertuples(index=False, name="Row")
                    ]
                ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=per_phName_df,name="self_analysis"),
                )
            ]
            result_field.update()
        else:
            time_for_phName_times=dataframe.groupby(["phName","task"]).size().reset_index(name="times")
            #*15にすることで実際の時間に変換　(1入力15ふん）
            time_for_phName_times["times"]=time_for_phName_times["times"]*15
            #薬剤師ごとの件数を算出
            count_phName=dataframe.groupby(["phName","task"])["count"].sum().reset_index(name="counts")
            #薬剤師ごとの件数と時間の合計
            per_phName_df=pd.merge(
                count_phName,
                time_for_phName_times,
                on=["phName","task"],
                how="left"
            )
            #１件あたりの平均値を算出
            per_phName_df["time_per_task"]=per_phName_df["times"]/per_phName_df["counts"]
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
                                ft.DataCell(ft.Text(str(row.counts))),
                                ft.DataCell(ft.Text(str(row.times))),
                                ft.DataCell(ft.Text(f"{row.time_per_task:.2f}")),
                            ]
                        )
                        for row in per_phName_df.itertuples(index=False, name="Row")
                    ]
                ),
                ft.ElevatedButton(
                    "保存",
                    icon=ft.icons.DOWNLOAD,
                    tooltip="データフレームを保存",
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=per_phName_df,name="self_analysis"),
                )
            ]
            result_field.update()

    @staticmethod
    def self_analysis_total_time(dataframe,result_field,page,self_df):
        Handlers_Chart.show_progress_bar(result_field, page)
        if self_df is not None:
            df=self_df
            time_for_phname_total=df.groupby(["phName","task"]).size().reset_index(name="times")
            #*15にすることで実際の時間に変換　(1入力15ふん）
            time_for_phname_total["times"]=time_for_phname_total["times"]*15
            #業務数列
            taskdf=dataframe.groupby(["phName","task"]).size().reset_index(name="task_count")
            #カウント列の合計を算出
            countdf=dataframe.groupby(["phName","task"])["count"].sum().reset_index(name="count_total")
            time_for_phname_total=pd.merge(
                time_for_phname_total,
                taskdf,
                on=["phName","task"],
                how="left"
            )
            time_for_phname_total=pd.merge(
                time_for_phname_total,
                countdf,
                on=["phName","task"],
                how="left"
            )
            #集計
            total_df=time_for_phname_total.groupby(["phName"])["times"].sum().reset_index(name="total_times")
            #phNameごとの総業務数
            total_df["task_count"]=time_for_phname_total.groupby("phName")["task_count"].transform("sum")
            #phNameごとの総件数
            total_df["count_total"]=time_for_phname_total.groupby("phName")["count_total"].transform("sum")

            #１業務あたりの時間列を追加
            total_df["time_per_task"]=total_df["total_times"]/total_df["task_count"]
            #1件あたりの時間列を追加
            total_df["time_per_count"]=total_df["total_times"]/total_df["count_total"]

            #一番下に平均値を追加
            avg_row=total_df.mean(numeric_only=True)
            avg_row["phName"]="平均"
            total_df=pd.concat([total_df,pd.DataFrame([avg_row])],ignore_index=True)

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
                    on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=time_for_phname_total,name="self_analysis_total_time"),
                )
            ]
            result_field.update()

        else:
            time_for_phname_total=dataframe.groupby(["phName","task"]).size().reset_index(name="times")
            #*15にすることで実際の時間に変換　(1入力15ふん）
            time_for_phname_total["times"]=time_for_phname_total["times"]*15
            #業務数列
            taskdf=dataframe.groupby(["phName","task"]).size().reset_index(name="task_count")
            #カウント列の合計を算出
            countdf=dataframe.groupby(["phName","task"])["count"].sum().reset_index(name="count_total")
            time_for_phname_total=pd.merge(
                time_for_phname_total,
                taskdf,
                on=["phName","task"],
                how="left"
            )
            time_for_phname_total=pd.merge(
                time_for_phname_total,
                countdf,
                on=["phName","task"],
                how="left"
            )
            #集計
            total_df=time_for_phname_total.groupby(["phName"])["times"].sum().reset_index(name="total_times")
            #phNameごとの総業務数
            total_df["task_count"]=time_for_phname_total.groupby("phName")["task_count"].transform("sum")
            #phNameごとの総件数
            total_df["count_total"]=time_for_phname_total.groupby("phName")["count_total"].transform("sum")

            #１業務あたりの時間列を追加
            total_df["time_per_task"]=total_df["total_times"]/total_df["task_count"]
            #1件あたりの時間列を追加
            total_df["time_per_count"]=total_df["total_times"]/total_df["count_total"]

            #一番下に平均値を追加
            avg_row=total_df.mean(numeric_only=True)
            avg_row["phName"]="平均"
            total_df=pd.concat([total_df,pd.DataFrame([avg_row])],ignore_index=True)

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