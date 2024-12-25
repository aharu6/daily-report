import flet as ft
from flet import View, Page, ScrollMode
import datetime
from components.components import (
    DateComponent,
    NameDropdown,
    EndDrawer,
    AmDropDown,
    PmDropDown,
    EditButton,
    DeleteButtons,
)
from handlers.handlers import Handlers
from handlers.handlersMain import Handlers_Main
from handlers.handlers_chart import Handlers_Chart
from models.models import DataModel
from view.setting_page import SettingPage


# timelinepageのviewを定義
# main.pyの内容をこちらに移動する
class TimelinePage:
    def __init__(self, page):
        self.page = page
        self.today = datetime.date.today()
        self.handle_change = Handlers.handle_change
        self.date_component = DateComponent(
            page, self.today, lambda e: self.handle_change(e, self.today, self.Date)
        )
        self.Date = self.date_component.create()

        self.model = DataModel()
        self.phNameList = self.model.load_data(page)

        # pageにて共通のcount_dictを定義しておく
        self.count_dict = self.model.count_dict()

        self.comment_dict = {}

        # deletebutton
        # main.pyを参照にdeleteButtonを追加
        self.delete_buttons = [
            ft.IconButton(
                icon=ft.icons.DELETE_OUTLINE,
                visible=False,
                icon_size=20,
                icon_color="red",
                on_click=lambda e: Handlers.delete_content(
                    e,
                    page,
                    self.phNameList,
                    self.phName,
                    self.delete_buttons,
                    self.drag_data,
                    self.count_dict,
                    self.comment_dict,
                    self.columns,
                    self.draggable_data_for_move,
                    self.comments,
                    self.model.times(),  # delete_contentでの引数ではtimes
                    self.comment,
                ),
            )
            for _ in range(len(self.model.times()))
        ]

        # editbutton
        # main.pyを参照にeditButtonを追加
        self.editButton = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_size=20,
            on_click=lambda e: Handlers.toggle_delete_button(page, self.delete_buttons),
        )

        self.ineditButton = ft.Row(
            controls=[self.editButton],
            alignment=ft.alignment.center,
        )

        self.drag_data = {}

        self.comments = [
            ft.IconButton(
                icon=ft.icons.COMMENT,
                on_click=lambda e: Handlers.create_dialog_for_comment(
                    e, self.comments, self.dlg, self.comment_dict, self.page
                ),
            )
            for _ in range(len(self.model.times()))
        ]

        self.comment = ft.IconButton(
            icon=ft.icons.COMMENT,
            on_click=lambda e: Handlers.dlg_open(e),
        )

        self.comment_field = ft.TextField(label="その他")

        self.dlg = ft.AlertDialog(
            title=ft.Text("Comment"),
            content=self.comment_field,
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: Handlers.add_comment_for_dict(
                        e, self.dlg, self.comment_field, self.page
                    ),
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: Handlers.dlg_close(e, self.dlg, self.page),
                ),
            ],
        )

        self.save_button = ft.ElevatedButton(
            text="Save", on_click=lambda e: self.select_directory.get_directory_path()
        )
        self.select_directory = ft.FilePicker(
            on_result=lambda e: Handlers.write_csv_file(
                e,
                self.model.times(),
                self.model.amTime(),
                self.today,
                self.columns,
                self.drag_data,
                self.count_dict,
                self.amDropDown,
                self.pmDropDown,
                self.phName,
                self.page,
                self.comment_dict,
                self.select_directory,
            )
        )
        page.overlay.append(self.select_directory)

        self.selectColumns = []
        for kind in self.model.draggable_data().values():
            self.selectColumns.append(
                ft.Column(
                    [
                        ft.Draggable(
                            group="timeline",
                            content=ft.Container(
                                ft.Text(kind["task"], color="white"),
                                width=100,
                                height=70,
                                bgcolor=ft.colors.BLUE_GREY_500,
                                border_radius=5,
                            ),
                            data={"task": kind},
                        ),
                    ],
                    col={"sm": 3, "md": 2, "xl": 1},
                    spacing=0,
                    data={"task": kind},
                )
            )
        # 初期状態は 3を選択した状態 offの状態
        # 表示
        self.selectColumns[12].visible = True  # 委員会
        self.selectColumns[13].visible = True  # 勉強会参加
        self.selectColumns[14].visible = True  # WG活動
        self.selectColumns[15].visible = True  # 1on1

        self.selectColumns[26].visible = True  # 13:15業務調整
        self.selectColumns[27].visible = True  # 休憩
        self.selectColumns[28].visible = True  # その他
        # 非表示
        self.selectColumns[0].visible = False  # 情報収集　指導
        self.selectColumns[1].visible = False  # 指導記録作成
        self.selectColumns[2].visible = False  # 混注時間
        self.selectColumns[3].visible = False  # 薬剤セット数
        self.selectColumns[4].visible = False  # 持参薬を確認
        self.selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
        self.selectColumns[6].visible = False  # 処方代理修正
        self.selectColumns[7].visible = False  # TDM実施
        self.selectColumns[8].visible = False  # カンファレンス
        self.selectColumns[9].visible = False  # 医師からの相談
        self.selectColumns[10].visible = False  # 看護師からの相談
        self.selectColumns[11].visible = False  # その他の職種からの相談

        self.selectColumns[16].visible = False  # ICT/AST
        self.selectColumns[17].visible = False  # 褥瘡
        self.selectColumns[18].visible = False  # TPN評価
        self.selectColumns[19].visible = False  # TPN評価
        self.selectColumns[20].visible = False  # 手術使用薬剤確認
        self.selectColumns[21].visible = False  # 手術使用薬剤準備
        self.selectColumns[22].visible = False  # 周術期薬剤管理関連
        self.selectColumns[23].visible = False  # 手術使用麻薬確認・補充
        self.selectColumns[24].visible = False  # 術後疼痛管理チーム回診
        self.selectColumns[25].visible = False  # 脳卒中ホットライン対応

        self.selectColumns[29].visible = False  # 管理業務

        self.time_for_visual_label = []

        for i in self.model.time_for_visual():
            self.time_for_visual_label.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(i, size=10),
                        ],
                        width=50,
                    )
                )
            )

        self.columns = [ft.Container() for _ in range(len(self.model.times()))]
        # 辞書データがmove関数発動ごとに更新されないようにmainにて定義しておく
        self.draggable_data_for_move = self.model.draggable_data()
        for i, column in enumerate(self.columns):
            column.content = ft.DragTarget(
                group="timeline",
                content=ft.Container(
                    width=50,
                    height=300,
                    bgcolor=ft.colors.BLUE_50,
                    border_radius=5,
                ),
                on_accept=lambda e: Handlers.drag_accepted(
                    e,
                    self.page,
                    self.draggable_data_for_move,
                    self.delete_buttons,
                    self.columns,
                    self.comments,
                    self.model.times(),
                    self.drag_data,
                    self.comment,
                    self.count_dict,
                ),
                data={"time": self.model.times()[i], "num": i, "task": ""},
            )

        # ampmSelecticon
        self.iconforampmselect = ft.Icon(
            ft.icons.SCHEDULE,
        )
        self.amDropDown = AmDropDown().create()
        self.pmDropDown = PmDropDown().create()
        self.ampmSelect = ft.Row(
            controls=[
                self.amDropDown,
                ft.Container(height=20, width=10),
                self.pmDropDown,
            ],
        )

        self.TimeLine = ft.Row(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(controls=self.time_for_visual_label),
                        ft.Row(controls=self.columns),
                    ],
                ),
            ],
        )

        self.TimeLine.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.MaterialState.HOVERED: ft.colors.AMBER,
                    ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                },
                track_visibility=True,
                track_border_color=ft.colors.BLUE,
                thumb_visibility=True,
                thumb_color={
                    ft.MaterialState.HOVERED: ft.colors.RED,
                    ft.MaterialState.DEFAULT: ft.colors.GREY_300,
                },
                thickness=30,
                radius=15,
                main_axis_margin=5,
                cross_axis_margin=10,
            ),
        )

        # TimelinePageのviewを返す
        self.name_dropdown = NameDropdown(
            self.page,
            self.phNameList,
            dropdown_changed=lambda e: Handlers.dropdown_changed(
                e, self.phName, self.dialog, self.page
            ),
        )
        self.phName = self.name_dropdown.create()
        Handlers.update_dropdown(self.phName, self.phNameList, page)

        self.end_Drawer = EndDrawer(page)
        self.endDrawer = self.end_Drawer.create()
        self.iconforphName = ft.Icon(
            ft.icons.ACCOUNT_CIRCLE,
        )

        self.colPhName = ft.Column(
            [
                self.iconforphName,
                self.phName,
            ]
        )

        if self.phNameList is not None:
            for name in self.phNameList:
                self.endDrawer.controls.append(
                    ft.Row(
                        [
                            ft.Container(width=10),
                            ft.Text(name, size=15),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                on_click=lambda e: Handlers.delete_name(e),
                                data=name,
                            ),
                        ]
                    )
                )
        self.colampmSelect = ft.Column([self.iconforampmselect, self.ampmSelect])
        self.name_field = ft.TextField(label="新しく追加する名前を入力してください")

        self.dialog = ft.AlertDialog(
            title=ft.Text("Add Name"),
            content=self.name_field,
            actions=[
                ft.TextButton(
                    "追加",
                    on_click=lambda e: Handlers.add_name(
                        e,
                        self.phNameList,
                        self.name_field,
                        page,
                        self.phName,
                        self.dialog,
                    ),
                ),
                ft.TextButton(
                    "キャンセル",
                    on_click=lambda e: Handlers.close_dialog(e, self.dialog, page),
                ),
            ],
        )

        # 業務選択のcupertinoSlidingSegmentedButtonは全て一つにまとめる
        self.choice_button = ft.CupertinoSlidingSegmentedButton(
            selected_index=3,
            thumb_color=ft.colors.BLUE_GREY_100,
            on_change=lambda e: Handlers.change_choice_button(
                e, self.selectColumns, page
            ),
            padding=ft.padding.symmetric(0, 10),
            controls=[
                ft.Text("病棟担当者"),
                ft.Text("1,2F"),
                ft.Text("役職者・管理業務"),
                ft.Text("off"),
                ft.Text("ICT/AST"),
                ft.Text("NST"),
            ],
        )

    # TimelinePageのviewを返す
    def create(self):
        return View(
            "/",  # TimelinePageのURL
            [
                self.Date,
                self.dialog,
                ft.Row(
                    controls=[
                        self.colPhName,
                        ft.Container(height=20, width=50),
                        self.colampmSelect,
                        self.choice_button,
                    ]
                ),
                self.ineditButton,
                self.TimeLine,
                ft.ResponsiveRow(
                    controls=self.selectColumns,
                    run_spacing={"xs": 10},
                ),
                self.save_button,
                ft.CupertinoNavigationBar(
                    selected_index=0,
                    bgcolor=ft.colors.BLUE_GREY_50,
                    inactive_color=ft.colors.GREY,
                    active_color=ft.colors.BLACK,
                    on_change=lambda e: Handlers_Main().on_navigation_change(
                        e, self.page
                    ),
                    destinations=[
                        ft.NavigationBarDestination(
                            icon=ft.icons.CREATE,
                            label="Create",
                            selected_icon=ft.icons.BORDER_COLOR,
                        ),
                        ft.NavigationBarDestination(
                            icon=ft.icons.SHOW_CHART,
                            label="Showchart",
                            selected_icon=ft.icons.AUTO_GRAPH,
                        ),
                        ft.NavigationBarDestination(
                            icon=ft.icons.SETTINGS,
                            selected_icon=ft.icons.SETTINGS_SUGGEST,
                            label="Settings",
                        ),
                    ],
                ),
            ],
            scroll=ScrollMode.AUTO,
        )
