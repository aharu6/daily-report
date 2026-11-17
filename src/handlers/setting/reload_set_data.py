#デフォルトで表示する業務内容のON/OFFを切り替える表示設定
#client_storage内に保存する

#業務調整をデフォルト追加する時間帯の初期値（未設定時はこの時間帯を使う）
DEFAULT_TASK_TIME = "13:15 13:30"

class ReloadSetDataButton:
    @staticmethod
    def reload_set_data_button(e,page):
        change_set = page.client_storage.get("default_task")
        if not isinstance(change_set, dict):
            change_set = {}
        #時間帯の設定があれば引き継ぐ
        change_set["業務調整"] = e.data #0でon 1でoff
        page.client_storage.set("default_task",change_set)

    @staticmethod
    def select_index(page):
        selected_data = page.client_storage.get("default_task")
        if not isinstance(selected_data, dict):
            return 0
        return int(selected_data.get("業務調整", 0))

    @staticmethod
    def reload_set_time_button(e,page):
        change_set = page.client_storage.get("default_task")
        if not isinstance(change_set, dict):
            change_set = {"業務調整":0}
        change_set["業務調整_時間"] = e.control.value
        page.client_storage.set("default_task",change_set)

    @staticmethod
    def select_time(page):
        selected_data = page.client_storage.get("default_task")
        if not isinstance(selected_data, dict):
            return DEFAULT_TASK_TIME
        return selected_data.get("業務調整_時間", DEFAULT_TASK_TIME)
