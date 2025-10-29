# compoments_graph
import flet as ft

class ComponentChart:
    pass

class FilePickCard:
    def __init__(self,textButton):
        """_summary_

        Args:
            textButton (_type_): "ファイルを選択"ボタン
        """
        self.textButton = textButton
    def create(self):
        return ft.Card(
            content = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.ListTile(
                            leading = ft.icon(ft.icons.FOLDER),
                            title = ft.Text("csvファイルを選択してください"),
                            title_alignment = ft.MainAxisAlignment.END,
                        ),
                        ft.Row(
                            [self.textButton],
                            alignment = ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
            ),
            width =500,
        )

class FileNameCard:
    def __init__(self):
        pass
    def create(self):
        return ft.Card(
            content=ft.Container(
                content=ft.ListView(
                    controls=[
                        ft.ListTile(
                            leading=ft.icon(ft.icons.DESCRIPTION),
                            title=ft.Text("読み込んだファイル一覧"),
                            title_alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    expand=10,  # 修正: 高さを固定するために expand を False に設定
                    spacing=10,
                    auto_scroll=True,
                    padding=10,
                )
            )
        )