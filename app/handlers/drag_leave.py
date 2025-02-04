import flet as ft
class DragLeave:
    @staticmethod
    def drag_leave(e,page):
        print("drag_leave")
        e.control.content.border = None
