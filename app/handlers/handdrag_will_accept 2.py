import flet as ft
import re
class Add_will_accept:
    @staticmethod
    def drag_will_accept(e,page,columns,drag_data):
        #TrueかFalseで帰ってくるはず
        #Falseならgroup = "timeline"に変更してon_moveを追加する
        #on_moveコンテンツを減らして、・だけにする、data = {"time","task","num"}だけ渡しておく
        #on_acceptにて全てのからむに対して data = {}中身がある場合にのみcolumns.content を更新する
        #Falseの時だけ　 data = {}を渡してcolumnsに・を追加することはできる？
        #data = winllacceptだけ渡してaccept関数にて更新
        #更新時にdataを削除すれば大丈夫？    
        #左のカラムにtaskもしくはaccpeptか何かしらのデータがある場合に発動するようにする
        left_num = e.control.data["num"] - 1    
        left_column_data = columns[left_num].content.data["task"]
        if re.search(r'.+',left_column_data):
            if e.data == 'false':
                e.control.content = ft.Column(
                    controls=[
                        ft.Draggable(
                            group = "timeline_accepted",
                            content = ft.Container(
                                #keyは受け取れないから後でaccept時に追加する
                                width  = 50,
                                height = 50,
                                border_radius = 50,
                                #colorもkeyによるのでacceptにて適用する
                                #丸とか別の形にする？
                                #右にスライドしたら右矢印、左にドラッグしたら左矢印　コンテンツのみの更新
                                #データ保存時にどうにかする
                                #方向は固定できる？
                                #コピーの方向は右移動だけに限定する？　データ編集が楽
                                #右と左それぞれからドラッグされた時バッティングするため
                                #表示矢印も右矢印だけですむ
                                bgcolor = "blue",
                                content = ft.Icon(ft.icons.ARROW_RIGHT,color = "ehite"),
                            ),
                            data = {
                                "time":e.control.data["time"],
                                "num":e.control.data["num"],
                                "task":"will_accept"
                            },
                            )
                    ]
                )
                e.control.data["task"] = "will_accept"
                e.control.on_will_accept = None
                # e.controlに新しいdrag_accceptを追加する
                #無理なら先にpage.updateする
                e.control.group = "timeline_accepted" 
                
                drag_data[e.control.data["time"]] = {"task":"will_accept"}
                
                
        page.update()
