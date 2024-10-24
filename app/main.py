import flet as ft
import json
import calendar
import csv
import pandas as pd


def main(page: ft.Page):

    page.title = "Drag and Drop example"
    page.window.width = 1000
    page.scroll = "always"

    draggacle_data = {
        "_245": "処方修正",
        "_249": "医師からの問い合わせ",
        "_253": "看護師からの問い合わせ",
        "_257": "薬剤セット数",
        "_261": "持参薬を確認",
        "_265": "薬剤服用歴等について保険薬局へ照会",
        "_269": "TDM実施",
    }

    range_values = {}

    def drag_accepted(e):
        data = json.loads(e.data)
        src_id = data.get("src_id", "")
        print(src_id)
        key = draggacle_data.get(src_id, "")
        e.control.content = ft.Container(
            ft.Text(key, color="white"),
            width=50,
            height=90,
            bgcolor=ft.colors.BLUE_GREY_500,
        )
        e.control.update()
        range_values.setdefault(e.control.data, key)
        print(range_values)

    def write_csv_file(e):
        with open("output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Task"])
            for key, value in range_values.items():
                writer.writerow([key, value])

    save_button = ft.ElevatedButton(text="Save", on_click=write_csv_file)

    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            selected_files.text = ",".join(map(lambda x: x.name, e.files))
            file_paths = [f.path for f in e.files]
            try:
                # 空のデータフレームを作成
                df = pd.DataFrame()
                # ファイルの数だけ繰り返す
                df = pd.concat([pd.read_csv(file_path) for file_path in file_paths])
                # Task ごとにまとめる
                groupby_task = df.groupby("Task").size().reset_index(name="Count")
                print(groupby_task)
                # グラフを描画
                bar_charts = [
                    ft.BarChartGroup(
                        x=i,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=row["Count"],
                                color="blue",
                                border_radius=0,
                            )
                        ],
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

    file_picker = ft.FilePicker(on_result=pick_file_result)
    page.overlay.append(file_picker)

    selected_files = ft.Text()
    file_picker_Button = ft.ElevatedButton(
        "ファイルを選択",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )

    bar_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREEN_100),
        left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Count"), title_size=20),
        bottom_axis=ft.ChartAxis(labels_size=40),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.colors.GREEN_100, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREEN_100),
        max_y=10,
        interactive=True,
        expand=True,
    )

    hours = [
        "8:00",
        "9:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
    ]

    times = [
        "8:30 8:40",
        "8:40 8:50",
        "8:50 9:00",
        "9:00 9:10",
        "9:20 9:30",
        "9:30 9:40",
        "9:40 9:50",
        "9:50 10:00",
        "10:00 10:10",
        "10:10 10:20",
        "10:20 10:30",
        "10:30 10:40",
        "10:40 10:50",
        "10:50 11:00",
        "11:10 11:20",
        "11:20 11:30",
        "11:40 11:50",
        "11:50 12:00",
        "12:00 12:10",
        "12:10 12:20",
        "12:20 12:30",
        "12:30 12:40",
        "12:40 12:50",
        "12:50 13:00",
        "13:00 13:10",
        "13:10 13:20",
        "13:20 13:30",
        "13:30 13:40",
        "13:40 13:50",
        "13:50 14:00",
        "14:00 14:10",
        "14:10 14:20",
        "14:20 14:30",
        "14:30 14:40",
        "14:40 14:50",
        "14:50 15:00",
        "15:00 15:10",
        "15:10 15:20",
        "15:20 15:30",
        "15:30 15:40",
        "15:40 15:50",
        "15:50 16:00",
        "16:00 16:10",
        "16:10 16:20",
        "16:20 16:30",
        "16:30 16:40",
        "16:40 16:50",
        "16:50 17:00",
    ]
    columns = []
    for time in times:
        columns.append(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(time, size=12),
                        ft.DragTarget(
                            group="timeline",
                            content=ft.Container(
                                width=50,
                                height=90,
                                bgcolor=None,
                                border_radius=5,
                            ),
                            data=time,
                            on_accept=drag_accepted,
                        ),
                    ],
                    spacing=0,
                ),
                margin=0,
                padding=0,
            )
        )

    kinds = [
        "処方修正",
        "医師からの問い合わせ",
        "看護師からの問い合わせ",
        "薬剤セット",
        "持参薬を確認",
        "薬剤服用歴等について保険薬局へ照会",
        "TDM実施",
    ]
    selectColumns = []
    for kind in kinds:
        selectColumns.append(
            ft.Column(
                [
                    ft.Draggable(
                        group="timeline",
                        content=ft.Container(
                            ft.Text(kind, color="white"),
                            width=100,
                            height=70,
                            bgcolor=ft.colors.BLUE_GREY_500,
                            border_radius=5,
                        ),
                        data=kind,
                    )
                ]
            )
        )

    page.add(
        ft.Row(
            scroll=True,
            controls=columns,
        ),
        ft.Row(scroll=True, controls=selectColumns),
        save_button,
        file_picker_Button,
        selected_files,
        bar_chart,
    )


ft.app(main)
