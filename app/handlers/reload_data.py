import json
import flet as ft
from models.models import DataModel

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
        #delete_buttons,
        draggable_data_for_move,
        comments,
        model_times,
        drag_data,
        comment,
        count_dict,
        phName,
        custumDrawerAm,
        custumDrawerPm,
        phNameList,
        comment_dict,
        draggable_data,
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
                        #delete_buttons,
                        draggable_data_for_move,
                        comments,
                        model_times,
                        drag_data,
                        comment,
                        count_dict,
                        phName,
                        custumDrawerAm,
                        custumDrawerPm,
                        phNameList,
                        comment_dict,
                        draggable_data,
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
        #delete_buttons,
        draggable_data_for_move,
        comments,
        model_times,
        drag_data,
        comment,
        count_dict,
        phName,
        custumDrawerAm,
        custumDrawerPm,
        phNameList,
        comment_dict,
        draggable_data,
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
        
        #load dataを編集　最初のtask名は残して、2番目以降はwill_accept
        #willacceptの時は矢印ボタンだけを表示する もしくは続く間はwhileにて継続する
        # matchにて分岐する？
        #前のコンテンツが残っていて、追加される形式となっているので全てクリアしてから追加する
        
        from handlers.handlers import Handlers
        from handlers.timeline.delete_content_reload import DeleteContentReloadHandler
        import re
        for i in range(len_load_data):
            #taskがあれば基づいてcolumns内容を更新するが、will_acceptの場合には矢印ボタンだけを表示する
            key = list(load_data.keys())[i]
            if load_data[key]["task"] ==  "will_accept":
                columns[i].content  = ft.Column(
                    controls = [
                        ft.Container(
                            content = ft.Icon(ft.icons.DOUBLE_ARROW,color = "#2D6E7E"),
                            width = 50,
                            height = 50,
                            border_radius = 50,
                        ),
                    ],
                    data = {
                        "time": load_data[key]["time"],
                        "num": i,
                        "task": load_data[key]["task"],
                    }
                )
                
            elif re.search(r'.+',load_data[key]["task"]):
                #DragTargetにて元のと揃えた方がいい
                columns[i].content = ft.DragTarget(
                    group  = "timeline_accepted",
                    content=ft.Column(
                        controls = [
                            ft.IconButton(
                                icon=ft.icons.DELETE_OUTLINE,
                                visible=False,
                                icon_size=20,
                                icon_color="red",
                                on_click=lambda e: Handlers.delete_content(
                                    e=e,
                                    page=page,
                                    drag_data=drag_data,
                                    count_dict=count_dict,
                                    comment_dict=comment_dict,
                                    columns=columns,
                                    comments=comments,
                                    times=model_times,
                                    draggable_data=draggable_data,
                                    comment=comment,
                                    phNameList=phNameList,
                                    phName=phName,
                                    draggable_data_for_move=draggable_data_for_move,
                                ),
                                data = {
                                    "time": load_data[key]["time"],
                                    "num":i,
                                    "task":load_data[key]["task"],
                                    }
                            ),   
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
                    ),
                    data = {
                        "time":load_data[key]["time"],
                        "num":i,
                        "task":load_data[key]["task"],
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
                        #columns
                        columns[i].content.content.controls.append(comments[i])
                    # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
                    case (
                        "混注時間",
                        "休憩",
                        "委員会",
                        "WG活動",
                        "勉強会参加",
                        "1on1",
                        "カンファレンス",
                        "will_accept",
                    ):
                        pass
                    #カウンターの再表示
                    case _:
                        columns[i].content.content.controls.append(Handlers.create_counter(load_data[key]["time"],count_dict))
                        #カウンターデータの再表示
                        #１以上の場合には表示する
                        if load_data[key]["count"] >0:
                            columns[i].content.content.controls[2].controls[1].value = load_data[key]["count"]
                #コメント記載がある場合には内容更新もできる？
                
            #辞書データの更新
            #delete contentで使用する辞書データを読み込みデータに合わせて更新する
            #使用辞書：drag_data,comment_dict,count_dict
            drag_data[load_data[key]["time"]] = {"task":load_data[key]["task"]}
            if load_data[key]["comment"]!= "":
                comment_dict[load_data[key]["time"]] = {"comment":comment}

        #カレンダーの更新
        #適応に最初のkey
        key_for_reload = list(load_data.keys())[0]
        update_date = load_data[key_for_reload]["date"]
        calender.text = update_date
        calender.data = update_date 
        
        #薬剤師名の再表示
        update_phName = load_data[key_for_reload]["phName"] 
        phName.value = update_phName
        
        #病棟名の再表示
        #56のうち、columns[0] == am,columns[56] == pmのデータを取り出す
        key_for_first = list(load_data.keys())[0]
        key_for_last = list(load_data.keys())[-1]
        am_data = load_data[key_for_first]["locate"]
        pm_data = load_data[key_for_last]["locate"]
        for j in range(len(am_data)):            
            for i in range(len(custumDrawerAm.content.controls)):
                if custumDrawerAm.content.controls[i].label == am_data[j]:
                    custumDrawerAm.content.controls[i].value = True
                else:
                    pass
        
        for j in range(len(pm_data)):
            for i in range(len(custumDrawerPm.content.controls)):
                if custumDrawerPm.content.controls[i].label == pm_data[j]:
                    custumDrawerPm.content.controls[i].value = True
                else:
                    pass
                
        page.update()
        
        #カラムのgroupを受け取り後の状態に