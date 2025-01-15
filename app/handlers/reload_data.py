import json
import flet as ft

#ドロワーを展開する
#保管しているデータを取得して表示する
#右側にtimeline適用用のボタンを合わせて表示する
class ReloadDataHandler:
    @staticmethod
    def toggle_Reload_Data(e,page,drawer,columns):
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
                    on_click = lambda e:ReloadDataHandler.open_saved_data(e,page,columns,dat),
                    data = i
                    ),
                data = i,
                ))            
        page.update()
        
    #保存したデータを開いてcolumnに再転記する
    @staticmethod
    def open_saved_data(e,page,columns,dat):
        #columns = self.columns
        #選択したkeyに該当するデータを取り出す
        selected_key = e.control.data
        load_data = dat[selected_key]
        print(load_data)
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
        
        pass