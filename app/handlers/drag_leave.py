import flet as ft
class DragLeave:
    @staticmethod
    def drag_leave(e,page):
        e.control.content.bgcolor = None
        #
