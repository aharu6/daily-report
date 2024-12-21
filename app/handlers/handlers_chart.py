import pandas as pd
import flet as ft
from models.models import DataModel
from handlers.handlers import Handlers
from flet import FilePicker, FilePickerResultEvent

#Chartページ用のハンドラ   
class Handlers_Chart:
    @staticmethod
    def pick_file_result(e:ft.FilePickerResultEvent,selected_files,bar_chart):
        if e.files:
            selected_files.text = ",".join(map(lambda x:x.name,e.files))
            file_paths = [f.path for f in e.files]
            try:
                # 空のデータフレームを作成
                df = pd.DataFrame()
                # ファイルの数だけ繰り返す
                df = pd.concat([pd.read_csv(file_path) for file_path in file_paths])
                # Task ごとにまとめる
                groupby_task = df.groupby("Task").size().reset_index(name="Count")
                #病棟ごとのデータに変換するならここからまとめ直す
                bar_charts = [
                        ft.BarChartGroup(
                            x = i,
                            bar_rods = [
                                ft.BarChartRod(
                                    from_y = 0,
                                    to_y = row["Count"],
                                    color = "blue",
                                    border_radius = 0,
                                    tooltip = ft.Tooltip(message = f"{row['Count']}:{row['Count']*15}"),
                                )
                            ]
                        )
                        for i, row in groupby_task.iterrows()
                    ]
                x_labels = [
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Container(
                            ft.Text(row["Task"]), padding=ft.Padding(0, 0, 0, 0)
                        ),
                    )
                    for i, row in groupby_task.iterrows()
                ]
                bar_chart.bar_groups = bar_charts
                bar_chart.bottom_axis.labels = x_labels
                bar_chart.update()
            
            except Exception as e:
                print(e)
                