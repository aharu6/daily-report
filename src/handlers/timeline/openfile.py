import flet as ft
import pandas as pd
from flet import BoxShape
import re
from handlers.timeline.handlers import Handlers
import json
from handlers.timeline.make_popup import MakePopup
#csvファイル読み込みハンドラ
class Openfile:

    @staticmethod
    def file_picker_result(e:ft.FilePickerResultEvent,page,
                        calender,drawer,draggable_data_for_move,
                        comments,model_times,drag_data,comment,columns,
                        count_dict,phName,custumDrawerAm,custumDrawerPm,
                        phNameList,comment_dict,draggable_data,require_name,
                        require_location,update_location_data,
                        radio_selected_data,date,total_num_am,total_num_pm):
        try:
            csv_file = pd.read_csv(e.files[0].path)
            #csvfileのクリーニング
            y = csv_file["task"]
            csv_file["task_counts"] = y.groupby((y != y.shift()).cumsum()).cumcount()
            z = csv_file["count"]
            csv_file["count_counts"] = z.groupby((z != z.shift()).cumsum()).cumcount()
            #読み込んだファイル内容を元にcolumnへ再転記する
            len_load_data = csv_file.index.size
            for i in range(len_load_data):
                if csv_file.at[i,"task_counts"]>=1 and csv_file.at[i,"count_counts"]:
                        columns[i].content = ft.DragTarget(
                        group="timeline_accepted",
                        content = ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.icons.DOUBLE_ARROW,color="#2D6E7E"),
                                    width=50,
                                    height=50,
                                    border_radius=50,
                                    alignment=ft.alignment.top_center,
                                )
                            ]
                        ),
                        data = {
                            "time":csv_file.at[i,"time"],
                            "num":i,
                            "task":"will_accept"
                        }
                    )

                elif isinstance(csv_file.at[i,"task"],str) and re.search(r'.+', csv_file.at[i,"task"])and csv_file.at[i,"task_counts"]==0:
                    columns[i].content = ft.DragTarget(
                        group="timeline",
                        content = ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.DELETE_OUTLINE,
                                    visible=False,
                                    icon_size=20,
                                    icon_color="red",
                                    on_click = lambda e:Handlers.delete_content(
                                        e=e,
                                        page=page,
                                        drag_data=drag_data,
                                        count_dict=count_dict,
                                        comment_dict=comment_dict,
                                        columns=columns,
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
                                        "time":csv_file.at[i,"time"],
                                        "num":i,
                                        "task":csv_file.at[i,"task"],
                                    },
                                ),
                                ft.Draggable(
                                    group = "timeline",
                                    content = ft.Container(
                                        content = ft.Text(csv_file.at[i,"task"],color = "white"),
                                        width = 50,
                                        height = 130,
                                        bgcolor = Handlers.change_color(csv_file.at[i,"task"]),
                                        border_radius = ft.border_radius.only(top_left = 5,bottom_left = 5),
                                        shape =BoxShape.RECTANGLE,
                                    ),
                                    data = {
                                        "time":csv_file.at[i,"time"],
                                        "num":i,
                                        "task":csv_file.at[i,"task"],
                                    },
                                ),
                                ft.PopupMenuButton(
                                    items = [
                                        MakePopup.add_popup(
                                            time = csv_file.at[i,"time"],update_location_data=update_location_data,
                                            num = i,columns = columns,page=page,
                                            radio_selected_data = radio_selected_data,date=date
                                        ),
                                    ],
                                    icon = ft.icons.MORE_VERT,
                                    tooltip = "編集",
                                    icon_size = 20,
                                    on_open = lambda e:MakePopup.pop_up_reload(
                                        e=e,customDrawerAm =custumDrawerAm,
                                        customDrawerPm = custumDrawerPm,page = page
                                        ),
                                    data={
                                        "time":csv_file.at[i,"time"],
                                    }
                                ),
                                ft.Container(),
                            ],
                            height = 370,
                            spacing = 0,
                            data = {
                                "time":csv_file.at[i,"time"],
                                "num":i,
                                "task":csv_file.at[i,"task"],
                            }
                        ),
                        data = {
                            "time":csv_file.at[i,"time"],
                            "num":i,
                            "task":csv_file.at[i,"task"],
                        }
                    )
                
                    #データ内容に基づくカスタム
                    match csv_file.at[i,"task"]:
                        case "その他":
                            columns[i].content.content.controls.append(comments[i])
                        # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
                        case "混注時間"|"無菌調製関連業務"|"休憩"|"委員会"|"WG活動"|"勉強会参加"|"1on1"|"カンファレンス"|"業務調整"|"will_accept":
                            pass
                        #カウンターの再表示
                        case _:
                            columns[i].content.content.controls.append(Handlers.create_counter(e= csv_file.at[i,"time"],count_dict=count_dict))
                            #カウンターデータの再表示
                            #1以上の場合には表示する
                            if csv_file.at[i,"count"] > 0:
                                columns[i].content.content.controls[4].controls[1].value = csv_file.at[i,"count"]
                        
                #何も文字が入っていないカラムは初期状態へ
                elif pd.isna(csv_file.at[i,"task"]):
                    from handlers.timeline.handdrag_will_accept import Add_will_accept
                    from handlers.timeline.drag_leave import DragLeave
                    columns[i].content = ft.DragTarget(
                        group  = "timeline",
                        content = ft.Container(
                            width=50,
                            height=370,
                            bgcolor = "#CBDCEB",
                            border_radius=5,
                        ),
                        on_accept=lambda e:Handlers.drag_accepted(
                            e = e,
                            page = page,
                            draggable_data=draggable_data,
                            columns=columns,
                            comments=comments,
                            times = model_times,
                            drag_data=drag_data,
                            comment=comment,
                            count_dict=count_dict,
                            phNameList=phNameList,
                            phName=phName,
                            comment_dict=comment_dict,
                            draggable_data_for_move=draggable_data_for_move,
                            customDrawerAm=custumDrawerAm,
                            customDrawerPm=custumDrawerPm
                            ,
                            update_location_data=update_location_data,
                            radio_selected_data=radio_selected_data,
                            date=date,
                        ),
                        on_will_accept=lambda e:DragLeave.drag_leave(e=e,page=page),
                        on_leave=lambda e:DragLeave.drag_leave(e=e,page=page),
                        data = {"time":csv_file.at[i,"time"],"num":i,"task":csv_file.at[i,"task"]},
                    )
                #辞書データの更新
                #delete content で使用する辞書で０たを読み込みデータに合わせて更新する
                #使用辞書:drag_data,comment_dict,count_dict
                drag_data[csv_file.at[i,"time"]] = {"task":csv_file.at[i,"task"]}
                if csv_file.at[i,"comment"] !="NaN":
                    comment_dict[csv_file.at[i,"time"]] = {"comment":csv_file.at[i,"comment"]}            
            #カレンダーの更新
            update_date = csv_file["date"].unique()[0]
            calender.text = update_date
            calender.data = update_date

            #薬剤師名の再表示
            update_phName = csv_file["phName"].unique()[0]
            phName.value = update_phName

            #病棟名の再表示
            #読み込んだcsv_fileにam,pmの区別をつける
            from models.models import DataModel
            am_data = DataModel.amTime(self=None)
            pm_data = DataModel.pmTime(self=None)
            
            # "am_or_pm"列を追加
            csv_file["am_or_pm"] = csv_file["time"].apply(
                lambda x: "AM" if x in am_data else ("PM" if x in pm_data else "")
            )


            #初期化
            for i in range(len(custumDrawerAm.content.controls)):
                custumDrawerAm.content.controls[i].value = False
            for i in range(len(custumDrawerPm.content.controls)):
                custumDrawerPm.content.controls[i].value = False
            #再表示
            am_reload_data = csv_file[csv_file["am_or_pm"] == "AM"]["locate"].unique().tolist()
            am_reload_list = []
            for i in range(len(am_reload_data)):
                dat = am_reload_data[i]
                if dat and dat != '[]':
                    try:
                        if isinstance(dat,str):
                            dat_cleaned = dat.replace("'", '"')
                            split_data = json.loads(dat_cleaned)
                        else:
                            split_data = dat
                        am_reload_list.extend(split_data)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error for data: {dat} - {e}")
                
            pm_reload_data = csv_file[csv_file["am_or_pm"] == "PM"]["locate"].unique().tolist()
            pm_reload_list = []
            for i in range(len(pm_reload_data)):
                dat = pm_reload_data[i]
                if dat and dat != '[]':
                    try:
                        if isinstance(dat,str):
                            dat_cleaned = dat.replace("'", '"')
                            split_data = json.loads(dat_cleaned)
                        else:
                            split_data = dat
                        pm_reload_list.extend(split_data)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error for data: {dat} - {e}")
            #AM 再表示
            am_times = csv_file[csv_file["am_or_pm"] == "AM"]["time"].tolist()
            for i in range(len(am_reload_list)):
                for j in range(len(custumDrawerAm.content.controls)):
                    if custumDrawerAm.content.controls[j].label == am_reload_list[i]:
                        custumDrawerAm.content.controls[j].value = True
                        total_num_am["count"] +=1
                    else:
                        pass
            
            #PM
            pm_times = csv_file[csv_file["am_or_pm"] == "PM"]["time"].tolist()
            for i in range(len(pm_reload_list)):
                for j in range(len(custumDrawerPm.content.controls)):
                    if custumDrawerPm.content.controls[j].label == pm_reload_list[i]:
                        custumDrawerPm.content.controls[j].value = True
                        total_num_pm["count"] +=1
                    else:
                        pass

            #名前を入力してくださいの表示は消す
            require_name.visible = False

            #病棟を選択してくださいの表示は消す
            if total_num_am["count"] >0 and total_num_pm["count"] >0:
                #am
                require_location.content.controls[1].title.color = "green"
                require_location.content.controls[1].leading = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE,color="green")
                require_location.content.controls[1].data = "true"
                require_location.content.controls[1].visible =False
                #pm
                require_location.content.controls[2].title.color = "green"
                require_location.content.controls[2].leading = ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE,color="green")
                require_location.content.controls[2].data = "true"
                require_location.content.controls[2].visible =False

                #病棟を選択してくださいの表示は消す
                require_location.content.controls[0].visible =False

            elif total_num_am["count"] ==0:
                #am
                require_location.content.controls[1].title.color = "red"
                require_location.content.controls[1].leading = ft.Icon(ft.icons.HIGHLIGHT_OFF,color="red")
                require_location.content.controls[1].data = "false"
                require_location.content.controls[0].visible =True
                require_location.content.controls[2].visible =True
                #amの表示のみ消す
                require_location.content.controls[1].visible =False
            elif total_num_pm["count"] ==0:
                #pm
                require_location.content.controls[2].title.color = "red"
                require_location.content.controls[2].leading = ft.Icon(ft.icons.HIGHLIGHT_OFF,color="red")
                require_location.content.controls[2].data = "false"
                require_location.content.controls[0].visible =True
                require_location.content.controls[1].visible =True
                #pmの表示のみ消す
                require_location.content.controls[2].visible =False
            
            page.update()
            
        except Exception as ex:
            print(f"Error reading CSV file: {ex}")
            import traceback
            traceback.print_exc()