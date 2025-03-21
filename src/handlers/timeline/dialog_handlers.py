class DialogHandlers:
    @staticmethod
    def close_dialog(e, dialog, page):
        dialog.open = False
        page.update()

    @staticmethod
    def create_dialog_for_comment(e, comments, dlg, comment_dict, comment_field, page):
        comment_time = comments[e.control.data["num"]].data["time"]
        comment_num = comments[e.control.data["num"]].data["num"]
        dlg.data = {"time": comment_time, "num": comment_num}
        # TextFiledの初期化
        if comment_time in comment_dict:
            comment_field.value = comment_dict[comment_time]["comment"]
        else:
            comment_field.value = ""
        page.open(dlg)

    @staticmethod
    def add_comment_for_dict(e, dlg, comment_dict, comment_field, page):
        comment_time = dlg.data["time"]
        comment_num = dlg.data["num"]
        if comment_time in comment_dict:
            del comment_dict[comment_time]
            comment_dict[comment_time] = {"comment": comment_field.value}
        else:
            comment_dict[comment_time] = {"comment": comment_field.value}

        dlg.open = False
        page.update()

    @staticmethod
    def dlg_close(e, dlg, page):
        dlg.open = False
        page.update()
    
    @staticmethod
    def dlg_open(e, dlg):
        dlg.visible = True