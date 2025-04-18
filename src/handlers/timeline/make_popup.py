import flet as ft
from models.models import DataModel
class MakePopup:
    @staticmethod
    #選択した病棟名を取得し、ラジオボタンのメニューを作成する
    #何もない時はnoneの表示のみとする
    def make_popup(e,page):
        e.control.items.append(
            ft.PopupMenuItem(
                text = "item5",
                content = ft.Column(
                    controls = [
                        ft.RadioGroup(
                            ft.Radio(value = "test5",label ="test5"),
                            data = {"time":"test5"},
                        )
                    ]
                )
            )
        )
        
        #次回コントロールを追加した時がpopupmenuitem の追加タイミングになる
        #最初からitemsへの追加が良いかも

    #病棟データは時間ごとの辞書に直す必要が出てくる
    #選択したら、その時間の病棟データは直す
    #選択した場合のみ辞書データを作成して、合わせるときに合成するか
    #午前と午後でそれぞれ別のラジオボタンを作成しなければならない
    
    
    @staticmethod
    def add_popup(time, update_location_data, num, columns,page,radio_selected_data,date):
        
        # 午前と午後の判別
        pop_up = ft.PopupMenuItem(
            content = ft.RadioGroup(
                ft.Column(
                    controls=[]
                ),
                data={"time": time},
                on_change=lambda e: MakePopup.radio_click(
                    e=e, time=time, update_location_data=update_location_data, num=num, columns=columns,page=page,
                    radio_selected_data=radio_selected_data,
                    date=date
                    )
                
            )
        )
        
        # 何かは追加しておかないとreload機能が機能しない
        # popupmenuitem のみ追加しておく
        return pop_up
    
    #再描画用の読み込みハンドラ
    #reloadボタンは不要
    #noneはややこしいからいらないかも
    @staticmethod
    def pop_up_reload(e,customDrawerAm,customDrawerPm,page):
        list_am_location = []
        for i in range(len(customDrawerAm.content.controls)):
            if customDrawerAm.content.controls[i].value == True:
                list_am_location.append(customDrawerAm.content.controls[i].label)
        list_pm_location = []
        for i in range(len(customDrawerPm.content.controls)):
            if customDrawerPm.content.controls[i].value == True:
                list_pm_location.append(customDrawerPm.content.controls[i].label)
                
        #午前と午後の判別
        time = e.control.data["time"]
        time_model = DataModel()
        amtime = time_model.amTime()
        pmtime = time_model.pmTime()
        
        #前のラジオボタンのリセット
        e.control.items[0].content.content.controls.clear()
        if time in amtime:
            if len(list_am_location) > 0:
                for i in range(len(list_am_location)):        
                    e.control.items[0].content.content.controls.append(
                        ft.Radio(value=list_am_location[i], label=list_am_location[i])
                    )
            else:
                pass
        elif time in pmtime:
            if len(list_pm_location) > 0:
                for i in range(len(list_pm_location)):        
                    e.control.items[0].content.content.controls.append(
                        ft.Radio(value=list_pm_location[i], label=list_pm_location[i])
                    )
            else:
                pass
        else:
            pass

        page.update()
            
    @staticmethod
    def radio_click(e, time, update_location_data, num, columns,page,radio_selected_data,date):
        from datetime import datetime
        # クリックされた時は辞書データの更新を行う
        # 時間データの取得
        time = e.control.data["time"]
        #選択された病棟データの取得
        selected_location = e.control.value
        #辞書データの更新
        update_loc_data = update_location_data
        
        #時間データに紐付ける
        update_loc_data[time] = selected_location
        
        #選択された病棟名の表示
        #numにてカラム番号の取得
        #accdptedでのcontrolの一番最後にft.Textを追加する
        #変更したら更新。場所を決めておく ３番目
        columns[num].content.content.controls[3].content = ft.Text(selected_location)
        e.control.data["radio_select"]=selected_location
        if isinstance(date.data,str):
            date.data=datetime.strptime(date.data,"%Y-%m-%d")
        select_day=f"{date.data.year}-{date.data.month}-{date.data.day}"
        radio_selected_data[time]= {"date":select_day,"time":time,"num":num,"radio_select":selected_location}
        page.update()