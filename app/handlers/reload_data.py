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
        drawer,
        columns,
        delete_buttons,
        draggable_data_for_move,
        comments,
        model_times,
        drag_data,
        comment,
        count_dict,
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
                        columns,
                        dat,
                        delete_buttons,
                        draggable_data_for_move,
                        comments,
                        model_times,
                        drag_data,
                        comment,
                        count_dict,
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
        columns,
        dat,
        delete_buttons,
        draggable_data_for_move,
        comments,
        model_times,
        drag_data,
        comment,
        count_dict,
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
        print(len_load_data)    
        
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
        page.update()