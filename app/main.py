import flet as ft
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
    print(today)

    def handle_change(e):
        global today
        selected_date = e.control.value  # 例えば "2024-10-25" のような形式
        print(selected_date)

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
    # sqlite3
    con = sqlite3.connect("timelime.db")
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS timeline ( time TEXT PRIMARY KEY,task TEXT,count INTEGER,locate TEXT,date TEXT)"
    )
    # sqliteデータベースを初期化
    cur.execute("DELETE FROM timeline")

    def counterPlus(e, count_filed):
        # eが入力したカラムの値（時間）を取得している
        # sqliteデータベースからカウントを取得
        res = cur.execute("SELECT count FROM timeline WHERE time = ?", (e,))
        old_Count = res.fetchall()[0][0]
        new_Count = old_Count + 1
        # sqlite3データベースへ上書き保存
        cur.execute(
            "UPDATE timeline SET count = ? WHERE time = ?",
            (
                new_Count,
                e,
            ),
        )
        # 更新した値にてカウンター内を更新
        count_filed.value = new_Count
        count_filed.update()

    def counterMinus(e, count_filed):
        # +と同様
        res = cur.execute("SELECT count FROM timeline WHERE time = ?", (e,))
        old_Count = res.fetchall()[0][0]
        new_Count = old_Count - 1
        cur.execute(
            """
            UPDATE timeline SET count = ? WHERE time = ?
            """,
            (
                new_Count,
                e,
            ),
        )
        # update counter value
        count_filed.value = new_Count
        count_filed.update()

    draggacle_data = {
        "_208": "処方修正",
        "_212": "医師からの問い合わせ",
        "_216": "看護師からの問い合わせ",
        "_220": "薬剤セット数",
        "_224": "持参薬を確認",
        "_228": "薬剤服用歴等について保険薬局へ照会",
        "_232": "TDM実施",
        "_236": "情報収集＋指導",
        "_240": "指導記録",
        "_244": "混注準備",
        "_248": "カンファレンス",
        "_252": "休憩",
        "_256": "相談応需",
    }

    def create_counter(e):
        # eは入力したカラムの時間を取得
        # sqlite3データベースからカウントを取得
        res = cur.execute("SELECT count FROM timeline WHERE time = ?", (e,))
        count = res.fetchall()[0][0]
        count_filed = ft.TextField(
            count,
            width=40,
            text_align=ft.TextAlign.CENTER,
            text_size=10,
            border_color=None,
        )
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

    range_values = {}

    def drag_move(e):
        data = json.loads(e.data)
        kind = e.data
        print("draggabeldata",kind)
        src_id = data.get("src_id", "")
        key = draggacle_data.get(src_id, "")
        time_data = e.control.data
        print("dragtargetdata", time_data)
        src = page.get_control(e.src_id)
        print("src;",src)
        
        # AMかPMかを判定
        locate = ""
        if e.control.data in amTime:
            locate = "AM"
        elif e.control.data in pmTime:
            locate = "PM"
        print("locate",locate)
        
        # 選択した日付(デフォルトは今日)
        date = today
        # sqlite3形式にて保存
        cur.execute(
        """
        DELETE FROM timeline WHERE time = ?
        """,
        (e.control.data,),  
        )
        
        cur.execute(
            """
            INSERT INTO timeline(time,task,count,locate,date) VALUES (?,?,?,?,?)
            """,
            (e.control.data, key, 0, locate, date),
        )
        con.commit()
        
        e.control.content = ft.Column(
            controls=[
                ft.Container(
                    ft.Text(key,color = "white"),
                    width = 50,
                    height = 140,
                    bgcolor = ft.colors.BLUE_GREY_500),
                create_counter(e.control.data),
            ],
            height=300,
            spacing=0,
        )
        e.control.update()

        range_values.setdefault(e.control.data, key)
        
            
        res = cur.execute("SELECT * FROM timeline")
        print(res.fetchall())
        
    def drag_accepted(e):
        data = json.loads(e.data)
        src_id = data.get("src_id", "")
        key =  draggacle_data.get(src_id, "")
        
    def write_csv_file(e):
        #save前にlocateを更新
        print("amdropdownvalue",amDropDown.value)
        
        cur.execute(""" 
                        UPDATE timeline SET locate = ? WHERE locate = "AM"
                    """,    
                    (amDropDown.value,)
                    )
        con.commit()
        cur.execute("""
                    UPDATE timeline SET locate = ? WHERE locate = "PM"
                    """,
                    (pmDropDown.value,)
                    )   
        con.commit()
        res = cur.execute("SELECT * FROM timeline") 
        data = res.fetchall()
        print(data)
        with open(f"{today}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Task", "Count", "locate", "date"])
            for key, value, count, locate, date in data:
                writer.writerow([key, value, count, locate, date])

    save_button = ft.ElevatedButton(text="Save", on_click=write_csv_file)

    
    kinds = [
        "処方修正",
        "医師からの問い合わせ",
        "看護師からの問い合わせ",
        "薬剤セット",
        "持参薬を確認",
        "薬剤服用歴等について保険薬局へ照会",
        "TDM実施",
        "情報収集＋指導",
        "指導記録",
        "混注準備",
        "カンファレンス",
        "休憩",
        "相談応需",
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
                        data= json.dumps({"kind":kind}),
                        on_drag_start = lambda e,kind = kind: print("drag start",kind),
                    ),
                ],
                spacing = 0
                
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
        "8:30 :45",
        ":45 :00",
        "9:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :00",
        "10:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :00",
        "11:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :00",
        "12:00 :15",
        ":15 :30",
        "12:30 :45",
        ":45 :00",
        "13:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :00",
        "14:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :00",
        "15:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :00",
        "16:00 :15",
        ":15 :30",
        ":30 :45",
        ":45 :1700",
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
    
    columns =[]

    for time in times:
        columns.append(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(time, size=10),
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
            )
        )

    def change_locateAM(e):
        # 現在のデータを入力された値に更新
        #なし
        print("changeam")
        
        
    def change_locatePM(e):
        #なし
        print("changepm")

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
        on_change=change_locateAM,
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
        on_change=change_locatePM,
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
                print(groupby_task)
                
                #件数か時間か
                print("graph_mode",graph_mode.selected_index) 
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
        if e.data == "0":
            bar_chart.left_axis = ft.ChartAxis(labels_size=40, title=ft.Text("Count"), title_size=20)
            bar_chart.update()
            print(df)
        elif e.data == "1":
            bar_chart.left_axis = ft.ChartAxis(labels_size=40, title=ft.Text("Time"), title_size=20)
            bar_chart.update()
            print(df)
            

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
