import flet as ft
from flet import View, Page, ScrollMode
import datetime
from components.components import (
    DateComponent,
    NameDropdown,
    EndDrawer,
    AmDropDown,
    PmDropDown,
    ReloadDrawer,
)
from handlers.timeline.handlers import Handlers
from handlers.timeline.temp_save import Temp_Save
from handlers.timeline.handdrag_will_accept import Add_will_accept
from handlers.timeline.drag_leave import DragLeave
from handlers.timeline.reload_data import ReloadDataHandler
from handlers.handlersMain import Handlers_Main
from handlers.pageScroll import Scroll
from handlers.setting.task_set import Set_Default_task
from models.models import DataModel
# timelinepageのviewを定義
# main.pyの内容をこちらに移動する
class TimelinePage:
    def __init__(self, page):
        self.page = page
        self.handle_change = Handlers.handle_change
        self.today = datetime.date.today()
        self.date_component = DateComponent(
            page, self.today, lambda e: self.handle_change(e, self.Date,page)
        )
        self.Date = self.date_component.create()
        
        self.date_component_includeicon = ft.Column(
            controls = [
                ft.Icon(ft.icons.CALENDAR_MONTH),
                self.Date,
                ],
            width = 130,
        )
        
        self.model = DataModel()
        self.phNameList = self.model.load_data(page)
        self.today = datetime.date.today()
        # pageにて共通のcount_dictを定義しておく
        self.count_dict = self.model.count_dict()
        self.draggable_data = self.model.draggable_data()
        self.comment_dict = {}

        # deletebutton
        # main.pyを参照にdeleteButtonを追加
        """
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
                data = {"num":i}
            )
            for i in range(len(self.model.times()))
        ]
        """
        # editbutton
        # main.pyを参照にeditButtonを追加
        self.editButton = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_size=25,
            selected_icon  = ft.icons.DELETE,
            selected_icon_color = "red",
            on_click=lambda e: Handlers.toggle_delete_button(e=e,page=page, columns=self.columns),
        )
        
        self.reloadData = ft.IconButton(
            icon = ft.icons.STORAGE,
            icon_size = 25,
            on_click = lambda e:ReloadDataHandler.toggle_Reload_Data(
                e=e,
                page=self.page,
                calender=self.Date,
                drawer=self.reloadDrawer,
                columns=self.columns, #open_saved_data内で使用
                draggable_data_for_move=self.draggable_data_for_move,
                comments=self.comments,
                model_times=self.model.times(),
                drag_data=self.drag_data,
                comment=self.comment,
                count_dict=self.count_dict,
                phName=self.phName,
                custumDrawerAm= self.custumDrawerAm,
                custumDrawerPm=self.custumDrawerPm,
                phNameList=self.phNameList,
                comment_dict=self.comment_dict,
                draggable_data=self.model.draggable_data(),
                require_name=self.require_name,
                require_location=self.require_location,
                )
        )

        self.ineditButton = ft.Row(
            controls=[
                self.editButton,
                self.reloadData,
                ft.Container(width = 60),
                ],
            alignment=ft
            .MainAxisAlignment.END,
            spacing = 10,
        )

        self.drag_data = {}

        self.comments = [
            ft.IconButton(
                icon=ft.icons.COMMENT,
                on_click=lambda e: Handlers.create_dialog_for_comment(
                    e=e,
                    comments=self.comments,
                    dlg=self.dlg,
                    comment_dict=self.comment_dict,
                    comment_field=self.comment_field,
                    page=self.page,
                ),
                data={"time": self.model.times()[i], "num": i},
            )
            for i in range(len(self.model.times()))
        ]

        self.comment = ft.IconButton(
            icon=ft.icons.COMMENT,
            on_click=lambda e: Handlers.dlg_open(e=e),
        )

        self.comment_field = ft.TextField(label="その他")

        self.dlg = ft.AlertDialog(
            title=ft.Text("内容を入力"),
            content=self.comment_field,
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: Handlers.add_comment_for_dict(
                        e=e,
                        dlg=self.dlg,
                        comment_dict=self.comment_dict,
                        comment_field=self.comment_field,
                        page=self.page
                    ),
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: Handlers.dlg_close(
                        e=e, 
                        dlg=self.dlg,
                        page=self.page),
                ),
            ],
        )
        self.temp_save_message = ft.Container(
            ft.Row(
                controls = [
                    ft.Icon(ft.icons.CHECK,color = "green",visible = False),
                    ft.Text("一時保存が完了しました",color = "green",visible = False),
                ]
            )
        )
        self.temp_save_button = ft.ElevatedButton(
            text = "一時保存",
            on_click = lambda e: Temp_Save.on_save(
                e=e,
                times = self.model.times(),
                amTime = self.model.amTime(),
                select_day = self.Date,
                columns = self.columns,
                drag_data = self.drag_data,
                count_dict = self.count_dict,
                custumDrawerAm = self.custumDrawerAm,
                custumDrawerPm = self.custumDrawerPm,
                phName = self.phName,
                page = self.page,
                comment_dict = self.comment_dict,
                message=self.temp_save_message,
            )
        )
        
        
        self.require_name = ft.Container(ft.Text("名前を選択してください", color="red"))
        self.require_location = ft.Container(ft.Text("病棟を選択してください",color = "red"))
        self.save_message = ft.Container(ft.Row(
            controls=[
                ft.Icon(ft.icons.CHECK,color  = "green",visible = False ),
                ft.Text("保存が完了しました", color="green", visible=False),
            ]
        ))
        self.save_button = ft.ElevatedButton(
            text="保存", on_click=lambda e: self.select_directory.get_directory_path()
        )
        
        
        self.save_error_message = ft.Container()
        self.select_directory = ft.FilePicker(
            on_result=lambda e: Handlers.write_csv_file(
                e=e,
                times=self.model.times(),
                amTime=self.model.amTime(),
                select_day=self.Date,
                columns=self.columns,
                drag_data=self.drag_data,
                count_dict=self.count_dict,
                amDropDown=self.amDropDown,
                pmDropDown=self.pmDropDown,
                custumDrawerAm= self.custumDrawerAm,
                custumDrawerPm=self.custumDrawerPm,
                phName=self.phName,
                page=self.page,
                comment_dict=self.comment_dict,
                select_directory=self.select_directory,
                save_error_message=self.save_error_message,
                today=self.today,
                require_location=self.require_location,
                require_name=self.require_name,
                save_message = self.save_message,
            )
        )
        
        page.overlay.append(self.select_directory)

        self.selectColumns = []
        from flet import TextAlign
        for kind in self.model.draggable_data().values():
            self.selectColumns.append(
                ft.Column(
                    [
                        ft.Draggable(
                            group="timeline",
                            content=ft.Container(
                                ft.Text(
                                    kind["task"],
                                    color="white",
                                    text_align = TextAlign.CENTER,
                                    ),
                                width=100,
                                height=70,
                                bgcolor=Handlers.change_color(kind["task"]),
                                border_radius=ft.border_radius.only(top_left = 10,bottom_right = 10),
                            ),
                            data={"task": kind},
                        ),
                    ],
                    col={"sm": 3, "md": 2, "xl": 1},
                    spacing=3,
                    data={"task": kind},
                )
            )
        # 初期状態は 3を選択した状態 offの状態
        # 表示
        self.selectColumns[12].visible = True  # 委員会
        self.selectColumns[13].visible = True  # 勉強会参加
        self.selectColumns[14].visible = True  # WG活動
        self.selectColumns[15].visible = True  # 1on1

        self.selectColumns[26].visible = True  # 業務調整
        self.selectColumns[27].visible = True  # 休憩
        self.selectColumns[28].visible = True  # その他
        # 非表示
        self.selectColumns[0].visible = False  # 情報収集　指導
        self.selectColumns[1].visible = False  # 指導記録作成
        self.selectColumns[2].visible = False  # 混注時間
        self.selectColumns[3].visible = False  # 薬剤セット・確認
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
        self.selectColumns[30].visible = False  # NST

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
                    height=350,
                    bgcolor="#CBDCEB",
                    border_radius=5,
                ),
                on_accept=lambda e: Handlers.drag_accepted(
                    e=e,
                    page=self.page,
                    draggable_data_for_move=self.draggable_data_for_move,
                    columns=self.columns,
                    comments=self.comments,
                    times=self.model.times(),
                    drag_data=self.drag_data,
                    comment=self.comment,
                    count_dict=self.count_dict,
                    phNameList=self.phNameList,
                    phName=self.phName,
                    comment_dict=self.comment_dict,
                    draggable_data=self.draggable_data,
                ),
                on_will_accept=lambda e: Add_will_accept.drag_will_accept(
                        e=e,
                        page=self.page,
                        columns=self.columns,
                        drag_data=self.drag_data,
                        ),
                on_leave = lambda e:DragLeave.drag_leave(e,page),
                data={"time": self.model.times()[i], "num": i, "task": ""},
            )
        # ampmSelecticon
        self.iconforampmselect = ft.Icon(
            ft.icons.SCHEDULE,
        )
        
        self.amDropDown = ft.TextButton(
            "AM",
            on_click=lambda e: Handlers.open_Drawer(
                e=e,
                customDrawerTile=self.custumDrawerAmTitle ,
                customDrawer= self.custumDrawerAm, 
                page = self.page),
        )
        self.pmDropDown = ft.TextButton(
            "PM",
            on_click=lambda e: Handlers.open_Drawer(
                e=e,
                customDrawerTile=self.custumDrawerPmTitle,
                customDrawer=self.custumDrawerPm,
                page=self.page),
        )
        self.ampmSelect = ft.Row(
            controls=[
                self.amDropDown,
                ft.Container(height=20, width=10),
                self.pmDropDown,
            ],
        )
        self.custumDrawerAmTitle = ft.ResponsiveRow(
            controls=[
                ft.Text("AM"),
                ft.Divider(),
            ]
        )
        self.custumDrawerAmTitle.visible = False
        
        self.custumDrawerAm = ft.Container()
        self.custumDrawerAm.visible = False
        self.custumDrawerAm.content = AmDropDown().create(self.require_location,self.page)

        self.custumDrawerPmTitle = ft.ResponsiveRow(
            controls = [
                ft.Text("PM"),
                ft.Divider(),
            ]
        )
        self.custumDrawerPmTitle.visible = False
        self.custumDrawerPm = ft.Container()
        self.custumDrawerPm.visible = False
        self.custumDrawerPm.content = PmDropDown().create(self.require_location,self.page)

        self.TimeLine = ft.Row(
            scroll = ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(controls=self.time_for_visual_label),
                        ft.Row(controls=self.columns),
                    ],
                ),
            ],
        )
        
        
        #スクロールボタンを実装してみる
        #コンテンツの左移動するボタン
        self.backscrollButton = ft.ElevatedButton(
            content = ft.Icon(ft.icons.ARROW_BACK_IOS),
            width = 450,
            on_click = lambda _:self.TimeLine.scroll_to(delta = -100,duration = 200)
        )
        #コンテンツ右移動まで移動するボタン
        self.forwardscrollButton = ft.ElevatedButton(
            content = ft.Icon(ft.icons.ARROW_FORWARD_IOS),
            width = 450,
            on_click  = lambda _ :self.TimeLine.scroll_to(delta = 100,duration = 200) #self.TimeLine.scroll_to(delta = 40,duration = 200)
        )
        #deltaが効くのなら+ と-で左右にスクロールできればいい
        #Timelineの外側に置くたwめにさらに囲む必要
        self.scrollButton = ft.Row(
            [
                self.backscrollButton,
                self.forwardscrollButton,
            ],
            ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        #scrollmode的に難しい？
        #オーバーレイ表示が聞けば上に載せられる？
        #pageでなくて、Timeline上のオーバーレイとすれば効く？
        #とりあえず下に配置してみて、オーバーレイ表示を実装する
        #スクロールボタンはできたので一度コミット crossaxisalignment
        #ボタンを並べた上でバラバラにalignmentを設定？
        
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
                e=e,
                phName=self.phName,
                dialog=self.dialog, 
                page=self.page,
                require_error_message=self.require_name,
            ),
        )
        self.phName = self.name_dropdown.create()
        
        #settingpageの設定に基づいてデフォルトで業務を登録する
        Set_Default_task.set_default_task(
            page=page,
            columns=self.columns,
            phNameList=self.phNameList,
            phName=self.phName,
            drag_data=self.drag_data,
            count_dict=self.count_dict,
            comment_dict=self.comment_dict,
            draggable_data_for_move=self.draggable_data_for_move,
            comments=self.comments,
            comment=self.comment,
            draggable_data=self.model.draggable_data()
            )
        
        Handlers.update_dropdown(
            phName=self.phName,
            phNameList=self.phNameList,
            page=page)

        self.end_Drawer = EndDrawer(page)
        self.endDrawer = self.end_Drawer.create()
        #読み出し用ドロワーの作成
        self.reloadDrawer = ReloadDrawer(page).create()
        #page_client_dataがあるときに読み出し用ドロワーに保管しているデータを表示する
        #コントロール部分　ft.Row ft.Containerを追加していく

            
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
        self.choice_button = ft.Container(
            content=ft.CupertinoSlidingSegmentedButton(
                selected_index=3,
                thumb_color="#CBDCEB",
                on_change=lambda e: Handlers.change_choice_button(
                    e, self.selectColumns, page
                ),
                padding=ft.padding.symmetric(0, 10),
                controls=[
                    ft.Text("病棟担当者"),
                    ft.Text("1,2F"),
                    ft.Text("役職者・管理業務"),
                    ft.Text("その他"),
                    ft.Text("ICT/AST"),
                    ft.Text("NST"),
                ],
            ),
            alignment = ft.alignment.center,
        )
        
        self.contents_list = View(
            "/",  # TimelinePageのURL
            [
                self.dialog,
                ft.Row(
                    controls=[
                        self.colPhName,
                        ft.Container(height=20, width=50),
                        self.date_component_includeicon,
                        ft.Container(height=20, width=50),
                        self.colampmSelect,
                    ]
                ),
                self.custumDrawerAmTitle,
                self.custumDrawerAm,
                self.custumDrawerPmTitle,
                self.custumDrawerPm,
                self.ineditButton,
                self.choice_button, 
                self.TimeLine,
                self.scrollButton,
                ft.ResponsiveRow(
                    controls=self.selectColumns,
                    run_spacing={"xs": 10},
                ),
                self.require_name,
                self.require_location,
                self.temp_save_message,
                self.temp_save_button,
                self.save_message,
                self.save_button,
                self.save_error_message,
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
            on_scroll_interval = 4,
            end_drawer=self.reloadDrawer,
        )
        
        
    
    # TimelinePageのviewを返す
    def create(self):
        return self.contents_list