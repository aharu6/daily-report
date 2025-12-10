import flet as ft
from flet import BoxShape
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
        require_name,
        require_location,
        update_location_data,
        radio_selected_data,
        date,
        total_num_am,
        total_num_pm,
        ):
        import json
        page.open(drawer)
        #保存しているデータを読み出す
        #write csv時の保存名：timeline_data
        try:
            load_data = page.client_storage.get("timeline_data")
        except:
            load_data = {}
        try:
            dat = json.loads(load_data)
        except:
            dat = {}
        #save_data = {"date_phName":dict_data}
        #日付と名前それぞれのデータを取り出す
        #ドロワーには保管されている　key = date_phNameにて表示
        #編集ボタンを追加して、押すと再編集できるように
        
        #date_phName のデータを取り出す
        key = list(dat.keys())
        #keyに基づいてドロワーを作成 reloadDrawer   controls
        #drawer.controls.append(ft.Card(content = ft.Column()))
        drawer.controls[1].content.controls = []
        for i in key:
            drawer.controls[1].content.controls.append(ft.ListTile(
                title = ft.Text(i),
                trailing = ft.IconButton(
                    ft.icons.EDIT_SQUARE, 
                    on_click = lambda e:ReloadDataHandler.open_saved_data(
                        e=e,
                        page=page,
                        calender=calender,
                        columns=columns,
                        dat=dat,
                        #delete_buttons,
                        draggable_data_for_move=draggable_data_for_move,
                        comments=comments,
                        model_times=model_times,
                        drag_data = drag_data,
                        comment=comment,
                        count_dict=count_dict,
                        phName=phName,
                        custumDrawerAm=custumDrawerAm,
                        custumDrawerPm=custumDrawerPm,
                        phNameList=phNameList,
                        comment_dict=comment_dict,
                        draggable_data=draggable_data,
                        require_name=require_name,
                        require_location=require_location,
                        update_location_data=update_location_data,
                        radio_selected_data=radio_selected_data,
                        date=date,
                        total_num_am=total_num_am,
                        total_num_pm=total_num_pm,
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
        require_name,
        require_location,
        update_location_data,
        radio_selected_data,
        date,
        total_num_am,
        total_num_pm,
        ):
        
        #業務調整デフォルト入力オンオフも反映する
        
        #columns = self.columns
        #選択したkeyに該当するデータを取り出す
        selected_key = e.control.data
        load_data = dat[selected_key]
        #取り出したデータの長さに従ってcolumns[0] = data[0] の辞書データにてcontentsを更新していく
        
        len_load_data = len(list(load_data.keys()) ) 
        
        #load dataを編集　最初のtask名は残して、2番目以降はwill_accept
        #willacceptの時は矢印ボタンだけを表示する もしくは続く間はwhileにて継続する
        # matchにて分岐する？
        #前のコンテンツが残っていて、追加される形式となっているので全てクリアしてから追加する
        
        from handlers.timeline.handlers import Handlers
        import re
        import json
        from handlers.timeline.make_popup import MakePopup
        for i in range(len_load_data):
            #taskがあれば基づいてcolumns内容を更新するが、will_acceptの場合には矢印ボタンだけを表示する
            key = list(load_data.keys())[i]
            if load_data[key]["task"] ==  "will_accept":
                columns[i].content  = ft.DragTarget(
                    group ="timeline_accepted", 
                    content=ft.Column(
                        controls = [
                            ft.Container(
                                content = ft.Icon(ft.icons.DOUBLE_ARROW,color = "#2D6E7E"),
                                width = 50,
                                height = 50,
                                border_radius = 50,
                            ),
                        ],
                        
                    ),
                    data={
                            "time": load_data[key]["time"],
                            "num": i,
                            "task": load_data[key]["task"],
                        }
                )
                
            elif re.search(r'.+',load_data[key]["task"]):
                #DragTargetにて元のと揃えた方がいい
                columns[i].content = ft.DragTarget(
                    group  = "timeline",
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
                                    update_location_data=update_location_data,
                                    customDrawerAm=custumDrawerAm,
                                    customDrawerPm=custumDrawerPm,
                                    radio_selected_data=radio_selected_data,
                                    date=date,
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
                                    height = 130,
                                    bgcolor = Handlers.change_color(load_data[key]["task"]),
                                    border_radius=ft.border_radius.only(top_left = 5,bottom_left=5),
                                    shape=BoxShape.RECTANGLE,
                                ),
                                data = {
                                    "time": load_data[key]["time"],
                                    "num": i,
                                    "task": load_data[key]["task"],
                                },
                            ),
                            ft.PopupMenuButton(
                                items = [
                                    MakePopup.add_popup(
                                        time = load_data[key]["time"],update_location_data=update_location_data,
                                        num = i,columns = columns,page = page,
                                        radio_selected_data=radio_selected_data,
                                        date=date
                                        ), 
                                    ],
                                icon = ft.icons.MORE_VERT,
                                tooltip = "編集",
                                icon_size = 20,
                                on_open = lambda e:MakePopup.pop_up_reload(e=e,customDrawerAm=custumDrawerAm,customDrawerPm=custumDrawerPm,page=page),
                                data = {
                                    "time": load_data[key]["time"]
                                }
                            ),
                            ft.Container(),
                        ],
                        height = 370,
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
                if load_data[key]["task"]:
                    print(load_data[key]["task"])
                match load_data[key]["task"]:
                    case "その他":
                        #columns
                        columns[i].content.content.controls.append(comments[i])
                        
                    # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
                    case "混注時間"|"無菌調製関連業務"|"休憩"|"委員会"|"WG活動"|"勉強会参加"|"1on1"|"カンファレンス"|"will_accept":
                        pass
                    #カウンターの再表示
                    case _:
                        columns[i].content.content.controls.append(Handlers.create_counter(load_data[key]["time"],count_dict))
                        #カウンターデータの再表示
                        #１以上の場合には表示する
                        if load_data[key]["count"] >0:
                            columns[i].content.content.controls[4].controls[1].value = load_data[key]["count"]
                            print("counterreload")
                
                #radiobuttonでの選択内容は別データにて保管し、ある場合には再表示
                #何も文字が入っていないカラムは初期状態へ
            elif load_data[key]["task"] == "":
                from handlers.timeline.handdrag_will_accept import Add_will_accept
                from handlers.timeline.drag_leave import DragLeave
                columns[i].content = ft.DragTarget(
                    group="timeline",
                    content=ft.Container(
                        width=50,
                        height=370,
                        bgcolor="#CBDCEB",
                        border_radius=5,
                    ),
                    on_accept=lambda e:Handlers.drag_accepted(
                        e=e,
                        page=page,
                        draggable_data=draggable_data,
                        columns=columns,
                        comments=comments,
                        times=model_times,
                        drag_data=drag_data,
                        comment=comment,
                        count_dict=count_dict,
                        phNameList=phNameList,
                        phName=phName,
                        comment_dict=comment_dict,
                        draggable_data_for_move=draggable_data_for_move,
                        customDrawerAm=custumDrawerAm,
                        customDrawerPm=custumDrawerPm,
                        update_location_data=update_location_data,
                        radio_selected_data=radio_selected_data,
                        date=date,
                    ),
                    on_will_accept=lambda e:Add_will_accept.drag_will_accept(
                        e=e,
                        page=page,
                        columns=columns,
                        drag_data=drag_data,
                        
                    ),
                    on_leave=lambda e:DragLeave.drag_leave(e=e,page=page),
                    data={"time":load_data[key]["time"],"num":i,"task":load_data[key]["task"]},
                )
                #コメント記載がある場合には内容更新もできる？
                
            #辞書データの更新
            #delete contentで使用する辞書データを読み込みデータに合わせて更新する
            #使用辞書：drag_data,comment_dict,count_dict
            drag_data[load_data[key]["time"]] = {"task":load_data[key]["task"]}
            if load_data[key]["comment"]!= "":
                comment_dict[load_data[key]["time"]] = {"comment":load_data[key]["comment"]}
                print(comment_dict)

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
        #writeにてlocateデータば辞書データと別に保管しておく
        
        load_location_data = json.loads(page.client_storage.get("location_data"))
        #name_dateにて紐づける中から取り出す
        key=f"{update_date}_{update_phName}"
        am_data = load_location_data[key]["locate_AM"]
        pm_data = load_location_data[key]["locate_PM"]
        #初期化
        for i in range(len(custumDrawerAm.content.controls)):
            custumDrawerAm.content.controls[i].value = False
        for i in range(len(custumDrawerPm.content.controls)):
            custumDrawerPm.content.controls[i].value = False
        #再表示
        for j in range(len(am_data)):            
            for i in range(len(custumDrawerAm.content.controls)):
                if custumDrawerAm.content.controls[i].label == am_data[j]:
                    custumDrawerAm.content.controls[i].value = True
                    total_num_am["count"]+=1
                else:
                    pass
        
        for j in range(len(pm_data)):
            for i in range(len(custumDrawerPm.content.controls)):
                if custumDrawerPm.content.controls[i].label == pm_data[j]:
                    custumDrawerPm.content.controls[i].value = True
                    total_num_pm["count"]+=1
                else:
                    pass
        
        #病棟単数選択（radiobutton）での再表示
        load_radio_data=json.loads(page.client_storage.get("radio_selected_data"))
        #name_dataにて紐づける中から取り出す
        radio_data=load_radio_data[key]
        #numdataもほしいかも
        for time_key,data in radio_data.items():
            column_num=data["num"]
            columns[column_num].content.content.controls[3].content=ft.Text(data["radio_select"])
        #名前を入力してくださいの表示は消す
        require_name.visible = False

        #病棟を選択してくださいの表示は消す
        if total_num_am["count"]>0:
            require_location.content.controls[1].title.color="green"
            require_location.content.controls[1].leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color="green")
            require_location.content.controls[1].data="true"
        elif total_num_am["count"]==0:
            require_location.content.controls[1].title.color="red"
            require_location.content.controls[1].leading=ft.Icon(ft.icons.HIGHLIGHT_OFF, color="red")
            require_location.content.controls[1].data="false"
            require_location.content.controls[0].visible =True
            require_location.content.controls[2].visible =True
        
        if total_num_am["count"]>0:
            require_location.content.controls[2].title.color="green"
            require_location.content.controls[2].leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color="green")
            require_location.content.controls[2].data="true"
        elif total_num_am["count"]==0:
            require_location.content.controls[2].title.color="red"
            require_location.content.controls[2].leading=ft.Icon(ft.icons.HIGHLIGHT_OFF, color="red")
            require_location.content.controls[2].data="false"
            require_location.content.controls[0].visible =True
            require_location.content.controls[1].visible =True

        if require_location.content.controls[1].data=="true" and require_location.content.controls[2].data=="true":
            require_location.content.controls[0].visible =False
            require_location.content.controls[1].visible =False
            require_location.content.controls[2].visible =False

                

        page.update()
        
        #カラムのgroupを受け取り後の状態に