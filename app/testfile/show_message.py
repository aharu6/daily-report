import flet as ft
import threading

class Component:
    def __init__(self):
        self.message = ft.Text("This is a message")
        

class HideMessageHandler:
    @staticmethod
    def hide_message(message,page):
        threading.Timer(5,lambda:HideMessageHandler._hide(message,page)).start()
        
    @staticmethod
    def _hide(message,page):
        message.visible =False
        page.update()
    
def main(page: ft.Page):
    component = Component()
    page.add(
        component.message,
        ft.TextButton("hide message",on_click = lambda e:HideMessageHandler.hide_message(component.message,page)),
        )
ft.app(main)