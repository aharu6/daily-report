#reloadした後のコンテンツにおけるdeleteの挙動
import flet as ft
from models.models import DataModel
from handlers.timeline.handdrag_will_accept import Add_will_accept
from handlers.timeline.handlers import Handlers
from handlers.timeline.drag_leave import DragLeave

class DeleteContentReloadHandler:
    @staticmethod
    def delete_content_for_reload(e,
                                page,
                                drag_data,
                                count_dict,
                                comment_dict,
                                columns,
                                draggable_data,
                                comments,
                                times,
                                comment,
                                phNameList,
                                phName,
                                draggable_data_for_move,
                                save_error_message,
                                ):
        col_num = e.control.data["num"]
        columns[col_num].content = ft.DragTarget(
            group = "timeline",
            content = ft.Container(
                width = 50,
                height = 300,
                bgcolor = "#CBDCEB",
                border_radius = 5,
            ),
            on_accept = lambda e:Handlers.drag_accepted(
                e,
                page,
                draggable_data,
                columns,
                comments,
                times,
                drag_data,
                comment,
                count_dict,
                comment_dict,
                phNameList,
                phName,
                draggable_data_for_move,
            ),
            on_will_accept = lambda e:Add_will_accept.drag_will_accept(e,page,columns,drag_data),
            on_leave = lambda e:DragLeave.drag_leave(e,page),
            data = {"time":DataModel().times()[col_num],"num":col_num,"task":""},
        )
        #該当するdrag_dataを削除
        del drag_data[e.control.data["time"]]
        #該当のcountデータも削除
        if DataModel().times()[col_num] in count_dict:
            del count_dict[DataModel().times()[col_num]]
        #該当のcommentデータも削除
        if DataModel().times()[col_num] in comment_dict:
            del comment_dict[DataModel().times()[col_num]]
        #カラムのgroupを元に戻す
        #カラムのデータを初期化
        #on_will_acceptを元に戻す
        #accept関数を元に戻す
        
        right_col_num = e.control.data["num"] +1
        try:
            right_key = columns[right_col_num].content.data["task"]
        except:
            right_key = None
        #右方向に広がるcontent.data["task"] == "will_accept"のコンテンツは全て削除
        #while
        while right_key == "will_accept":
            columns[right_col_num].content = ft.DragTarget(
                group = "timeline",
                content = ft.Container(
                    width = 50,
                    height = 300,
                    bgcolor = "#CBDCEB",
                    border_radius = 5,
                ),
                on_accept = lambda e:Handlers.drag_accepted(
                    e=e,
                    page=page,
                    draggable_data=draggable_data,
                    columns=columns,
                    comments=comments,
                    times=times,
                    drag_data=drag_data,
                    comment=comment,
                    count_dict=count_dict,
                    comment_dict=comment_dict,
                    phNameList=phNameList,
                    phName=phName,
                    draggable_data_for_move=draggable_data_for_move,
                ),
                on_will_accept = lambda e:Add_will_accept.drag_will_accept(
                    e=e,
                    page=page,
                    columns=columns,
                    drag_data=drag_data
                    ),
                on_leave = lambda e:DragLeave.drag_leave(e,page),
                data = {"time":DataModel().times()[col_num],"num":col_num,"task":""},
            )
            
            del drag_data[DataModel().times()[right_col_num]]
            if DataModel().times()[right_col_num] in count_dict:
                del count_dict[DataModel().times()[right_col_num]]
            if DataModel().times()[right_col_num] in comment_dict:
                del comment_dict[DataModel().times()[right_col_num]]
                
            columns[right_col_num].content.group = "timeline"
            columns[right_col_num].group = "timeline"
            
            columns[right_col_num].content.on_will_accept = lambda e:Add_will_accept.drag_will_accept(e,page,columns,drag_data)
            columns[right_col_num].on_will_accept = lambda e:Add_will_accept.drag_will_accept(e,page,columns,drag_data)
            right_col_num += 1
            right_key = columns[right_col_num].content.data["task"]
        else :
            pass
            
        #accept 関数は元に戻す
        
        #保存ボタン上部の名前を入力してくださいのエラーは削除する
        #save_error_message
        save_error_message.visible = False
        
        page.update()