import flet as ft
from handlers.chart.handlers_chart import Handlers_Chart
class Handlers_analyze:
    #時間帯ごとのタスク分析
    @staticmethod
    def time_task_analysis(dataframe, result_field, page):  
        
        pass
    #業務内容ごとの件数
    @staticmethod
    def task_par_count(dataframe, result_field, page):
        pass

    #件数あたりの時間
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