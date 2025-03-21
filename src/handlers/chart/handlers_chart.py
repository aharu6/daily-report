import pandas as pd
import flet as ft
from flet import FilePicker, FilePickerResultEvent
import ast
import plotly
import plotly.express as px
import plotly.io as pio
from flet.plotly_chart import PlotlyChart
import chart_studio.plotly as py

# Chartページ用のハンドラ
class Handlers_Chart:
    @staticmethod
    def pick_file_result(e: ft.FilePickerResultEvent, selected_files, parent_instance):
        """_summary_

        Args:
            e (ft.FilePickerResultEvent): _description_
            selected_files (_type_): _description_
            parent_instance (_type_): _description_
        """
        if e.files:
            selected_files.text = ",".join(map(lambda x: x.name, e.files))
            file_paths = [f.path for f in e.files]
            try:
                # ファイルの数だけ繰り返す
                parent_instance.dataframe = pd.concat(
                    [pd.read_csv(file_path) for file_path in file_paths]
                )
                # Task ごとにまとめる
                # parent_instance.dataframe = df.groupby("Task").size().reset_index(name="Count")
                # 病棟ごとのデータに変換するならここからまとめ直す

            except Exception as e:
                pass
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
    def ComponentChart_for_standard(dataframe, chart_field, page):
        Handlers_Chart.show_progress_bar(chart_field, page)
        new_rows = []
        for index, row in dataframe.iterrows():
            tarn_row = ast.literal_eval(row["locate"])
            for loc in range(len(tarn_row)):
                new_row = row.copy()
                new_row["locate"] = tarn_row[loc]
                new_rows.append(new_row)
        df = pd.DataFrame(new_rows) 
        
        # bubble chart
        group_bubble = df.groupby(["locate","task","count"]).size().reset_index(name="times")
        #Countsが0の場合とそれ以外に分かれるので、それぞれを合計する
        group_bubble2 = group_bubble.groupby(["locate","task"]).sum(numeric_only=True).reset_index()
        #times*15 = かかった時間となるので計算しなおす
        group_bubble2["times"] = group_bubble2["times"]*15
        bar_chart=px.bar(group_bubble2,x="task",y="times")
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
        chart_field.controls = [(ft.Card(content = PlotlyChart(bar_chart,expand = True,original_size = False,isolated = True)))]
        page.update()
        

        
    @staticmethod
    def ComponentChart_for_location(dataframe, chart_field, page):
        """_summary_

        Args:
            dataframe (_type_): pick_file_resultで返されるデータフレーム
            chart_field (_type_): _description_
            page (_type_): _description_
        """
        Handlers_Chart.show_progress_bar(chart_field, page)
        # データフレームを渡してグラフを生成する
        # まずグラフを描画するcardを病棟数分作成
        # 取得したデータフレームから病棟の数,名前を取得
        # locateは複数選択にてリスト形式になっているからバラす必要がある
        new_rows = []
        for index, row in dataframe.iterrows():
            tarn_row = ast.literal_eval(row["locate"])
            for loc in range(len(tarn_row)):
                new_row = row.copy()
                new_row["locate"] = tarn_row[loc]
                new_rows.append(new_row)

        df = pd.DataFrame(new_rows)

        # 算出したデータフレームから病棟数を算出し、病棟数分のcardを作成する
        # data =病棟名　でもつけて紐づけるできるように？
        group_df_locate = (
            df.groupby(["locate", "task"]).size().reset_index(name="counts")
        )
        for locate in group_df_locate["locate"].unique():
            fig = px.pie(
                group_df_locate[group_df_locate["locate"] == locate],
                values="counts",
                names="task",
                title=locate,
            )
            chart_field.controls = [
                ft.Card(
                    content=ft.Column(
                        controls=[
                            PlotlyChart(
                                fig, expand=True, original_size=False, isolated=True
                            ),
                            ft.Text(locate),
                        ],
                        width="30%",
                    ),
                    data=locate,
                    col={"sm": 10, "md": 6, "xl": 4},
                )
            ]
        page.update()
        # その上にplotlyにて円グラフを作成する

    @staticmethod
    def ComponentChart_for_self(dataframe,chart_field,page):
        """_summary_

        Args:
            dataframe (_type_): pick_file_resultで返されるデータフレーム
        """
        Handlers_Chart.show_progress_bar(chart_field, page)
        #データフレームの作成
        new_rows = []
        for index, row in dataframe.iterrows():
            tarn_row = ast.literal_eval(row["locate"])
            for loc in range(len(tarn_row)):
                new_row = row.copy()
                new_row["locate"] = tarn_row[loc]
                new_rows.append(new_row)

        df = pd.DataFrame(new_rows)
        
        # 個人ごとにデータをまとめ直す
        gorup_by_person = df.groupby(["phName","task"]).size().reset_index(name="counts")
        
        # その上にplotlyにて円グラフを作成する
        fig_bar = px.bar(gorup_by_person, x="counts", y="phName", color="task", barmode="stack", orientation="h")
        # まずグラフを描画するcardを作成
        chart_field.controls = [
            ft.Card(content = 
                PlotlyChart(fig_bar,expand = True,original_size = False,isolated = True)
            )
        ]
        page.update()
