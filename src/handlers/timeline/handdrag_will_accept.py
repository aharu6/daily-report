import flet as ft
class Add_will_accept:
    @staticmethod
    def drag_will_accept(e,page,columns,drag_data):
        #TrueかFalseで帰ってくるはず
        #Falseならgroup = "timeline"に変更してon_moveを追加する
        #on_moveコンテンツを減らして、・だけにする、data = {"time","task","num"}だけ渡しておく
        #on_acceptにて全てのからむに対して data = {}中身がある場合にのみcolumns.content を更新する
        #Falseの時だけ　 data = {}を渡してcolumnsに・を追加することはできる？
        #data = winllacceptだけ渡してaccept関数にて更新
        #左にドラッグしないようにする
        left_key = columns[e.control.data["num"]-1].content.data["task"]
        if e.data == 'false':
            #deleteiconがonになっているときは矢印も表示しない
            #編集できないようにする
            if e.control.group == "timeline":
                match left_key:
                    case "":
                        pass
                    case _:
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
                                        #右にスライドしたら右矢印、左にドラッグしたら左矢印　コンテンツのみの更新
                                        #コピーの方向は右移動だけに限定する？　データ編集が楽
                                        #右と左それぞれからドラッグされた時バッティングするため
                                        #表示矢印も右矢印だけですむ
                                        content = ft.Icon(ft.icons.DOUBLE_ARROW,color = "#2D6E7E"),
                                        alignment = ft.alignment.top_center,
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
                        drag_data[e.control.data["time"]] = {"task":"will_accept"}
            elif e.control.group == "delete_toggle":
                pass
        #trueの時（初回ドラッグの時はドラッグ可能であることを示す色をつける）
        elif e.data == 'true':
            e.control.content.border = ft.border.all("#B6EB7A")
            
        page.update()
