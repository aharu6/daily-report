import threading

#保存完了時のメッセージ表示
class HideMessageHandler:
    @staticmethod
    def hide_message(message, page):
        threading.Timer(10, lambda: HideMessageHandler._hide(message, page)).start()
        
        
    @staticmethod
    def _hide(message, page):
        message.content.controls[0].visible = False
        message.content.controls[1].visible = False
        page.update()

#一時保存時のメッセージ表示
    @staticmethod
    def hide_message_temp(message,page) :
        threading.Timer(10, lambda: HideMessageHandler._hide_temp(message, page)).start()
        
    @staticmethod
    def _hide_temp(message, page):
        message.content.controls[0].visible = False
        message.content.controls[1].visible = False
        page.update()
