import flet as ft

class Add_will_accept:
    @staticmethod
    def drag_will_accept(e,page,columns,draggable_data):
        #TrueかFalseで帰ってくるはず
        #Falseならgroup = "timeline"に変更してon_moveを追加する
        #on_moveコンテンツを減らして、・だけにする、data = {"time","task","num"}だけ渡しておく
        #on_acceptにて全てのからむに対して data = {}中身がある場合にのみcolumns.content を更新する
        #Falseの時だけ　 data = {}を渡してcolumnsに・を追加することはできる？
        #data = winllacceptだけ渡してaccept関数にて更新
        #更新時にdataを削除すれば大丈夫？       
        if e.data == 'true':
            e.control.content = ft.Container(
                bgcolor = "red",
                width=50,
                height=140,
                )
            e.control.data["task"] = "will_accept"
            # e.controlに新しいdrag_accceptを追加する
            #無理なら先にpage.updateする
        page.update()
