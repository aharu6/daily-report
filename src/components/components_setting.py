import flet as ft
import json
from handlers.setting.reload_set_data import ReloadSetDataButton
from handlers.setting.trash_exp import Trashdata_ExpantionPanel

class Title:
    def __init__(self, page):
        self.page = page

    def create(self):
        return ft.Text(
            "設定、保存データの編集",
            size=20,
            weight=ft.FontWeight.BOLD,
        )


class Panel:
    def __init__(self, page):
        self.page = page

    def create(self, phNameList, page):
        # phNameLIst が文字列の場合、リストに変換
        #phNameListがない時は名前が登録されていないパネルを返す
        if isinstance(phNameList, str):
                phNameList = json.loads(phNameList)


        load_data = page.client_storage.get("timeline_data")
        try:
            key = list(json.loads(load_data).keys())
        except:
            key = []
        
        return ft.ExpansionPanelList(
            elevation=8,
            divider_color="#D6EFD8",
            controls=[
                ft.ExpansionPanel(
                    bgcolor=None,
                    header=ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON),
                        title=ft.Text("ユーザー名の編集"),
                    ),
                    content=ft.Column(
                        # 名前があれば保存しているデータを呼び出す
                        # なければadd_nameを表示
                        controls=[]
                        + (
                            [
                                ft.ListTile(
                                    title=ft.Text("名前が登録されていません"),
                                )
                            ]
                            if not phNameList
                            else []
                        ),
                    ),
                ),
                ft.ExpansionPanel(
                    bgcolor=None,
                    header=ft.ListTile(
                        leading=ft.Icon(ft.icons.STORAGE),
                        title=ft.Text("この端末に保存されているデータ"),
                    ),
                    content = ft.DataTable(
                        width = 700,
                        #Time,Task,Count,locate,date,PhName,Comment
                        columns = [
                            ft.DataColumn(ft.Text("日付_名前")),
                            ft.DataColumn(ft.Text("")),
                        ],
                        rows = [
                            ft.DataRow(
                                    cells = [
                                    ]
                                )
                            for i in key
                        ],
                    ),
                ),
                ft.ExpansionPanel(
                    bgcolor=None,
                    header=ft.ListTile(
                        leading=ft.Icon(ft.icons.DELETE),
                        title=ft.Text("削除データ"),
                        subtitle=ft.Text("ここに保管されているデータは30日後に自動削除されます")
                        ),
                        content=ft.Column(
                            controls=Trashdata_ExpantionPanel.create_expantion_panel(page)
                    
                        )
                ),
                ft.ExpansionPanel(
                    bgcolor = None,
                    header = ft.ListTile(
                        leading = ft.Icon(ft.icons.VISIBILITY),
                        title = ft.Text("デフォルトの表示設定"),
                    ),
                    content = ft.Column(
                        controls = [
                            ft.ListTile(
                                title = ft.Text("業務調整のデフォルト追加"),
                                subtitle = ft.Text("ONにすると起動時にデフォルトで表示されます"),
                                trailing = ft.CupertinoSlidingSegmentedButton(
                                    controls = [
                                        ft.Text("ON"),
                                        ft.Text("OFF"),
                                    ],
                                    selected_index =ReloadSetDataButton.select_index(page),
                                    on_change = lambda e:ReloadSetDataButton.reload_set_data_button(e,page),
                                    data = "業務調整"
                                )
                            )
                        ]
                    )
                
                )
            ],
        )


        
            
        