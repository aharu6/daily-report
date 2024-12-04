import flet as ft
from flet import View, Page
import datetime
import csv
import pandas as pd
import json

#上から順に
#日付、名前選択、午前・午後選択


#日付選択ボタン
class Date_Button(ft.ElevatedButton):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.today = datetime.date.today()
        self.text = f"{self.today.year}/{self.today.month}/{self.today.day}"
        self.icon = ft.icons.CALENDAR_MONTH
        self.on_click = lambda e: page.open(
            ft.DatePicker(
                first_date = datetime.date(
                    year = self.today.year,month = self.today.month,day = self.today.day
                    ),
                on_change = self.handle_change,
                )
            )
        
    
    def handle_change(self,e):
        selected_date = e.control.value #例えば2021-01-01のような形式
        
        #日付オブジェクトに変換
        today = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
        
        #年月日を取得して表示用のテキストに変換
        self.Date.text = f"{today.year}/{today.month}/{today.day}"
        self.Date.update()
        
#ユーザー選択
    # phNameListに基づき名前ごとにドロップダウンを作成
    # 最後にはデータ追加ボタンを実装する    
class phNameDropDown(ft.Dropdown):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.width = 130
        self.options = []
        self.on_change = self.dropdown_changed
        self.label = "Name"
        self.text_size = 12,
        self.label_style = ft.TextStyle(size = 12)
        self.border_color = ft.colors.BLUE_GREY_100
        self.height = 40
        self.update_dropdown(self)
        self.page.update()
    

    def dropdown_changed(self,e):
        if self.value == "Add":
            dialog = Pagedialog(self.page)
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()            
        
    def update_dropdown(self,e):
        phNameList = self.get_phNameList()
        if phNameList is not None:
            self.options = [ft.dropdown.Option(item["name"]) for item in phNameList]
        else:
            self.options.append(ft.dropdown.Option("Add"))
        #phNameがない場合にはAddのみを表示
        self.options.append(ft.dropdown.Option("Add"))
        self.page.update()
        
    def get_phNameList(self):
        return json.loads(self.page.client_storage.get("phName"))

class Pagedialog(ft.AlertDialog):
    def __init__(self,page:ft.Page):    
        super().__init__()
        self.title = ft.Text("Add Name")
        self.content = ft.TextField(label = "新しく追加する名前を入力してください")
        self.actions = [
            ft.TextButton("追加",on_click = self.add_name),
            ft.TextButton("キャンセル",on_click = self.close_dialog)
        ]
        self.page = page
        
        
    #phNameList への追加        
    def add_name(self,e):
        new_name = self.content.value.strip()
        phNameList = self.get_phNameList()
        if new_name:
            phNameList.append({"name":new_name})
            self.page.client_storage.set("phName",json.dumps(phNameList,ensure_ascii=False))
            self.content.value = ""
            self.close_dialog(e)
            self.update_dropdown()
        self.page.update()
        
    def close_dialog(self, e):
        # ダイアログを閉じる
        self.open = False
        self.page.update()
        
    def get_phNameList(self):
        try:
            return json.loads(self.page.client_storage.get("phName")) or []
        except TypeError:
            return []        
        
class ColphName(ft.Column):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.controls = [
            ft.Icon(ft.icons.ACCOUNT_CIRCLE),
            phNameDropDown(self.page)
            ]
        
class ColampamSelect(ft.Column):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.controls = [
            ft.Icon(ft.icons.SCHEDULE),
            ampmSelect(self.page)
        ]
        
class ampmSelect(ft.Row):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.controls = [
            TimeDropdown(self.page,"AM"),
            ft.Container(height = 20,width = 10),
            TimeDropdown(self.page,"PM"),
        ]
        
class TimeDropdown(ft.Dropdown):
    def __init__(self,page:ft.Page,label:str):
        super().__init__()
        self.width = 130
        self.options = [
            ft.dropdown.Option("ICU"),
            ft.dropdown.Option("3A"),
            ft.dropdown.Option("3B"),
            ft.dropdown.Option("3C"),
            ft.dropdown.Option("CCU"),
            ft.dropdown.Option("4A"),
            ft.dropdown.Option("4B"),
            ft.dropdown.Option("4C"),
            ft.dropdown.Option("HCU"),
            ft.dropdown.Option("5A"),
            ft.dropdown.Option("5B"),
            ft.dropdown.Option("5C"),
            ft.dropdown.Option("5D"),
        ]
        self.label = label
        self.text_size = 12,
        self.label_style = ft.TextStyle(size = 12)
        self.border_color = ft.colors.BLUE_GREY_100
        self.height = 40
