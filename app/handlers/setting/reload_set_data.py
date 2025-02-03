#デフォルトで表示する業務内容のON/OFFを切り替える表示設定
#client_storage内に保存する

class ReloadSetDataButton:
    @staticmethod
    def reload_set_data_button(e,page):
        change_set = page.client_storage.get("default_task")
        if change_set == None:
            page.client_storage.set("default_task",{"13:15業務調整":0}) #0でon 1でoff
        page.client_storage.set("default_task",{"13:15業務調整":e.data})
    
    @staticmethod
    def select_index(page):
        selected_data = page.client_storage.get("default_task")
        if selected_data == None:
            return 0
        return int(selected_data["13:15業務調整"])
