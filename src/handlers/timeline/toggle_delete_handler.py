class DeleteButtonHandler:
    @staticmethod
    def toggle_delete_button(e, page, columns):
        e.control.selected = not e.control.selected
        # 全てのselect columnsを選択不可能にする
        for i in range(len(columns)):
            # columns[i].disabled = not columns[i].disabled
            # disabled効かない
            # 特定のグループ名にして、falseの中で分ける？
            # seeletcolumnの方ではなくて、columnsの方
            if columns[i].content.group == "timeline":
                columns[i].content.group = "delete_toggle"
            elif columns[i].content.group == "delete_toggle":
                columns[i].content.group = "timeline"

        for i in range(len(columns)):
            if columns[i].content.data is not None:
                task = columns[i].content.data["task"]
                match task:
                    case "will_accept":
                        pass
                    case "":
                        pass
                    case _:
                        try:
                            # 初回ドラッグコンテンツ用のdeletebutton visible
                            # 全てのカラムで押すたびにtrueとfalseを揃える
                            # ゴミ箱アイコンがonのときにはドラッグできないように編集する
                            columns[i].content.content.controls[0].visible = (
                                not columns[i].content.content.controls[0].visible
                            )
                        except:
                            # reload時のdeletebutton visible
                            pass

                # button.visible = not button.visible
        page.update()
