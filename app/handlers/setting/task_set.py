import flet as ft
from handlers.handlers import Handlers
from models.models import DataModel

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
        ):
        #settingpageでセットしたclient_storageの内容に従って、デフォルトでの追加タスクを設定する
        #0 on /1 off
        change_set = page.client_storage.get("default_task")
        
        try:
            set_task1 = int(change_set["業務調整"])
        except:
            page.client_storage.set("default_task",{"業務調整":0})
            set_task1 = 0
            #業務調整のセットon/off
        
        match set_task1:
            case 0: #on 業務調整を 13:15の時間帯にデフォルトで追加する
                #columns 19 が 13:15の時間帯
                columns[19].content = ft.DragTarget(
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
                                        times=DataModel().times(),  # delete_contentでの引数ではtimes
                                        comment=comment,
                                        draggable_data=draggable_data,
                                    ),
                                    data = {"num":19}
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
                                        "time":"13:15 13:30",
                                        "num":19,
                                        "task":"業務調整",
                                    },
                                ),
                                
                            ],
                            height = 300,
                            spacing = 0,
                            
                        ),
                    data = {"time":"13:15 13:30","num":19,"task":"業務調整",},
                )
                #drag_dataに追加
                drag_data["13:15 13:30"] = {"task":"業務調整","num":19}
                #コメントはないから不要
                #カウントデータも不要
            case 1:
                pass