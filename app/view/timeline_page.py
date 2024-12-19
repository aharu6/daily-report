import flet as ft
from flet import View,Page,ScrollMode
import datetime
from components.components import DateComponent,NameDropdown,EndDrawer,AmDropDown,PmDropDown,EditButton,DeleteButtons
from handlers.handlers import Handlers
from handlers.handlersMain import Handlers_Main
from handlers.handlers_chart import Handlers_Chart
from models.models import DataModel
from view.setting_page import SettingPage
#timelinepageのviewを定義
#main.pyの内容をこちらに移動する
class TimelinePage:
    def __init__(self,page):        
        self.page = page
        self.today = datetime.date.today()
        self.handle_change = Handlers.handle_change
        self.date_component = DateComponent(page,self.today,lambda e:self.handle_change(e,self.today,self.Date))
        self.Date = self.date_component.create()
        
        self.model = DataModel()
        self.phNameList = self.model.load_data(page)
        
        #pageにて共通のcount_dictを定義しておく
        self.count_dict = self.model.count_dict()
        
        self.comment_dict = {}
        
        #deletebutton
        #main.pyを参照にdeleteButtonを追加
        self.delete_buttons = [
            ft.IconButton(
                icon = ft.icons.DELETE_OUTLINE,
                visible = False,
                icon_size = 20,
                icon_color = "red",
                on_click = lambda e:Handlers.delete_content(e,page,self.phNameList,self.phName,self.delete_buttons,
                                        self.drag_data,
                                        self.count_dict,self.comment_dict,self.columns)
            )
            for _ in range(len(self.model.times()))
        ]
        
        #editbutton
        #main.pyを参照にeditButtonを追加
        self.editButton = ft.IconButton(
            icon = ft.icons.DELETE_OUTLINE,
            icon_size = 20,
            on_click = lambda e:Handlers.toggle_delete_button(page,self.delete_buttons),
            )
        
        self.ineditButton = ft.Row(
            controls = [self.editButton],
            alignment = ft.MainAxisAlignment.END,
        )
        
        self.drag_data = {}
        
        self.comments = [
            ft.IconButton(
                icon = ft.icons.COMMENT,
                on_click = lambda e:Handlers.create_dialog_for_comment(
                    e,self.comments,self.dlg,self.comment_dict,
                    self.page
                    ),
            )
            for _ in range(len(self.model.times()))
        ]
        
        self.comment = ft.IconButton(
            icon = ft.icons.COMMENT,
            on_click = lambda e:Handlers.dlg_open(e),
        )
        
        
        self.comment_field = ft.TextField(label = "その他")
        
        self.dlg = ft.AlertDialog(
            title = ft.Text("Comment"),
            content = self.comment_field,
            actions = [
                ft.TextButton(
                    "OK",
                    on_click = lambda e:Handlers.add_comment_for_dict(e,self.dlg,self.comment_field,self.page)
                ),
                ft.TextButton(
                    "Cancel",
                    on_click = lambda e:Handlers.dlg_close(e,self.dlg,self.page)
                ),
            ]
        )
        
        self.save_button = ft.ElevatedButton(
            text = "Save",
            on_click = lambda e:self.select_directory.get_directory_path()
        )
        self.select_directory = ft.FilePicker(
            on_result = lambda e:Handlers.write_csv_file(
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
                self.select_directory)
        )
        page.overlay.append(self.select_directory)
        
        self.selectColumns = []
        for kind in self.model.draggable_data().values():
            self.selectColumns.append(
                ft.Column(
                    [
                        ft.Draggable(
                            group = "timeline",
                            content = ft.Container(
                                ft.Text(kind["task"],color= "white"),
                                width = 100,
                                height = 70,
                                bgcolor = ft.colors.BLUE_GREY_500,
                                border_radius = 5,
                            ),
                            data = {"task":kind},
                        ),
                    ],
                    spacing = 0,
                    data = {"task":kind},
                )
            )
            
        self.time_for_visual_label = []
        
        for i in self.model.time_for_visual():
            self.time_for_visual_label.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.Text(i,size = 10),
                        ],
                        width = 50,
                    )
                )
            )
            
        self.columns = [ft.Container() for _ in range(len(self.model.times()))]
        #辞書データがmove関数発動ごとに更新されないようにmainにて定義しておく
        self.draggable_data_for_move = self.model.draggable_data()
        for i ,column in enumerate(self.columns):
            column.content = ft.DragTarget(
                group = "timeline",
                content = ft.Container(
                    width = 50,
                    height = 300,
                    bgcolor = ft.colors.BLUE_50,
                    border_radius = 5,
                ),
                on_accept = lambda e:Handlers.drag_accepted,
                on_move = lambda e:Handlers.drag_move(
                    e,self.page,self.draggable_data_for_move,self.delete_buttons,
                    self.columns,self.comments,
                    self.model.times(),
                    self.drag_data,
                    self.comment,
                    self.count_dict,
                ),
                data = {"time":self.model.times()[i],"num":i,"task":""},
            )
        
        
        #ampmSelecticon
        self.iconforampmselect = ft.IconButton(ft.icons.SCHEDULE,hover_color  =ft.colors.with_opacity(0.0,ft.colors.BLUE_GREY_500))
        self.amDropDown = AmDropDown().create()
        self.pmDropDown = PmDropDown().create()
        self.ampmSelect = ft.Row(
            controls = [self.amDropDown,ft.Container(height = 20,width =10),self.pmDropDown],
        )
        
        self.TimeLine = ft.Row(
            scroll=True,
            controls=[
                ft.Column(
                    controls=[ 
                        ft.Row(controls=self.time_for_visual_label),
                        ft.Row(controls=self.columns),
                    ],
                ),
            ],
        )
        
        
        #TImelinePageのviewを返す
        self.name_dropdown = NameDropdown(self.page,self.phNameList,
                                    dropdown_changed=lambda e: Handlers.dropdown_changed(e,self.phName,self.dialog,self.page))      
        self.phName = self.name_dropdown.create()
        Handlers.update_dropdown(self.phName,self.phNameList,page)
        
        self.end_Drawer = EndDrawer(page)
        self.endDrawer = self.end_Drawer.create()
        self.iconforphName = ft.IconButton(ft.icons.ACCOUNT_CIRCLE,on_click = lambda e:Handlers.drawer_open(e,page,self.endDrawer))
        
        self.colPhName  = ft.Column(
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
                            ft.Container(width = 10),
                            ft.Text(name,size = 15),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                on_click = lambda e:Handlers.delete_name(e),
                                data = name,
                                ) 
                        ]
                    )
            )
        self.colampmSelect = ft.Column([self.iconforampmselect,self.ampmSelect])
        self.name_field = ft.TextField(label = "新しく追加する名前を入力してください")
        
        self.dialog = ft.AlertDialog(
            title = ft.Text("Add Name"),
            content = self.name_field,
            actions = [
                ft.TextButton("追加",on_click= lambda e:Handlers.add_name(e,self.phNameList,self.name_field,page,self.phName,self.dialog)),
                ft.TextButton("キャンセル",on_click = lambda e:Handlers.close_dialog(e,self.dialog,page))
            ],
        )
        
        self.choice_button = ft.CupertinoSlidingSegmentedButton(
            selected_index = 0,
            thumb_color = ft.colors.BLUE_GREY_100,
            on_change = lambda e:Handlers.change_choice_button(e,self.selectColumns,page),
            padding = ft.padding.symmetric(0,10),
            controls = [
                ft.Text("病棟担当者"),
                ft.Text("1,2F"),
            ]
        )
        
        self.special_choice =ft.CupertinoSlidingSegmentedButton(
            selected_index = 2,
            thumb_color = ft.colors.BLUE_GREY_100,
            on_change = lambda e:Handlers.change_special_choice(e,self.selectColumns,page),
            padding = ft.padding.symmetric(0,10),
            controls = [
                ft.Text("ICT/AST"),
                ft.Text("NST"),
                ft.Text("off"),
            ]
        )
        
    
        
    #TimelinePageのviewを返す
    def create(self):
        return View(
            "/", #TimelinePageのURL
            [
                self.Date,
                self.dialog,
                ft.Row(controls = [self.colPhName,ft.Container(height=20, width=50),self.colampmSelect,self.choice_button,self.special_choice]),
                self.ineditButton,
                self.TimeLine,
                ft.Row(scroll = True,controls = self.selectColumns),
                self.save_button,                    
                ft.CupertinoNavigationBar(
                    selected_index = 0,
                    bgcolor=ft.colors.BLUE_GREY_50,
                    inactive_color=ft.colors.GREY,
                    active_color=ft.colors.BLACK,
                    on_change= lambda e:Handlers_Main().on_navigation_change(e,self.page),
                    destinations = [
                        ft.NavigationBarDestination(icon=ft.icons.CREATE, label="Create",selected_icon = ft.icons.BORDER_COLOR),
                        ft.NavigationBarDestination(icon=ft.icons.SHOW_CHART, label="Showchart",selected_icon = ft.icons.AUTO_GRAPH),
                        ft.NavigationBarDestination(icon=ft.icons.SETTINGS,selected_icon= ft.icons.SETTINGS_SUGGEST,label="Settings",),
                    ]   
                )
            ],
            scroll = ScrollMode.AUTO,
        )