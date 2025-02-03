#reloadした後のコンテンツにおけるdeleteの挙動
import flet as ft
from models.models import DataModel
from handlers.handdrag_will_accept import Add_will_accept
class DeleteContentReloadHandler:
    @staticmethod
    def delete_content_for_reload(e,
                                page,
                                drag_data,
                                count_dict,
                                comment_dict,
                                columns,
                                ):
        col_num = e.control.data["num"]
        columns[col_num].content = ft.Column(
            controls = [
                ft.Container(
                    width  = 50,
                    height = 300,
                    bgcolor = "#CBDCEB",
                    border_radius = 5,
                )
            ]
        )
        #該当するdrag_dataを削除
        del drag_data[e.control.data["time"]]
        #該当のcountデータも削除
        if DataModel().times()[col_num] in count_dict:
            del count_dict[DataModel().times()[col_num]]
        #該当のcommentデータも削除
        if DataModel().times()[col_num] in comment_dict:
            del comment_dict[DataModel().times()[col_num]]
            
        right_col_num = e.control.data["num"] +1
        try:
            right_key = columns[right_col_num].content.data["task"]
        except:
            right_key = None
        
        #右方向に広がるcontent.data["task"] == "will_accept"のコンテンツは全て削除
        #while
        while right_key == "will_accept":
            columns[right_col_num].content = ft.Column(
                controls = [
                    ft.Container(
                        width = 50,
                        height = 300,
                        bgcolor = "#CBDCEB",
                        border_radius = 5,
                    ),
                ]
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
            
        page.update()