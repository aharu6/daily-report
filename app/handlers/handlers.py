import json
import datetime
import flet as ft
import csv
import pandas as pd
from models.models import DataModel
class Handlers:
    @staticmethod
    def handle_change(e,today,Date):
        selected_date = e.control.value #例えば2021-01-01のような形式
        
        #文字列を日付オブジェクトに変換
        today = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        
        #年月日を取得して表示用のテキストに変換
        Date.text = f"{today.year}/{today.month}/{today.day}"
        Date.update()
    
    @staticmethod
    def dropdown_changed(e,phName,dialog,page):
        if phName.value == "Add": 
            dialog.open = True
            page.update()
        else:
            page.update()
            
    @staticmethod
    def update_dropdown(phName,phNameList,page):  
        try:
            options = [ft.dropdown.Option(item["name"]) for item in phNameList]
        except:
            options =[]
        options.append(ft.dropdown.Option("Add"))
        
        phName.options = options
        page.update()
        
    @staticmethod
    def drawer_open(e,page,endDrawer):
        page.open(endDrawer)
        
    @staticmethod
    def delete_name(e,phNameList,page):
        new_phNameList = phNameList.remove(e.control.data)
        page.client_storage.set("phName",json.dumps(new_phNameList,ensure_ascli = False))
        page.update()
        
    @staticmethod
    def change_choice_button(e,selectColumns,page):
        #0 病棟担当者
        if int(e.data) ==0:
            selectColumns[2].visible = True
            page.update()
        #1 DI担当者
            #非表示にするもの：混注時間
            #薬剤セット数
        elif int(e.data) ==1:
            selectColumns[2].visible = False
            page.update()
            
        #2 主任/副主任
        elif int(e.data) ==2:
            selectColumns[2].visible = True
            page.update()
            
    @staticmethod
    def change_special_choice(e,selectColumns,page):
        #0 AST
            #表示にするもの：ICT/AST
            #非表示にするもの：褥瘡、TPN評価
        if int(e.data) == 0:
            selectColumns[16].visible = True #ICT/AST
            selectColumns[17].visible = False #褥瘡
            selectColumns[18].visible = False #TPN評価
            page.update()
        #1 NST
            #表示にするもの：褥瘡、TPN評価
            #非表示にするもの：ICT/AST
        elif int(e.data) == 1:
            selectColumns[16].visible = False #ICT/AST
            selectColumns[17].visible = True #褥瘡
            selectColumns[18].visible = True #TPN評価
            page.update()
        #2 off
            #ICT/NST,褥瘡、TPN評価全て非表示
        elif int(e.data) == 2:
            selectColumns[16].visible = False #ICT/AST
            selectColumns[17].visible = False #褥瘡
            selectColumns[18].visible = False #TPN評価
            page.update()
        else:
            print("updatenone")
    
    @staticmethod
    def toggle_delete_button(page,delete_buttons):
        for button in delete_buttons:
            button.visible = not button.visible
        page.update()
        
    @staticmethod
    def delete_content(
        e,page,phNameList,phName,delete_buttons,drag_data,
        count_dict,comment_dict,columns
        ):
        #_move関数でdelete_button.dataに入れたのはdragtargetで設定したカラムの番号
        #columns[i]でそのカラムの情報を取得し、見た目上削除
        #正しくはcolumnsの初期化を行う。ドラッグする前の状態に戻す
        col_num = delete_buttons[e.control.data["num"]].data["num"]
        print(col_num)
        #同じ情報の新しいカラムに差し替える
        columns[col_num].content = ft.DragTarget(
            group = "timeline",
            content = ft.Container(
                width = 50,
                height = 300,
                bgcolor = None,
                border_radius = 5,
            ),
            on_accept = Handlers.drag_accepted(e),
            on_move = Handlers.drag_move,
            data = {"time":DataModel().times()[col_num],"num":col_num}
        )
        columns[col_num].update()
        
        #同時に該当するdrag_dataのデータも削除する
        del drag_data[DataModel().times()[col_num]]
        print(DataModel().times()[col_num])
        #該当のカウントデータも削除する
        if DataModel().times[col_num] in count_dict:
            del comment_dict[DataModel.times()[col_num]]
        #該当のその他のデータも削除する
        if DataModel().times[col_num] in comment_dict:
            del comment_dict[DataModel().times()[col_num]]
            
    #カウンターの関数
    @staticmethod
    def counterPlus(e,count_field,count_dict,time):
        print(e)
        old_Count = int(count_field.value)
        new_Count = old_Count + 1
        #更新した値にてカウンター内を更新
        count_field.value = new_Count
        count_field.update()
        #dict内の値を更新
        count_dict[time]["count"] =new_Count
        print(count_dict)
    
    @staticmethod
    def counterMinus(e,count_field,count_dict,time):
        # +と同様
        old_Count = int(count_field.value)
        new_Count = old_Count - 1
        # update counter value
        count_field.value = new_Count
        count_field.update()
        #dict内の値を更新
        print(e.control.data)
        count_dict[time]["count"] =new_Count
        
    @staticmethod
    def create_counter(e,count_dict):
        #eは入力したカラムの時間を取得
        #初期は０
        count = 0
        time = e
        count_field = ft.TextField(
            count,
            width =40,
            text_align = ft.TextAlign.CENTER,
            text_size = 10,
            border_color = None,
        )
        count_dict[e] = {"count":count}
        return ft.Column(
            [
                ft.IconButton(
                    ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size = 25,
                    on_click = lambda e: Handlers.counterPlus(e,count_field,count_dict,time),
                    style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                count_field,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: Handlers.counterMinus(e, count_field,count_dict,time),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
            ]
        )
    
    @staticmethod
    def dlg_close(e,dlg,page):
        dlg.open = False
        page.update()
    
    @staticmethod
    def create_dialog_for_comment(e,comments,dlg,comment_dict,comment_field,page):
        comment_time = comments[e.control.data["num"]].data["time"]
        comment_num = comments[e.control.data["num"]].data["num"]
        dlg.data = {"time":comment_time,"num":comment_num}
        #TextFiledの初期化
        if comment_time in comment_dict:
            comment_field.value = comment_dict[comment_time]["comment"]
        else:
            comment_field.value = ""
        page.open(dlg)
    
    @staticmethod
    def dlg_open(e,dlg):
        dlg.visible = True
        
    @staticmethod
    def add_name(e,phNameList,name_field,page,phName,dialog):
        new_name = name_field.value.strip()
        phName_List = phNameList
        print("phnamelist",phNameList)
        if new_name :
            phName_List.append({"name":new_name})
            page.client_storage.set("phName",phName_List)
            print()
            name_field.value = ""
            Handlers.update_dropdown(phName,phName_List,page)
            dialog.open = False
            page.update()
            
    @staticmethod
    def add_comment_for_dict(e,dlg,comment_dict,comment_field,page):
        comment_time = dlg.data["time"]
        comment_num = dlg.data["num"]
        if comment_time in comment_dict:
            del comment_dict[comment_time]
            comment_dict[comment_time] = {"comment":comment_field.value}
        else:
            comment_dict[comment_time] = {"comment":comment_field.value}
            
        dlg.open = False
        page.update()
    
    @staticmethod
    def drag_move(e,page,draggable_data,delete_buttons,columns,comments,times,drag_data,comment,count_dict):
        print(e.src_id)
        if page.get_control(e.src_id):
            src = page.get_control(e.src_id)
            try:
                key = src.data["task"]["task"]
            except:
                key = src.data["task"]            
        else:
            key = draggable_data[e.src_id]["task"]
        
        e.control.content = ft.Column(
            controls = [
                delete_buttons[e.control.data["num"]],
                ft.Draggable(
                    group = "timeline",
                    content = ft.Container(
                        content = ft.Text(key,color = "white"),
                        width = 50,
                        height = 140,
                        bgcolor = ft.colors.BLUE_GREY_500,
                    ),
                    data = {"time":e.control.data["time"],"num":e.control.data["num"],"task":key},
                ),
            ],
            height = 300,
            spacing = 0,
            data = {"time":e.control.data["time"],"num":e.control.data["num"],"task":key},
        )
        #ドラッグ時にコンテンツを更新する用
        columns[e.control.data["num"]].content.data["task"] = key
        print("columns",columns[e.control.data["num"]].content.data["task"],e.src_id,"src_id")
        #moveにて新規src_idが追加された場合、その情報をdrag_dataに追加
        #elseに向けて辞書データを更新しておく
        draggable_data[e.src_id] = {"task":key}
        #delete_buttonsに渡すdata
        delete_buttons[e.control.data["num"]].data = {"num":e.control.data["num"]}
        e.control.update()
        left_column_num = e.control.data["num"] - 1
        #left_keyの初期化
        left_key = None
        try:
            left_key = columns[left_column_num].content.data["task"]
        except:
            pass
        
        match key:
            # key==その他の場合にはコメントボタンを追加する
            case "その他":
                #すでに左のカラムにコンテンツがある場合にはコメントボタンは作成しない
                e.control.content.controls.append(comments[e.control.data["num"]])
            #混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
            case "混注時間"|"休憩"|"委員会"|"WG活動"|"勉強会参加"|"1on1"|"カンファレンス":
                pass
            #その他の場合にはカウンターを表示する 
            #左カラムに同じデータはある場合にはカウンターは作成しない
            case _:
                if left_key == key:
                    pass
                else:
                    e.control.content.controls.append(Handlers.create_counter(e.control.data["time"],count_dict))
        e.control.update()
        
        #現在のカラムの番号はnum = e.control.data["num"]
        #左のカラム　num -1 のカラムの情報を取得
        #一番左のカラムだけ表示、後は非表示にする（カウンターはそもそも作成しない）
        try:
            if left_key == key:
                e.control.content.controls[1].content.content.visible = False
                e.control.content.update()
        except:
            pass
        
        
        #左ではなくて、現在のカラム番号と左のカラム番号を比較する
        #右のカラムも比較して、同じ業務内容の場合、右は非表示に
        #左のみ残して表示する
        right_column_num = e.control.data["num"] + 1
        try:
            right_key = columns[right_column_num].data["task"]
        except:
            pass
        try:
            if right_key == key:
                columns[right_column_num].content = ft.Column(
                    controls = [
                        delete_buttons[right_column_num],
                        ft.Draggable(
                            group = "timeline",
                            content = ft.Container(
                                width = 50,
                                height = 140,
                                bgcolor = ft.colors.BLUE_GREY_500,
                            ),
                        ),
                    ],
                    height = 300,
                    spacing = 0,
                    data = {"time":times[right_column_num],"num":right_column_num,"task":key},
                )
                columns[right_column_num].update()
        except:
            pass
        #ドラッグデータの保存
        drag_data[e.control.data["time"]] = {'task':key}
        if comment:
            comments[e.control.data["num"]].data = {"time":e.control.data["time"],"num":e.control.data["num"]}  
            
    @staticmethod
    def drag_accepted(e):
        data = e.data
        
    @staticmethod
    def write_csv_file(e,times,amTime,today,columns,drag_data,count_dict,amDropDown,pmDropDown,phName,page,comment_dict,select_directory):
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
            
        list_pm_location_data = []
        for time in data_dict.keys():
            if list_pm_location_data is not None:
                if data_dict[time]["locate"] == "PM":
                    data_dict[time]["locate"] = list_pm_location_data
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
                data_dict[time]["comment"] = comment_data["comment"]
            
        #csvファイルの書き込み  
        if select_directory.result and select_directory.result.path:
            file_path = select_directory.result.path + f"/{today}.csv"
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Task", "Count", "locate", "date","PhName","Comment"])
                for time, record in data_dict.items():
                    writer.writerow([record["time"], record["task"], record["count"], record["locate"], record["date"],record["phName"],record["comment"]])
                    
        ###Chart###########################################################################
        
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
                