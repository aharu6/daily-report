import flet as ft
from flet import Page
import json
import calendar
import csv
import pandas as pd
import sqlite3
import datetime
import sys
from tkinter import filedialog

# main
def main(page: ft.Page):

    page.title = "Drag and Drop example"
    page.window.width = 1100
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
    
    # 薬剤師名の入力
    phNameList = page.client_storage.get("phName")
    # phNameListに基づき名前ごとにドロップダウンを作成
    # 最後にはデータ追加ボタンを実装する
    
    # phNameListがない場合はaddListのみを表示
    if phNameList is not None:
        phNameList = json.loads(phNameList)
    else:
        phNameList = []
        
    def update_dropdown():
        options = [ft.dropdown.Option(item["name"]) for item in phNameList]
        options.append(ft.dropdown.Option("Add"))
        phName.options = options
        page.update()
    
    # phNameListへの追加
    def add_name(e):
        new_name = name_field.value.strip()
        if new_name:
            phNameList.append({"name":new_name})
            page.client_storage.set("phName",json.dumps(phNameList,ensure_ascii=False))
            name_field.value = ""
            update_dropdown()
        dialog.open = False
        page.update()
        
    # Add が選択された時の処理
    def dropdown_changed(e) :
        if phName.value  == "Add":
            dialog.open  = True
            page.update()
        else:
            page.update()
                
    name_field = ft.TextField(label = "新しく追加する名前を入力してください")
    
    dialog = ft.AlertDialog(
        title = ft.Text("Add Name"),
        content = name_field,
        actions = [
            ft.TextButton("追加",on_click= add_name),
            ft.TextButton("キャンセル",on_click = lambda e:close_dialog())
        ],
    )
    
    def close_dialog():
        dialog.open = False
        page.update()
        
    
    
    iconforphname = ft.Icon(ft.icons.ACCOUNT_CIRCLE)
        
    phName = ft.Dropdown(
        width=130,
        options = [],
        on_change = dropdown_changed,
        label = "Name",
        text_size = 12,
        label_style = ft.TextStyle(size = 12),
        border_color = ft.colors.BLUE_GREY_100,
        height = 40,
    )
    update_dropdown()
    
    colphName = ft.Column(
        [iconforphname,phName],
    )
    
    # あとでメニューバーに変更するかも
    popup_menu = ft.PopupMenuButton(
        items =[
            ft.PopupMenuItem(text = "edit")
        ]
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
    # editButton
    editButton = ft.IconButton(
        icon = ft.icons.DELETE_OUTLINE,
        icon_size = 20,
        on_click = lambda e:toggle_delete_button(e),
        )
    
    delete_buttons = [
        ft.IconButton(
            icon = ft.icons.REMOVE,
            visible = False,
            icon_color = "red",
            icon_size = 20,
            on_click = lambda e:delete_content(e),
        )
        for _ in range(len(times))
    ]
    delete_button = ft.IconButton(
        icon = ft.icons.REMOVE,
        visible = False,
        on_click = lambda e:delete_content(e),
    )
    
    ineditButton = ft.Row(
        controls = [editButton],
        alignment = ft.MainAxisAlignment.END,
    )
    def toggle_delete_button(e):
        for button in delete_buttons:
            button.visible = not button.visible
        page.update()
        
    def delete_content(e):
        #_move関数でdelete_button.dataに入れたのはdragtargetで設定したカラムの番号
        #columns[i]でそのカラムの情報を取得し、見た目上削除
        #正しくはcolumnsの初期化を行う。ドラッグする前の状態に戻す
        col_num = delete_buttons[e.control.data["num"]].data["num"]
        #同じ情報の新しいカラムに差し替える
        columns[col_num].content  = ft.DragTarget(
            group = "timeline",
            content = ft.Container(
                width = 50,
                height = 300,
                bgcolor = None,
                border_radius = 5,
            ),
            on_accept = drag_accepted,
            on_move = drag_move,
            data = {"time":times[col_num],"num":col_num}
        )
        columns[col_num].update()
        #同時に該当するdrag_dataのデータも削除する
        del drag_data[times[col_num]]
            
    # カウンターの関数
    def counterPlus(e, count_filed):
        
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
        '_269':{"task":"情報収集＋指導"},
        '_273':{"task":"指導記録作成"},
        '_277':{"task":"混注準備"},
        '_281':{"task":"混注時間"},
        '_285':{"task":"薬剤セット数"},
        '_289':{"task":"持参薬を確認"},
        '_293':{"task":"薬剤服用歴等について保険薬局へ照会"},
        '_297':{"task":"処方代理修正"},
        '_301':{"task":"TDM実施"},
        '_305':{"task":"カンファレンス"},
        '_309':{"task":"休憩"},
        '_313':{"task":"その他"},
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
                    ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: counterPlus(e, count_filed),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                count_filed,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: counterMinus(e, count_filed),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
            ]
        )
        
    drag_data = {}
    
    last_key = {"task":None}
    
    comments = [
        ft.IconButton(
            icon = ft.icons.COMMENT,
            on_click = lambda e:create_dialog_for_comment(e),
            )
        for _ in range(len(times))
    ]
    
    comment = ft.IconButton(
        icon = ft.icons.COMMENT,
        on_click = lambda e:dlg_open(e),
    )
    
    def dlg_close(e):
        dlg.open = False
        page.update()
    
    comment_dict = {}
    def create_dialog_for_comment(e):
        comment_time = comments[e.control.data["num"]].data["time"]
        comment_num = comments[e.control.data["num"]].data["num"]
        dlg.data = {"time":comment_time,"num":comment_num}
        dlg.open = True
        page.update()
        
        
    def dlg_open(e):
        dlg.visible = True
    
    def add_comennt_for_dict(e):
        comment_time = dlg.data["time"]
        comment_num = dlg.data["num"]
        if comment_time in comment_dict:
            del comment_dict[comment_time]
            comment_dict[comment_time] = {"comment":comment_filed.value}
        else:
            comment_dict[comment_time] = {"comment":comment_filed.value}
        print(comment_time)
        print(comment_dict)
        dlg.open = False
        page.update()
    
    comment_filed = ft.TextField(label = "その他")
    
    dlg = ft.AlertDialog(
        title = ft.Text("Comment"),
        content = comment_filed,
        actions = [
            ft.TextButton("OK",on_click = lambda e:add_comennt_for_dict(e)),
            ft.TextButton("Cancel",on_click = lambda e:dlg_close(e)),
        ],
    )
    
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
            else:#last_keyが未設定の場合
                print("last_key is None")
        
        #ドラッグした時、「その他」ならば入力フォームも追加しておく
        
        if key == "その他":
            e.control.content = ft.Column(
                controls=[
                    delete_buttons[e.control.data["num"]],
                    ft.Draggable(
                        group = "timeline",
                        content = ft.Container(
                            ft.Text(key,color = "white"),
                            width = 50,
                            height = 100,
                            bgcolor = ft.colors.BLUE_GREY_500,
                        ),
                        ),
                    comments[e.control.data["num"]],
                    create_counter(e.control.data["time"]),
                ],
                height=300,
                spacing=0,
            )
            e.control.update()
            
        else:
            e.control.content = ft.Column(
                controls=[
                    delete_buttons[e.control.data["num"]],
                    ft.Draggable(
                        group = "timeline",
                        content = ft.Container(
                            ft.Text(key,color = "white"),
                            width = 50,
                            height = 140,
                            bgcolor = ft.colors.BLUE_GREY_500,
                        ),
                        ),
                    create_counter(e.control.data["time"]),
                ],
                height=300,
                spacing=0,
            )
            e.control.update()
            
        drag_data[e.control.data["time"]] = {'task':key}
        delete_buttons[e.control.data["num"]].data = {"time":e.control.data["time"],"num":e.control.data["num"]}
        
        if comment:
            comments[e.control.data["num"]].data = {"time":e.control.data["time"],"num":e.control.data["num"]}  
    
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
        time_for_label = times
        #初期ベースの作成
        set_data = [
            {"time":time_for_label[i],"task":"","count":0,"locate":"AM" if time_for_label[i] in amTime else "PM","date":str(today),"PhName":"","comment":""}
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
        # phName データの書き込み
        for time in data_dict.keys():
            if phName.value != None:
                data_dict[time]["phName"] = phName.value
            else: data_dict[time]["phName"] = ""
        page.client_storage.set("timeline_data",json.dumps(data_dict,ensure_ascii=False))
        # その他コメントの書き込み
        for time,comment_data in comment_dict.items():
            if time in data_dict:
                data_dict[time]["comennt"] = comment_data["comment"]
            else:data_dict[time]["comennt"] = ""
        
        
        #csvファイルの書き込み  
        if select_directory.result and select_directory.result.path:
            file_path = select_directory.result.path + f"/{today}.csv"
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Task", "Count", "locate", "date","PhName","Comment"])
                for time, record in data_dict.items():
                    writer.writerow([record["time"], record["task"], record["count"], record["locate"], record["date"],record["phName"],record["comment"]])

    save_button = ft.ElevatedButton(text="Save", on_click=lambda e:select_directory.get_directory_path())
    select_directory = ft.FilePicker(on_result = write_csv_file)
    page.overlay.append(select_directory)
        
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
        
    columns =[ft.Container() for _ in range(len(times))]
    
    for i ,column in enumerate(columns):
        column.content = ft.DragTarget(
            group = "timeline",
            content = ft.Container(
                width = 50,
                height = 300,
                bgcolor = None,
                border_radius = 5,
            ),
            on_accept = drag_accepted,
            on_move = drag_move,
            data = {"time":times[i],"num":i}
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
    
    #ampmSelecticon
    iconforampmselect = ft.Icon(ft.icons.SCHEDULE)

    ampmSelect = ft.Row(
        controls=[
            amDropDown,
            ft.Container(height=20, width=10),
            pmDropDown,
        ]
    )
    
    colampamSelect = ft.Column([iconforampmselect, ampmSelect])

    TimeLine = ft.Row(
        scroll=True,
        controls=[
            ft.Column(
                controls=[ 
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
    body = [
        
    ]
    page.add(
        Date,
        dialog,
        ft.Row(controls = [colphName,ft.Container(height=20, width=50),colampamSelect]),
        ineditButton,
        TimeLine,
        dlg,
        ft.Row(scroll=True, controls=selectColumns),
        save_button,
        file_picker_Button,
        selected_files,
        bar_chart,
    )
ft.app(main)
