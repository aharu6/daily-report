import threading
class HideMessageHandler:
    @staticmethod
    def hide_message(message, page):
        threading.Timer(10, lambda: HideMessageHandler._hide(message, page)).start()
        
        
    @staticmethod
    def _hide(message, page):
        message.content.controls[0].visible = False
        message.content.controls[1].visible = False
        page.update()
        print("message hidden")