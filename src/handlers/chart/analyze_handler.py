import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import pandas as pd
class Handlers_analyze:
    #各タスクがどの時間帯に集中しているかを分析。　ヒートマップ
    @staticmethod
    def time_task_analysis(dataframe, result_field, page):  
        Handlers_Chart.show_progress_bar(result_field, page)
        df=Handlers_Chart.create_dataframe(dataframe)
        task_per_time_heatmap=df.groupby(["task","time"]).size().reset_index(name="counts")
        fig=px.density_heatmap(
            task_per_time_heatmap,
            x="time",
            y="task",
            z="counts",
            title="Task Distribution by Time (Heatmap)",
            labels={"time": "Time", "task": "Task", "counts": "Task Count"},
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
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


    #業務内容ごとの件数
    @staticmethod
    def task_par_count(dataframe, result_field, page):
        Handlers_Chart.show_progress_bar(result_field, page)
        df=Handlers_Chart.create_dataframe(dataframe)
        task_per_count=df.groupby(["task"])["count"].sum().reset_index(name="counts")
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
                            ft.DataCell(ft.Text(str(row.counts)))
                        ]
                    )
                    for row in task_per_count.itertuples(index=False, name="Row")
                ]
            )
        ]
        result_field.update()

    #件数あたりの時間 件数あたりに要した時間の算出
    @staticmethod
    def count_par_time(dataframe, result_field, page):
        """_summary_

        Args:
            dataframe (_type_): _description_
            result_field (_type_): グラフかデータフレームを表示する=ft.ResponsiveRow(controls=)
            page (_type_): _description_
        """
        Handlers_Chart.show_progress_bar(result_field, page)
        df=Handlers_Chart.create_dataframe(dataframe)
        time_per_task=df.groupby(["task"]).size().reset_index(name="times")
        #times列に*15することで、実際の時間に変換（１入力あたり１５分のため）
        time_per_task["times"]=time_per_task["times"]*15
        #count列を合計しておく
        count_per_task=df.groupby(["task"])["count"].sum().reset_index(name="counts")
        time_per_task["counts"]=count_per_task["counts"]

        # 新しいtime/taskにて1件あたりに要した時間を計算
        time_per_task["time_per_task"] = time_per_task["times"] / time_per_task["counts"]
        
        # データフレームとして表示する
        result_field.controls = [
            ft.Text("1件あたりに要した時間の算出", size=20),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("業務内容")),
                    ft.DataColumn(ft.Text("件数")),
                    ft.DataColumn(ft.Text("時間")),
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
            )
        ]
        page.update()

    #各タスクがどの場所（locate列）で行われたかを集計。
    @staticmethod
    def task_par_location(dataframe, result_field, page):
        Handlers_Chart.show_progress_bar(result_field, page)
        df=Handlers_Chart.create_dataframe(dataframe)
        locate_df=df.groupby(["locate","task"]).size().reset_index(name="counts")
        fig=px.bar(
            locate_df,
            x="locate",
            y="counts",
            color="task",
            title="Task Distribution by Location",
            labels={"locate": "Location", "counts": "Task Count", "task": "Task"},
            barmode="stack",
        )
        result_field.controls=[
            ft.Text("場所ごとに記録された業務内容と記録回数を表示",size=20),
            PlotlyChart(fig),#
        ]
        result_field.update()

    #date列を基に、日付ごとのタスクの分布を分析
    @staticmethod
    def date_task_analysis(dataframe,result_field,page):
        Handlers_Chart.show_progress_bar(result_field, page)
        df=Handlers_Chart.create_dataframe(dataframe)
        #date列をdatetime型に変換
        df["date"]=pd.to_datetime(df["date"])
        #date列を基に、日付ごとのタスクの分布を分析
        date_group_df=df.groupby(["date","task"]).size().reset_index(name="counts")
        #counts は時間になる*15をすると作業時間となる
        #dateごとのタスクを積み上げ棒グラフで可視化
        fig=px.bar(
            date_group_df,
            x="date",
            y="counts",
            color="task",
            title="Task Distribution by Date",
            labels={"date": "Date", "counts": "Task Count", "task": "Task"},
            barmode="stack",
        )
        result_field.controls=[
            ft.Text("日付ごとに記録された業務内容と記録回数を表示",size=20),
            PlotlyChart(fig),#
        ]
        result_field.update()