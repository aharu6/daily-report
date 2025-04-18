import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import pandas as pd
from handlers.chart.download_handler import Chart_Download_Handler
from handlers.chart.download_dataframe import DataframeDownloadHandler
class Handlers_analyze:
    #各タスクがどの時間帯に集中しているかを分析。　ヒートマップ
    @staticmethod
    def time_task_analysis(dataframe, result_field, page):  
        Handlers_Chart.show_progress_bar(result_field, page)
        df=dataframe
        task_per_time_heatmap=df.groupby(["task","time"]).size().reset_index(name="counts")
        fig=px.density_heatmap(
            task_per_time_heatmap,
            x="time",
            y="task",
            z="counts",
            title="時間ごとに業務が記録された回数",
            labels={"time": "Time", "task": "Task", "counts": "Task Count"},
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
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


    #業務内容ごとの件数
    @staticmethod
    def task_par_count(dataframe, result_field, page):
        Handlers_Chart.show_progress_bar(result_field, page)
        df=dataframe
        #業務内容と場所ごとに集計する
        count_per_task_locate=df.groupby(["locate","task"])["count"].sum().reset_index(name="counts")
        #保存用の横長データフレーム
        #病棟全ての合計と病棟ごとの合計
        sum_task_counts_pi=count_per_task_locate.pivot_table(
            values="counts",
            index="task",
            columns="locate",
            fill_value=0,
        )

        #件数集計していない業務は削除する
        #件数入力しない（混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンス）
        #上記業務内容を入力していない場合はdropでエラーになるから、止まらないようにする
        try:
            sum_task_counts_pi.drop(index="混注時間",inplace=True)
            sum_task_counts_pi.drop(index="休憩",inplace=True)
            sum_task_counts_pi.drop(index="委員会",inplace=True)
            sum_task_counts_pi.drop(index="WG活動",inplace=True)
            sum_task_counts_pi.drop(index="勉強会参加",inplace=True)
            sum_task_counts_pi.drop(index="1on1",inplace=True)
            sum_task_counts_pi.drop(index="カンファレンス",inplace=True)
        except KeyError:
            pass

        #合計値列と平均値列を追加する
        sum_task_counts_pi["sum"]=sum_task_counts_pi.sum(axis=1)
        sum_task_counts_pi["mean"]=sum_task_counts_pi.iloc[:,:-1].mean(axis=1)
        result_field.controls=[
            ft.DataTable(
                columns=[ft.DataColumn(ft.Text("業務内容"))]+[
                    ft.DataColumn(ft.Text(sum_task_counts_pi.columns[i]))
                    for i in range(len(sum_task_counts_pi.columns))
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[j]))) if j < len(row) else ft.DataCell(ft.Text(""))
                            for j in range(len(row))
                        ]
                    )
                    for row in sum_task_counts_pi.itertuples(name="Row")
                ]
            ),
            ft.ElevatedButton(
                "保存",
                icon=ft.icons.DOWNLOAD,
                tooltip="データフレームを保存",
                on_click=lambda _:DataframeDownloadHandler.open_directory_for_dataframe(page=page,dataframe=sum_task_counts_pi,name="counts_per_task"),
            )
        ]
        """for i in range(len(sum_task_counts_pi.columns)):    
            result_field.controls[0].columns.append(
                ft.DataColumn(ft.Text(sum_task_counts_pi.columns[i]))
            )
        """
        
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
    def task_par_location(dataframe, result_field, page):
        Handlers_Chart.show_progress_bar(result_field, page)
        df=dataframe
        locate_df=df.groupby(["locate","task"]).size().reset_index(name="counts")
        fig=px.bar(
            locate_df,
            x="locate",
            y="counts",
            color="task",
            title="場所ごとに記録された業務内容と記録回数",
            labels={"locate": "Location", "counts": "Task Count", "task": "Task"},
            barmode="stack",
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
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
    def date_task_analysis(dataframe,result_field,page):
        Handlers_Chart.show_progress_bar(result_field, page)
        df=dataframe
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
            title="日付ごとに記録された業務内容と記録回数",
            labels={"date": "Date", "counts": "Task Count", "task": "Task"},
            barmode="stack",
        )
        result_field.controls=[
            PlotlyChart(fig),#グラフ
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
    def comment_analysis(dataframe,result_field,page):
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
