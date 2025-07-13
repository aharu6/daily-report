from models.models import DataModel

#ページ遷移の共通ハンドラを定義
class Handlers_Main:
    @staticmethod
    def on_navigation_change(e,page):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/")
        elif selected_index == 1:
            page.go("/chart")
        elif selected_index == 2:
            page.go("/calendar")
        elif selected_index == 3:
            page.go("/settings")