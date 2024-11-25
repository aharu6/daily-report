import flet as ft
from flet import Page
import json
import calendar
import csv
import pandas as pd
import sqlite3
import datetime
import sys


# main
def main(page: ft.Page):

    page.title = "Drag and Drop example"
    page.window.width = 1000
    page.scroll = "always"

    today = datetime.date.today()  # 今日の日付を取得

    def handle_change(e):
        global today
        selected_date = e.control.value  # 例えば "2024-10-25" のような形式

        # 文字列を日付オブジェクトに変換
        today = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()

        # 年、月、日を取得して表示用のテキストに変換
        Date.text = f"{today.year}/{today.month}/{today.day}"
        Date.update()

    Date = ft.ElevatedButton(
        f"{today.year}/{today.month}/{today.day}",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.date(
                    year=today.year, month=today.month, day=today.day
                ),
                on_change=handle_change,
            )
        ),
    )
        
    # カウンターの関数
    def counterPlus(e, count_filed):
        # eが入力したカラムの値（時間）を取得している
        old_Count = int(count_filed.value)
        new_Count = old_Count + 1
        # 更新した値にてカウンター内を更新
        count_filed.value = new_Count
        count_filed.update()
        #dict内の値を更新
        count_dict[e] = {"count":new_Count}

    def counterMinus(e, count_filed):
        # +と同様
        old_Count = int(count_filed.value)
        new_Count = old_Count - 1
        # update counter value
        count_filed.value = new_Count
        count_filed.update()
        count_dict[e] = {"count":new_Count}

    draggable_data = {
        '_280':{"task":"情報収集＋指導"},
        '_284':{"task":"指導記録作成"},
        '_288':{"task":"混注準備"},
        '_292':{"task":"混注時間"},
        '_296':{"task":"薬剤セット数"},
        '_300':{"task":"持参薬を確認"},
        '_304':{"task":"薬剤服用歴等について保険薬局へ照会"},
        '_308':{"task":"処方代理修正"},
        '_312':{"task":"TDM実施"},
        '_316':{"task":"カンファレンス"},
        '_320':{"task":"休憩"},
        '_324':{"task":"その他"},
    }
    
    count_dict = {}
    
    def create_counter(e):
        # eは入力したカラムの時間を取得
        # sqlite3データベースからカウントを取得
        #res = cur.execute("SELECT count FROM timeline WHERE time = ?", (e,))
        #count = res.fetchall()[0][0]
        #初期は０
        count = 0
        
        count_filed = ft.TextField(
            count,
            width=40,
            text_align=ft.TextAlign.CENTER,
            text_size=10,
            border_color=None,
        )
        count_dict[e] = {"count": count}
        return ft.Column(
            [
                ft.IconButton(
                    ft.icons.ADD,
                    icon_size=20,
                    on_click=lambda _: counterPlus(e, count_filed),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                count_filed,
                ft.IconButton(
                    ft.icons.REMOVE,
                    icon_size=20,
                    on_click=lambda _: counterMinus(e, count_filed),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
            ]
        )
        
    drag_data = {}
    
    last_key = {"task":None}
    
    def drag_move(e):
        data = json.loads(e.data)
        kind = e.data
        src_id = data.get("src_id", "")
        print(src_id)
        key = draggable_data.get(src_id,{}).get("task")
        #time_data = e.control.data
        src = page.get_control(e.src_id)
        
        if src_id in draggable_data:
            last_key["task"] = key
            draggable_data[src_id] = {'task':key}
        else:
            if last_key["task"] is not None:
                new_key = last_key["task"]
                draggable_data[src_id] = {'task':new_key}
                print(draggable_data)
            else:#last_keyが未設定の場合
                print("last_key is None")
                
            
        e.control.content = ft.Column(
            controls=[
                ft.Draggable(
                    group = "timeline",
                    content = ft.Container(
                        ft.Text(key,color = "white"),
                        width = 50,
                        height = 140,
                        bgcolor = ft.colors.BLUE_GREY_500,
                    ),
                    
                    ),
                create_counter(e.control.data),
            ],
            height=300,
            spacing=0,
        )
        e.control.update()
        drag_data[e.control.data] = {'task':key}     
    
    def add_draggable_data(src_id,key):
        print(key)
        #src_idがdrag_dataに含まれているかどうか
        if src_id in draggable_data:
            print("src_id in dragacle_data")
        else:
            draggable_data[src_id] = {'task':key['task']}
            print(draggable_data)
        
    def drag_accepted(e):
        data = json.loads(e.data)
        src_id = data.get("src_id", "")
        key =  draggable_data.get(src_id, "")
        
    def write_csv_file(e):
        #最後にデータベースに保管する

        #入力された辞書データの長さ
        #print(len(drag_data.keys()))
        #first_key = list(drag_data.keys())[0]
        #first_value = drag_data[first_key]
        #print(first_key)
    
        #初期ベースの作成
        #時間
        time_for_label = [
            columns[i].data
            for i in range(len(columns))
        ]
        #初期ベースの作成
        set_data = [
            {"time":time_for_label[i],"task":"","count":0,"locate":"AM" if time_for_label[i] in amTime else "PM","date":str(today)}
            for i in range(len(columns))
        ]
        #リストを辞書形式に変換
        data_dict = {record['time']:record for record in set_data}
        #辞書データの更新
        #taskデータの書き込み
        for time,task_data in drag_data.items():
            if time in data_dict:
                data_dict[time]["task"] = task_data["task"]
        #countデータの書き込み
        for time,count in count_dict.items():
            if time in data_dict:
                data_dict[time]["count"] = count["count"]
        #病棟データの書き込み
        for time in data_dict.keys():    
            if amDropDown.value != None:
                if data_dict[time]["locate"] == "AM":
                    data_dict[time]["locate"] = amDropDown.value
            else: None
        for time in data_dict.keys():    
            if pmDropDown.value != None:
                if data_dict[time]["locate"] == "PM":
                    data_dict[time]["locate"] =pmDropDown.value
            else: None
            
        page.client_storage.set("timeline_data",json.dumps(data_dict,ensure_ascii=False))
                
        with open(f"{today}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Task", "Count", "locate", "date"])
            for time, record in data_dict.items():
                writer.writerow([record["time"], record["task"], record["count"], record["locate"], record["date"]])

    save_button = ft.ElevatedButton(text="Save", on_click=write_csv_file)
    
    selectColumns = []
    
    for kind in draggable_data.values():
        selectColumns.append(
            ft.Column(
                [
                    ft.Draggable(
                        group="timeline",
                        content=ft.Container(
                            ft.Text(kind["task"], color="white"),
                            width=100,
                            height=70,
                            bgcolor=ft.colors.BLUE_GREY_500,
                            border_radius=5,
                        ),
                        data= json.dumps({"kind":kind}),
                    ),
                ],
                spacing = 0,
                data = kind,
            )
        )

    times = [
        "8:30 8:45",
        "8:45 9:00",
        "9:00 9:15",
        "9:15 9:30",
        "9:30 9:45",
        "9:45 10:00",
        "10:00 10:15",
        "10:15 10:30",
        "10:30 10:45",
        "10:45 11:00",
        "11:00 11:15",
        "11:15 11:30",
        "11:30 11:45",
        "11:45 12:00",
        "12:00 12:15",
        "12:15 12:30",
        "12:30 12:45",
        "12:45 13:00",
        "13:00 13:15",
        "13:15 13:30",
        "13:30 13:45",
        "13:45 14:00",
        "14:00 14:15",
        "14:15 14:30",
        "14:30 14:45",
        "14:45 15:00",
        "15:00 15:15",
        "15:15 15:30",
        "15:30 15:45",
        "15:45 16:00",
        "16:00 16:15",
        "16:15 16:30",
        "16:30 16:45",
        "16:45 17:00",
    ]
    time_for_visual = [
        "8:30      ",
        "8:45        ",
        "9:00        ",
        "9:15         ",
        "9:30        ",
        "9:45         ",
        "10:00        ",
        "10:15        ",
        "10:30        ",
        "10:45        ",
        "11:00        ",
        "11:15        ",
        "11:30        ",
        "11:45       ",
        "12:00       ",
        "12:15       ",
        "12:30        ",
        "12:45       ",
        "13:00       ",
        "13:15       ",
        "13:30       ",
        "13:45       ",
        "14:00       ",
        "14:15       ",
        "14:30        ",
        "14:45        ",
        "15:00        ",
        "15:15        ",
        "15:30        ",
        "15:45       ",
        "16:00       ",
        "16:15       ",
        "16:30       ",
        "16:45       ",
        "17:00       ",
        
        ]

    amTime = [
        "8:30 8:45",
        "8:45 9:00",
        "9:00 9:15",
        "9:15 9:30",
        "9:30 9:45",
        "9:45 10:00",
        "10:00 10:15",
        "10:15 10:30",
        "10:30 10:45",
        "10:45 11:00",
        "11:00 11:15",
        "11:15 11:30",
        "11:30 11:45",
        "11:45 12:00",
        "12:00 12:15",
        "12:15 12:30",
    ]

    pmTime = [
        "12:30 12:45",
        "12:45 13:00",
        "13:00 13:15",
        "13:15 13:30",
        "13:30 13:45",
        "13:45 14:00",
        "14:00 14:15",
        "14:15 14:30",
        "14:30 14:45",
        "14:45 15:00",
        "15:00 15:15",
        "15:15 15:30",
        "15:30 15:45",
        "15:45 16:00",
        "16:00 16:15",
        "16:15 16:30",
        "16:30 16:45",
        "16:45 17:00",
    ]  
    time_for_visual_label  = []
    for i in time_for_visual:
        time_for_visual_label.append(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(i, size=10),
                    ]
                )
            )
        )
        
    columns =[]

    for time in times:
        columns.append(
            ft.Container(
                ft.Column(
                    [
                        #ft.Text(time, size=10),
                        ft.DragTarget(
                            group="timeline",
                            content=ft.Container(
                                width=50,
                                height=300,
                                bgcolor=None,
                                border_radius=5,
                            ),
                            data=time,
                            on_accept=drag_accepted,
                            on_move =drag_move,
                        ),
                    ],
                    spacing=0,
                ),
                margin=0,
                padding=0,
                data = time,
            )
        )

    amDropDown = ft.Dropdown(
        width=130,
        options=[
            ft.dropdown.Option("ICU"),
            ft.dropdown.Option("3A"),
            ft.dropdown.Option("3B"),
            ft.dropdown.Option("3C"),
            ft.dropdown.Option("CCU"),
            ft.dropdown.Option("4A"),
            ft.dropdown.Option("4B"),
            ft.dropdown.Option("4C"),
            ft.dropdown.Option("HCU"),
            ft.dropdown.Option("5A"),
            ft.dropdown.Option("5B"),
            ft.dropdown.Option("5C"),
            ft.dropdown.Option("5D"),
        ],
        label="AM",
        text_size=12,
        label_style=ft.TextStyle(size=12),
        border_color=ft.colors.BLUE_GREY_100,
        height=40,
    )
    pmDropDown = ft.Dropdown(
        width=130,
        options=[
            ft.dropdown.Option("ICU"),
            ft.dropdown.Option("3A"),
            ft.dropdown.Option("3B"),
            ft.dropdown.Option("3C"),
            ft.dropdown.Option("CCU"),
            ft.dropdown.Option("4A"),
            ft.dropdown.Option("4B"),
            ft.dropdown.Option("4C"),
            ft.dropdown.Option("HCU"),
            ft.dropdown.Option("5A"),
            ft.dropdown.Option("5B"),
            ft.dropdown.Option("5C"),
            ft.dropdown.Option("5D"),
        ],
        label="PM",
        text_size=12,
        label_style=ft.TextStyle(size=12),
        border_color=ft.colors.BLUE_GREY_100,
        height=40,
    )

    ampmSelect = ft.Row(
        controls=[
            amDropDown,
            ft.Container(height=20, width=10),
            pmDropDown,
        ]
    )

    TimeLine = ft.Row(
        scroll=True,
        controls=[
            ft.Column(
                controls=[
                    ampmSelect,
                    ft.Row(controls=time_for_visual_label),
                    ft.Row(controls=columns),
                ],
            ),
        ],
    )
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
    
    def change_grapgh_mode(e):
        print(e.data)

    page.add(
        Date,
        TimeLine,
        ft.Row(scroll=True, controls=selectColumns),
        save_button,
        file_picker_Button,
        selected_files,
        bar_chart,
    )


ft.app(main)
