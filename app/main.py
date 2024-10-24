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
        "_197": "処方修正",
        "_201": "医師からの問い合わせ",
        "_205": "看護師からの問い合わせ",
        "_209": "薬剤セット数",
        "_213": "持参薬を確認",
        "_217": "薬剤服用歴等について保険薬局へ照会",
        "_213": "TDM実施",
    }

    range_values = {}

    def drag_accepted(e):
        data = json.loads(e.data)
        src_id = data.get("src_id", "")
        print(src_id)
        key = draggacle_data.get(src_id, "")
        e.control.content = ft.Container(
            ft.Text(key),
            width=50,
            height=50,
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
    graph_Space = ft.Container()
    selected_files = ft.Text()

    def pick_file_result(e: ft.FilePickerResultEvent):
        print(e.files)

    file_picker = ft.FilePicker(on_result=pick_file_result)

    file_picker_Button = ft.ElevatedButton(
        "ファイルを選択",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )

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
        "16:50 17:00",]
    columns = []
    for time in times:
        columns.append(
            ft.Column(
                [
                    ft.Text(time, size=10),
                    ft.DragTarget(
                        group="timeline",
                        content=ft.Container(
                            width=50,
                            height=50,
                            bgcolor=ft.colors.BLUE_GREY_100,
                            border_radius=5,
                        ),
                        data=time,
                        on_accept=drag_accepted,
                    ),
                ]
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
                            ft.Text(kind),
                            width=50,
                            height=50,
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
        graph_Space,
    )


ft.app(main)
