import flet as ft
from handlers.timeline.handlers import Handlers
from models.models import DataModel
from handlers.timeline.make_popup import MakePopup
from handlers.setting.reload_set_data import DEFAULT_TASK_TIME

#settingoageの設定に基づいてデフォルトで業務を登録する
class Set_Default_task:
    @staticmethod
    def set_default_task(
        page,
        columns,
        phNameList,
        phName,
        drag_data,
        count_dict,
        comment_dict,
        draggable_data_for_move,
        comments,
        comment,
        draggable_data,
        update_location_data,
        customDrawerAm,
        customDrawerPm,
        radio_selected_data,
        date,
        ):
        #settingpageでセットしたclient_storageの内容に従って、デフォルトでの追加タスクを設定する
        #0 on /1 off
        change_set = page.client_storage.get("default_task")
        
        model = DataModel()
        
        try:
            set_task1 = int(change_set["業務調整"])
        except:
            page.client_storage.set("default_task",{"業務調整":0})
            set_task1 = 0
            #業務調整のセットon/off
        
        #追加する時間帯（設定がなければ従来通り13:15の時間帯）
        time_str = DEFAULT_TASK_TIME
        if isinstance(change_set, dict):
            time_str = change_set.get("業務調整_時間", DEFAULT_TASK_TIME)
        if time_str not in model.times():
            time_str = DEFAULT_TASK_TIME
        num = model.times().index(time_str)

        match set_task1:
            case 0: #on 業務調整を設定した時間帯にデフォルトで追加する
                #columns[num] が設定した時間帯
                columns[num].content = ft.DragTarget(
                    content=ft.Column(
                            controls = [
                                ft.IconButton(
                                    icon = ft.icons.DELETE_OUTLINE,
                                    visible = False,
                                    icon_size = 20,
                                    icon_color = "red",
                                    on_click = lambda e:Handlers.delete_content(
                                        e=e,
                                        page=page,
                                        phNameList=phNameList,
                                        phName=phName,
                                        drag_data=drag_data,
                                        count_dict=count_dict,
                                        comment_dict=comment_dict,
                                        columns=columns,
                                        draggable_data_for_move=draggable_data_for_move,
                                        comments=comments,
                                        times=model.times(),  # delete_contentでの引数ではtimes
                                        comment=comment,
                                        draggable_data=draggable_data,
                                        update_location_data=update_location_data,
                                        customDrawerAm=customDrawerAm,
                                        customDrawerPm=customDrawerPm,
                                        radio_selected_data=radio_selected_data,
                                        date=date,
                                    ),
                                    data = {"num":num}
                                ),
                                ft.Draggable(
                                    group = "timeline_accepted",
                                    content = ft.Container(
                                        content = ft.Text("業務調整",color = "white"),
                                        width = 50,
                                        height = 140,
                                        bgcolor = Handlers.change_color("業務調整"),
                                    ),
                                    data = {
                                        "time":time_str,
                                        "num":num,
                                        "task":"業務調整",
                                    },
                                ),
                                ft.PopupMenuButton(
                                    items = [
                                        MakePopup.add_popup(
                                            time=time_str,
                                            update_location_data=update_location_data,
                                            num=num,
                                            columns = columns,
                                            page=page,
                                            radio_selected_data=radio_selected_data,
                                            date=date,
                                        )
                                    ],
                                    tooltip= "編集",
                                    icon=ft.icons.MORE_VERT,
                                    icon_size=20,
                                    on_open=lambda e:MakePopup.pop_up_reload(
                                        e=e,
                                        customDrawerAm=customDrawerAm,
                                        customDrawerPm=customDrawerPm,
                                        page=page,
                                    ),
                                    data={"time":time_str},
                                ),
                                ft.Container(),
                            ],
                            height=370,
                            spacing = 0,
                            
                        ),
                    data = {"time":time_str,"num":num,"task":"業務調整",},
                )
                #drag_dataに追加
                drag_data[time_str] = {"task":"業務調整","num":num}
                #コメントはないから不要
                #カウントデータも不要
            case 1:
                pass