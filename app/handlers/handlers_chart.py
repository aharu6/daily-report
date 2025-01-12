import pandas as pd
import flet as ft
from models.models import DataModel
from handlers.handlers import Handlers
from flet import FilePicker, FilePickerResultEvent
import ast


# Chartページ用のハンドラ
class Handlers_Chart:
    @staticmethod
    def pick_file_result(e: ft.FilePickerResultEvent, selected_files, parent_instance):
        if e.files:
            selected_files.text = ",".join(map(lambda x: x.name, e.files))
            file_paths = [f.path for f in e.files]
            try:
                # 空のデータフレームを作成
                df = pd.DataFrame()
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
        print(df)

        # 算出したデータフレームから病棟数を算出し、病棟数分のcardを作成する
        # data =病棟名　でもつけて紐づけるできるように？
        group_df_locate = df.groupby(["locate"]).size().reset_index(name="counts")
        print(group_df_locate["locate"].unique())
        for locate in group_df_locate["locate"].unique():
            chart_field.append(
                ft.Card(
                    content=ft.Text(locate),
                    width=300,
                    data=locate,
                )
            )
        page.update()
        # その上にplotlyにて円フを作成する

    @staticmethod
    def ComponentChart_for_self(dataframe):
        """_summary_

        Args:
            dataframe (_type_): pick_file_resultで返されるデータフレーム
        """
        # データフレームを渡してグラフを生成する
        print(dataframe)
        # まずグラフを描画するcardを作成

        # その上にplotlyにて円グラフを作成する
