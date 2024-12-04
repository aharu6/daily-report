import flet as ft
from flet import View, Page
import datetime
import csv
import pandas as pd
import json
times = [
        "8:30 8:45",
        "8:45 9:00",
        "9:00 9:15",
        "9:15 9:30",
        "9:30 9:45",
        "9:45 10:00",
        "10:00 10:15",
        "10:15 10:30",
        "10:30 10:45",
        "10:45 11:00",
        "11:00 11:15",
        "11:15 11:30",
        "11:30 11:45",
        "11:45 12:00",
        "12:00 12:15",
        "12:15 12:30",
        "12:30 12:45",
        "12:45 13:00",
        "13:00 13:15",
        "13:15 13:30",
        "13:30 13:45",
        "13:45 14:00",
        "14:00 14:15",
        "14:15 14:30",
        "14:30 14:45",
        "14:45 15:00",
        "15:00 15:15",
        "15:15 15:30",
        "15:30 15:45",
        "15:45 16:00",
        "16:00 16:15",
        "16:15 16:30",
        "16:30 16:45",
        "16:45 17:00",
    ]

count_dict = {} 

draggable_data = {
        '_264':{"task":"情報収集＋指導"},
        '_268':{"task":"指導記録作成"},
        '_272':{"task":"混注準備"},
        '_276':{"task":"混注時間"},
        '_280':{"task":"薬剤セット数"},
        '_284':{"task":"持参薬を確認"},
        '_288':{"task":"薬剤服用歴等について保険薬局へ照会"},
        '_292':{"task":"処方代理修正"},
        '_296':{"task":"TDM実施"},
        '_300':{"task":"カンファレンス"},
        '_304':{"task":"休憩"},
        '_308':{"task":"その他"},
    }
class ButtonManager:
    def __init__(self,times,columns,drag_data,page,count_dict,draggable_data):
        self.times = times
        self.columns = columns
        self.drag_data = drag_data
        self.page = page
        self.button_list = []
        self.editButton = ft.ElevatedButton(
            icon = ft.icons.DELETE_OUTLINE,
            icon_size = 20,
            on_click = self.toggle_delete_button,
        )
        
        self.delete_buttons = [
            ft.IconButton(
                icon = ft.icons.REMOVE,
                visible = False,
                icon_color = "red",
                icon_size = 20,
                on_click = self.delete_content
            )
            for _ in range(len(times))
        ]
        
        self.count_dict = count_dict
        self.draggable_data = draggable_data
        
        self.comments = [
            ft.IconButton(
                icon = ft.icons.COMMENT,
                on_click = lambda e:create_dialog_for_comment(e),
            )
            for _ in range(len(times))
        ]
        
        self.comment = ft.IconButton(
            icon = ft.icons.COMMENT,
            on_click = lambda e:dlg_open,
        )
        
        self.comment_field = ft.TextField(label = "その他")
    
    def toggle_delete_button(self,e):
        for button in self.delete_buttons:
            button.visible = not button.visible
        self.page.update()
        
    def delete_content(self,e):
        #_move関数でdelete_button.dataに入れたのはdragtargetで設定したカラムの番号
        #columns[i]でそのカラムの情報を取得し、見た目上削除
        #正しくはcolumnsの初期化を行う。ドラッグする前の状態に戻す
        col_num = self.delete_buttons[e.control.data["num"]].data["num"]
        columns[col_num].content = ft.DragTarget(
            group = "timeline",
            content = ft.Container(
                width = 50,
                height = 300,
                bgcolor = None,
                border_radius = 5,
            ),
            on_accept = self.drag_accepted,
            on_move = drag_move,
            data = {"time":times[col_num],"num":col_num},
        )
        columns[col_num].update()
        #同時に該当するdatag_dataのデータも削除する
        del self.drag_data[times[col_num]]
    
    
    #カウンターの関数
    def counterPlkus(self,e,count_field):
        old_Count = int(count_field.value)
        new_Count = old_Count + 1
        #更新した値にてカウンター内おを更新
        count_field.value = new_Count
        count_field.update()
        #dict内の値を更新
        self.count_dict[e] = {"count":new_Count}
    
    def counterMinus(self,e,count_field):
        # +と同様
        old_Count = int(count_field.value)
        new_Count = old_Count - 1
        count_field.value = new_Count
        count_field.update()
        self.count_dict[e] = {"count":new_Count}
        
    def create_counter(self,e):
        # eは入力したカラムの時間を取得
        # sqlite3データベースからカウントを取得
        #res = cur.execute("SELECT count FROM timeline WHERE time = ?", (e,))
        #count = res.fetchall()[0][0]
        #初期は０
        count = 0
        
        count_field = ft.TextField(
            count,
            width = 40,
            text_align = ft.TextAlign.CENTER,
            text_size = 10,
            border_color = None,
        )
        count_dict[e] = {"count":count}
        return ft.Column(
            [
                ft.IconButton(
                    ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size = 25,
                    on_click = lambda _:counterPlus(e,count_field),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                count_field,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size = 25,
                    on_click = lambda _:counterMinus(e,count_field),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
            ]
        )
    
    drag_data = {}
    
    #コメントのダイアログ
    def dlg_close(e):
        dlg.open = False
        page.update()
        
    comment_dict = {}
    
    def create_dialog_for_comment(self,e):
        comment_time = self.comments[e.control.data["num"]].data["time"]
        comment_num = self,comments[e.control.data["num"]].data["num"]
        dlg.data = {"time":comment_time,"num":comment_num}
        print(comment_time)
        #TextFieldの初期化
        if comment_time in comment_dict:
            comment_filed.value = comment_dict[comment_time]["comment"]
        else:
            comment_filed.value = ""
        self.page.open(dlg)
    
    def dlg_open(self,e):
        self.dlg.visible = True
        
    def add_comennt_for_dict(e):
        comment_time = dlg.data["time"]
        comment_num = dlg.data["num"]
        if comment_time in comment_dict:
            del comment_dict[comment_time]
            comment_dict[comment_time] = {"comment":comment_filed.value}
        else:
            comment_dict[comment_time] = {"comment":comment_filed.value}
            

        dlg.open = False
        page.update()
    