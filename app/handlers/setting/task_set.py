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
        DataModel,
        comment,
        draggable_data,
        ):
        #settingpageでセットしたclient_storageの内容に従って、デフォルトでの追加タスクを設定する
        #0 on /1 off
        change_set = page.client_storage.get("default_task")
        if int(change_set["13:15業務調整"])is None:
            set_task1 = 0
        else:
            set_task1  = int(change_set["13:15業務調整"]) #業務調整のセットon/off
        
        match set_task1:
            case 0: #on 13:15業務調整を 13:15の時間帯にデフォルトで追加する
                #columns 19 が 13:15の時間帯
                columns[19].content = ft.Column(
                    controls = [
                        ft.IconButton(
                            icon = ft.icons.DELETE_OUTLINE,
                            visible = False,
                            icon_size = 20,
                            icon_color = "red",
                            on_click = lambda e:Handlers.delete_content(
                                e,
                                page,
                                phNameList,
                                phName,
                                drag_data,
                                count_dict,
                                comment_dict,
                                columns,
                                draggable_data_for_move,
                                comments,
                                DataModel().times(),  # delete_contentでの引数ではtimes
                                comment,
                                draggable_data,
                            ),
                            data = {"num":19}
                        ),
                        ft.Draggable(
                            group = "timeline_accepted",
                            content = ft.Container(
                                content = ft.Text("13:15業務調整",color = "white"),
                                width = 50,
                                height = 140,
                                bgcolor = Handlers.change_color("13:15業務調整"),
                            ),
                            data = {
                                "time":"13:15",
                                "num":19,
                                "task":"13:15業務調整",
                            },
                        ),
                        
                    ],
                    height = 300,
                    spacing = 0,
                    data = {
                        "time":"13:15",
                        "num":19,
                        "task":"13:15業務調整",
                    }
                )
                #drag_dataに追加
                drag_data["13:15"] = {"task":"13:15業務調整","num":19}
                #コメントはないから不要
                #カウントデータも不要
            case 1:
                pass