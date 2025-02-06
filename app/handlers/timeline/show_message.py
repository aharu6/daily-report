import threading
class ShowMessageHandler:
    @staticmethod
    def hide_message():
        save_message.visible = False

    @staticmethod
    def set_timer():
        threading.Timer(5,ShowMessageHandler.hide_massage()).start