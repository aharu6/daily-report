import pandas as pd
import flet as ft
from models.models import DataModel
from handlers.handlers import Handlers
from flet import FilePicker, FilePickerResultEvent
import ast
import plotly
import plotly.express as px
from flet.plotly_chart import PlotlyChart


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
                print(e)

    @staticmethod
    def ComponentChart_for_location(dataframe, chart_field, page):
        """_summary_

        Args:
            dataframe (_type_): pick_file_resultで返されるデータフレーム
            chart_field (_type_): _description_
            page (_type_): _description_
        """
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
            df.groupby(["locate", "Task"]).size().reset_index(name="counts")
        )
        for locate in group_df_locate["locate"].unique():
            fig = px.pie(
                group_df_locate[group_df_locate["locate"] == locate],
                values="counts",
                names="Task",
                title=locate,
            )
            chart_field.append(
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
            )
        page.update()
        # その上にplotlyにて円グラフを作成する

    @staticmethod
    def ComponentChart_for_self(dataframe,chart_field,page):
        """_summary_

        Args:
            dataframe (_type_): pick_file_resultで返されるデータフレーム
        """
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
        gorup_by_person = df.groupby(["PhName","Task"]).size().reset_index(name="counts")
        
        
        # その上にplotlyにて円グラフを作成する
        fig_bar = px.bar(gorup_by_person,x = "counts",y = "PhName",color = "Task",barmode = "stack",orientation = "h")
        # まずグラフを描画するcardを作成
        chart_field.append(ft.Card(content = 
            PlotlyChart(fig_bar,expand = True,original_size = False,isolated = True)
        ))
        page.update()
