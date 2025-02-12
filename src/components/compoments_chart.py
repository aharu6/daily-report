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
                            leading = ft.Icon(ft.icons.FOLDER),
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