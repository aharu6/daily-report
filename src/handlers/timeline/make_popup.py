import flet as ft
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
                        )
                    ]
                )
            )
        )
        
    
    @staticmethod
    def make_popup2():
        return ft.PopupMenuItem(
            content = ft.RadioGroup(
                ft.Column(
                    controls=[
                        ft.Radio(value="test", label="test"),
                        ft.Radio(value="test2", label="test2"),
                        ft.Radio(value="test3", label="test3")
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
    def add_popup(page, customDrawerAm, customDrawerPm, time):
        #選択した病棟データを読み出し
        list_am_locationdata = []
        for i in range(len(customDrawerAm.content.controls)):
            if customDrawerAm.content.controls[i].value == True:
                list_am_locationdata.append(customDrawerAm.content.controls[i].label)

        pop_up = ft.PopupMenuItem(
            content = ft.RadioGroup(
                ft.Column(
                    controls=[]
                )
            )
        )
        
        #病棟データがある場合
        if len(list_am_locationdata) > 0:
            for i in range(len(list_am_locationdata)):        
                pop_up.content.content.controls.append(
                    ft.Radio(value=list_am_locationdata[i], label=list_am_locationdata[i])
                )
                
        #病棟データがない場合
        else:
            pop_up.content.content.controls.append(
                    ft.Text("None")
            )
        
        #どちらにおいても病棟選択後のラジオボタン再描画用の読み込みボタンを追加
        return pop_up
    
    @staticmethod
    def pop_up_reload(e):
        pass
    
    @staticmethod
    def radio_click(e, time):
        #クリックされた時は辞書データの更新を行う
        #時間データの取得
        print(time)
        #選択された病棟データの取得
        selected_location = e.value
        print(selected_location)
        #辞書データの更新
        print("Radio button clicked")