import flet as ft

class DragMoveHandler:
    @staticmethod
    def drag_move(
        e,
        page,
        draggable_data,
        delete_buttons,
        columns,
        comments,
        times,
        drag_data,
        comment,
        count_dict,
    ):
        """_summary_

        Args:
            e (_type_): _description_
            page (_type_): _description_
            draggable_data (_type_): _description_
            delete_buttons (_type_): _description_
            columns (_type_): _description_
            comments (_type_): _description_
            times (_type_): _description_
            drag_data (_type_): _description_
            comment (_type_): _description_
            count_dict (_type_): _description_
        """
        src_id_str = e.src_id.replace("_", "")
        try:
            src_id_int = int(src_id_str)
            # 次カラム
            next_id = f"_{src_id_int + 4}"
        except:
            pass

        if page.get_control(e.src_id):
            src = page.get_control(e.src_id)
            try:
                key = src.data["task"]["task"]
            except:
                key = src.data["task"]

        elif e.src_id in draggable_data and "task":
            key = draggable_data[e.src_id]["task"]

        elif page.get_control(e.target):
            src = page.get_control(e.target)
            if isinstance(src.data["task"], dict):
                key = src.data["task"]["task"]
            else:
                key = src.data["task"]

        from handlers.handlers import Handlers
        #コンテンツの名前は非表示にしておいて、あとで再表示にvisible  = trueで再表示できるように
        e.control.content = ft.Column(
            controls=[
                delete_buttons[e.control.data["num"]],
                ft.Draggable(
                    group="timeline",
                    content=ft.Container(
                        content=ft.Text(key, color="white"),
                        width=50,
                        height=140,
                        bgcolor=Handlers.change_color(key),
                    ),
                    data={
                        "time": e.control.data["time"],
                        "num": e.control.data["num"],
                        "task": key,
                    },
                ),
            ],
            height=300,
            spacing=0,
            data={
                "time": e.control.data["time"],
                "num": e.control.data["num"],
                "task": key,
            },
        )
        page.add(e.control.content)
        e.control.content.update()

        # ドラッグ時にコンテンツを更新する用
        columns[e.control.data["num"]].content.data["task"] = key

        # delete_buttonsに渡すdata
        delete_buttons[e.control.data["num"]].data = {"num": e.control.data["num"]}
        left_column_num = e.control.data["num"] - 1
        # left_keyの初期化
        left_key = None
        try:
            left_key = columns[left_column_num].content.data["task"]
        except:
            pass

        # 現在のカラムの番号はnum = e.control.data["num"]
        # 左のカラム　num -1 のカラムの情報を取得
        # 一番左のカラムだけ表示、後は非表示にする（カウンターはそもそも作成しない）
        try:
            if left_key == key:
                e.control.content.controls[1].content.content.visible = True
                e.control.content.update()
            elif left_key != key:
                e.control.content.controls[1].content.content.visible = True
                e.control.content.update()
        except:
            pass

        match key:
            # key==その他の場合にはコメントボタンを追加する
            case "その他":
                # すでに左のカラムにコンテンツがある場合にはコメントボタンは作成しない
                e.control.content.controls.append(comments[e.control.data["num"]])
            # 混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンスの場合はカウンターを非表示にする
            case (
                "混注時間"
                | "休憩"
                | "委員会"
                | "WG活動"
                | "勉強会参加"
                | "1on1"
                | "カンファレンス"
                | "13:15業務調整"
            ):
                pass
            # その他の場合にはカウンターを表示する
            # 左カラムに同じデータはある場合にはカウンターは作成しない
            case _:
                if left_key == key:
                    pass
                else:
                    e.control.content.controls.append(
                        Handlers.create_counter(e.control.data["time"], count_dict)
                    )

        # moveにて新規src_idが追加された場合、その情報をdrag_dataに追加
        # elseに向けて辞書データを更新しておく
        draggable_data[e.src_id] = {"task": key}
        draggable_data[next_id] = {"task": key}

        # 左ではなくて、現在のカラム番号と左のカラム番号を比較する
        # 右のカラムも比較して、同じ業務内容の場合、右は非表示に
        # 左のみ残して表示する
        right_column_num = e.control.data["num"] + 1
        if right_column_num:
            right_key = columns[right_column_num].content.data["task"]
        try:
            if right_key == key:
                columns[right_column_num].content = ft.Column(
                    controls=[
                        delete_buttons[right_column_num],
                        ft.Draggable(
                            group="timeline",
                            content=ft.Container(
                                content = ft.Text(key, color="white",visible=False),
                                width=50,
                                height=140,
                                bgcolor=Handlers.change_color(key),
                            ),
                        ),
                    ],
                    height=300,
                    spacing=0,
                    data={
                        "time": times[right_column_num],
                        "num": right_column_num,
                        "task": key,
                    },
                )
                columns[right_column_num].content.update()
                columns[right_column_num].update()
        except:
            pass
        # ドラッグデータの保存
        drag_data[e.control.data["time"]] = {"task": key}
        if comment:
            comments[e.control.data["num"]].data = {
                "time": e.control.data["time"],
                "num": e.control.data["num"],
            }

        # 右隣と左隣のカラムにmove関数を追加する
        columns[left_column_num].content.on_move = lambda e: DragMoveHandler.drag_move(
            e,
            page,
            draggable_data,
            delete_buttons,
            columns,
            comments,
            times,
            drag_data,
            comment,
            count_dict,
        )
        columns[left_column_num].update()
        columns[right_column_num].content.on_move = lambda e: DragMoveHandler.drag_move(
            e,
            page,
            draggable_data,
            delete_buttons,
            columns,
            comments,
            times,
            drag_data,
            comment,
            count_dict,
        )
        columns[right_column_num].update()

        # 受け取ったらdragtargetのgroupを変更して再ドラッグ不可にする
        e.control.group = "timeline_accepted"
        page.update()
    # acceptしたらカラムのデータを更新する
    # 隣のカラムにmove関数を追加する