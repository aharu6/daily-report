import json
import flet as ft

#ドロワーを展開する
#保管しているデータを取得して表示する
#右側にtimeline適用用のボタンを合わせて表示する
class ReloadDataHandler:
    @staticmethod
    def toggle_Reload_Data(
        e,
        page,
        calender,
        drawer,
        columns,
        delete_buttons,
        draggable_data_for_move,
        comments,
        model_times,
        drag_data,
        comment,
        count_dict,
        phName,
        ):
        page.open(drawer)
        #保存しているデータを読み出す
        #write csv時の保存名：timeline_data
        load_data = page.client_storage.get("timeline_data")
        dat = json.loads(load_data)
        #save_data = {"date_phName":dict_data}
        #日付と名前それぞれのデータを取り出す
        #ドロワーには保管されている　key = date_phNameにて表示
        #編集ボタンを追加して、押すと再編集できるように
        
        #date_phName のデータを取り出す
        key = list(dat.keys())
        #keyに基づいてドロワーを作成 reloadDrawer   controls
        drawer.controls.append(ft.Card(content = ft.Column()))
        for i in key:
            drawer.controls[1].content.controls.append(ft.ListTile(
                title = ft.Text(i),
                trailing = ft.IconButton(
                    ft.icons.EDIT_SQUARE, 
                    on_click = lambda e:ReloadDataHandler.open_saved_data(
                        e,
                        page,
                        calender,
                        columns,
                        dat,
                        delete_buttons,
                        draggable_data_for_move,
                        comments,
                        model_times,
                        drag_data,
                        comment,
                        count_dict,
                        phName,
                        ),
                    data = i
                    ),
                data = i,
                ))            
        page.update()
        
    #保存したデータを開いてcolumnに再転記する
    @staticmethod
    def open_saved_data(
        e,
        page,
        calender,
        columns,
        dat,
        delete_buttons,
        draggable_data_for_move,
        comments,
        model_times,
        drag_data,
        comment,
        count_dict,
        phName,
        ):
        #columns = self.columns
        #選択したkeyに該当するデータを取り出す
        selected_key = e.control.data
        load_data = dat[selected_key]
        #取り出したデータの長さに従ってcolumns[0] = data[0] の辞書データにてcontentsを更新していく
        """
        columns.contentのメモ
        columns.content  = ft.Column(
            controls=[
                delete_buttons[e.control.data["num"]],
                ft.Draggable(
                    group="timeline",
                    content=ft.Container(
                        content=ft.Text(key, color="white"),
                        width=50,
                        height=140,
                        bgcolor=Handlers.change_color(key),
                    ),
                    data={
                        "time": e.control.data["time"],
                        "num": e.control.data["num"],
                        "task": key,
                    },
                ),
            ],
            height=300,
            spacing=0,
            data={
                "time": e.control.data["time"],
                "num": e.control.data["num"],
                "task": key,
            },
        )
        """
        len_load_data = len(list(load_data.keys()) ) 
        
        from handlers.handlers import Handlers
        for i in range(len_load_data):
            #keyがあれば基づいてcolumns内容を更新するが、ない場合には元々のDraggable状態を保持する
            key = list(load_data.keys())[i]
            if load_data[key]["task"] != "":
                columns[i].content = ft.Column(
                    controls  = [
                        delete_buttons[i],   
                        ft.Draggable(
                            group = "timeline",
                            content = ft.Container(
                                content = ft.Text(load_data[key]["task"],color = "white"),
                                width = 50,
                                height = 140,
                                bgcolor = Handlers.change_color(load_data[key]["task"]),
                            ),
                            data = {
                                "time": load_data[key]["time"],
                                "num": i,
                                "task": load_data[key]["task"],
                            },
                        ),
                    ],
                    height = 300,
                    spacing = 0,
                    data = {
                        "time": load_data[key]["time"],
                        "num": i,
                        "task": load_data[key]["task"],
                    }
                )
                
                #カウンターデータ0のときには何も表示されない
                #一番左のカラムだけは0でもカウンターが必要になるから、1以上の指定ではなくて、 key の比較
                # move関数とaccepted関数と同じように左のカラムkeyと比較して表示する　update前だからcolumnsに保管されているkeyは使えない
                #load_dataのうち、最初にkeyが出てきた辞書データを取り出してnum countsを取得、更新する
                
                #カウンター内の値も保存データに基づいて更新
                
                #コメントがある場合にはコメントボタンを追加
                match load_data[key]["task"]:
                    case "その他":
                        columns[i].content.contorls.append(comments[i])
                    # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
                    case (
                        "混注時間",
                        "休憩",
                        "委員会",
                        "WG活動",
                        "勉強会参加",
                        "1on1",
                        "カンファレンス",
                    ):
                        pass
                
                #コメント記載がある場合には内容更新もできる？
            else:
                #元々のDraggable状態を保持する
                columns[i].content = ft.DragTarget(
                    group="timeline",
                    content=ft.Container(
                        width=50,
                        height=300,
                        bgcolor="#CBDCEB",
                        border_radius=5,
                    ),
                    on_accept=lambda e: Handlers.drag_accepted(
                        e,
                        page,
                        draggable_data_for_move,
                        delete_buttons,
                        columns,
                        comments,
                        model_times,
                        drag_data,
                        comment,
                        count_dict,
                    ),
                    data={"time": model_times[i], "num": i, "task": ""},
                )
                
        #カレンダーの更新
        #適応に最初のkey
        key_for_reload = list(load_data.keys())[0]
        update_date = load_data[key_for_reload]["date"]
        calender.text = update_date
        calender.data = update_date 
        
        #薬剤師名の再表示
        update_phName = load_data[key_for_reload]["phName"] 
        phName.value = update_phName
        page.update() #updateしてからカウンターの追加
        
        #columnsにてループする
        for i in range(len_load_data):
            try:
                key = list(load_data.keys())[i]
                left_key = (list(load_data.keys()))[i-1]
                #カウンターの追加
                #左のカラムと同じkey の場合にはカウンターを追加しない
                #カウンターを追加する必要のない業務には追加しない
                current_key = load_data[key]["task"]
                left_key = load_data[left_key]["task"]
                
                if current_key == left_key:
                    pass
                else:
                    #カウンターを追加する必要のない業務には追加しない
                    match key:
                        case  (
                            "混注時間"
                            | "休憩"
                            | "委員会"
                            | "WG活動"
                            | "勉強会参加"
                            | "1on1"
                            | "カンファレンス"
                            |"13:15業務調整"
                        ):
                            pass
                        case _:
                            columns[i].content.controls.append(Handlers.create_counter(load_data[key]["time"],count_dict))
            except:
                pass   
            
        page.update()
        
        #カウンターデータが1以上ある場合には値に応じてカウンターの値を更新する
        #カウンターデータが0のときには0のまま
        for i in range(len_load_data):
            key = list(load_data.keys())[i]
            if load_data[key]["count"] > 0:
                columns[i].content.controls[2].controls[1].value = load_data[key]["count"]
        
        
        page.update()