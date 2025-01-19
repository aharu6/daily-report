import flet as ft
class DragLeave:
    @staticmethod
    def drag_leave(e,page):
        e.control.content = ft.Container(
            width=50,
            height=300,
            bgcolor="#CBDCEB",
            border_radius=5,
        )
        #group やon_willaccept関数の設定も元に戻す
        e.control.update()