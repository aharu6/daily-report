import flet as ft
from flet import Page,AppBar,View,Text,ScrollMode
import json
import calendar
import csv
import pandas as pd
import sqlite3
import datetime
import sys
from tkinter import filedialog
from components.components import DateComponent,NameDropdown,EndDrawer,AmDropDown,PmDropDown,EditButton,DeleteButtons
from handlers.handlers import Handlers
from models.models import DataModel
# main
def main(page: ft.Page):

    page.title = "Daily Report"
    page.window.width = 1100
    page.scroll = "always"
    
    today = datetime.date.today()
    date_component = DateComponent(page,today,lambda e:Handlers.handle_change(e))
    Date = date_component.create()
    
    model = DataModel()
    phNameList = model.load_data(page)
    #oageにて共通のcount/dictを定義しておく
    count_dict = model.count_dict()
    
    comment_dict = {}

    # editButton    
    delete_buttons = [
        ft.IconButton(
            icon = ft.icons.DELETE_OUTLINE,
            visible = False,
            icon_size = 20,
            icon_color = "red",
            on_click = lambda e:Handlers.delete_content(e,page,phNameList,phName,delete_buttons,
                                        drag_data,
                                        count_dict,comment_dict,columns)
            )
        for _ in range(len(model.times()))
    ]
    
    #editButton
    editButton  = ft.IconButton(
        icon = ft.icons.DELETE_OUTLINE,
        icon_size = 20,
        on_click = lambda e:Handlers.toggle_delete_button(page,delete_buttons),
    )   
    
    ineditButton = ft.Row(
        controls = [editButton],
        alignment = ft.MainAxisAlignment.END,
    )
    
    
    drag_data = {}
    
    comments = [
        ft.IconButton(
            icon = ft.icons.COMMENT,
            on_click = lambda e:Handlers.create_dialog_for_comment(e,comments,dlg,comment_dict,comment_field,page),
            )
        for _ in range(len(model.times()))
    ]
    
    comment = ft.IconButton(
        icon = ft.icons.COMMENT,
        on_click = lambda e:Handlers.dlg_open(e),
    )
    
    
    
    comment_field = ft.TextField(label = "その他")
        
    dlg = ft.AlertDialog(
        title = ft.Text("Comment"),
        content = comment_field,
        actions = [
            ft.TextButton("OK",on_click = lambda e:Handlers.add_comennt_for_dict(e)),
            ft.TextButton("Cancel",on_click = lambda e:Handlers.dlg_close(e)),
        ],
    )
    
    
    save_button = ft.ElevatedButton(text="Save", on_click=lambda e:select_directory.get_directory_path())
    select_directory = ft.FilePicker(on_result = lambda e:Handlers.write_csv_file(e,DataModel().times(),DataModel().amTime(),today,columns,drag_data,count_dict,amDropDown,pmDropDown,phName,page,comment_dict,select_directory))
    page.overlay.append(select_directory)
        
    selectColumns = []
    for kind in model.draggable_data().values():
        selectColumns.append(
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
                        data= {"task":kind},
                    ),
                ],
                spacing = 0,
                data = {"task":kind},
            )
        )

    
    time_for_visual_label  = []
    for i in model.time_for_visual():
        time_for_visual_label.append(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(i, size=10),
                    ]
                )
            )
        )
        
    columns =[ft.Container() for _ in range(len(model.times()))]
    #辞書データがmove関数発動ごとに更新されないようにmainにて定義しておく
    dragabledata_formove = model.draggable_data()
    for i ,column in enumerate(columns):
        column.content = ft.DragTarget(
            group = "timeline",
            content = ft.Container(
                width = 50,
                height = 300,
                bgcolor = None,
                border_radius = 5,
            ),
            on_accept = Handlers.drag_accepted,
            on_move = lambda e:Handlers.drag_move(e,page,dragabledata_formove,delete_buttons,columns,comments,model.times(),drag_data,comment,count_dict),
            data = {"time":model.times()[i],"num":i}
        )
        

    
    
    #ampmSelecticon
    iconforampmselect = ft.Icon(ft.icons.SCHEDULE)
    amDropDown = AmDropDown().create()
    pmDropDown = PmDropDown().create()
    ampmSelect = ft.Row(
        controls = [amDropDown,ft.Container(height = 20,width =10),pmDropDown],
    )

    TimeLine = ft.Row(
        scroll=True,
        controls=[
            ft.Column(
                controls=[ 
                    ft.Row(controls=time_for_visual_label),
                    ft.Row(controls=columns),
                ],
            ),
        ],
    )

    file_picker = ft.FilePicker(on_result=Handlers.pick_file_result)
    page.overlay.append(file_picker)

    selected_files = ft.Text()
    file_picker_Button = ft.ElevatedButton(
        "ファイルを選択",
        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
    )
    
    
    bar_chart = ft.BarChart(
        bar_groups=[],
        border=ft.border.all(1, ft.colors.GREEN_100),
        left_axis=ft.ChartAxis(labels_size=40, title=ft.Text("Count"), title_size=20),
        bottom_axis=ft.ChartAxis(labels_size=40),
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.colors.GREEN_100, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREEN_100),
        max_y=10,
        interactive=True,
        expand=True,
    )
    

    def on_navigation_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/")
        elif selected_index == 1:
            page.go("/chart")
        elif selected_index == 2:
            page.go("/settings")
    
    
    #Timelinepage
    name_dropdown = NameDropdown(page,phNameList,lambda e:Handlers.update_dropdown(NameDropdown,phNameList,page))      
    phName = name_dropdown.create()
    
    end_Drawer = EndDrawer(page)
    endDrawer = end_Drawer.create()
    iconforphName = ft.IconButton(ft.icons.ACCOUNT_CIRCLE,on_click = lambda e:Handlers.drawer_open(e,page,endDrawer))
    colPhName  = ft.Column(
        [
            iconforphName,
            phName,
        ]
    )
    
    if phNameList is not None:
        for name in phNameList:
            endDrawer.controls.append(
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
    colampmSelect = ft.Column([iconforampmselect,ampmSelect])
    name_field = ft.TextField(label = "新しく追加する名前を入力してください")
    
    dialog = ft.AlertDialog(
        title = ft.Text("Add Name"),
        content = name_field,
        actions = [
            ft.TextButton("追加",on_click= lambda e:Handlers.add_name(e,phNameList)),
            ft.TextButton("キャンセル",on_click = lambda e:Handlers.close_dialog())
        ],
    )
    
    choice_button = ft.CupertinoSlidingSegmentedButton(
        selected_index = 0,
        thumb_color = ft.colors.BLUE_GREY_100,
        on_change = lambda e:Handlers.change_choice_button(e,selectColumns,page),
        padding = ft.padding.symmetric(0,10),
        controls = [
            ft.Text("病棟担当者"),
            ft.Text("DI担当者"),
            ft.Text("主任/副主任"),
        ]
    )
    
    special_choice =ft.CupertinoSlidingSegmentedButton(
        selected_index = 2,
        thumb_color = ft.colors.BLUE_GREY_100,
        on_change = lambda e:Handlers.change_special_choice(e,selectColumns,page),
        padding = ft.padding.symmetric(0,10),
        controls = [
            ft.Text("ICT/AST"),
            ft.Text("NST"),
            ft.Text("off"),
        ]
    )
    


    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/", #TimelinePage
                [
                    Date,
                    dialog,
                    ft.Row(controls = [colPhName,ft.Container(height=20, width=50),colampmSelect,choice_button,special_choice]),
                    ineditButton,
                    TimeLine,
                    ft.Row(scroll = True,controls = selectColumns),
                    save_button,
                    file_picker_Button,
                    selected_files,
                    bar_chart,
                    ft.CupertinoNavigationBar(
                        selected_index = 0,
                        bgcolor=ft.colors.BLUE_GREY_50,
                        inactive_color=ft.colors.GREY,
                        active_color=ft.colors.BLACK,
                        on_change= on_navigation_change,
                        destinations = [
                            ft.NavigationBarDestination(icon=ft.icons.CREATE, label="Create",selected_icon = ft.icons.BORDER_COLOR),
                            ft.NavigationBarDestination(icon=ft.icons.SHOW_CHART, label="Showchart",selected_icon = ft.icons.AUTO_GRAPH),
                            ft.NavigationBarDestination(icon=ft.icons.SETTINGS,selected_icon= ft.icons.SETTINGS_SUGGEST,label="Settings",),
                        ]
                    )
                ],
                scroll = ScrollMode.AUTO,
            )
        )
        if page.route == "/chart":
            page.views.clear()
            page.views.append(
                View(
                    "/chart",
                    [
                        #chartPage,
                        ft.CupertinoNavigationBar(
                            selected_index = 1,
                            bgcolor=ft.colors.BLUE_GREY_50,
                            inactive_color=ft.colors.GREY,
                            active_color=ft.colors.BLACK,
                            on_change= on_navigation_change,
                            destinations = [
                                ft.NavigationBarDestination(icon=ft.icons.CREATE, label="Create",selected_icon = ft.icons.BORDER_COLOR),
                                ft.NavigationBarDestination(icon=ft.icons.SHOW_CHART, label="Showchart",selected_icon = ft.icons.AUTO_GRAPH),
                                ft.NavigationBarDestination(icon=ft.icons.SETTINGS,selected_icon= ft.icons.SETTINGS_SUGGEST,label="Settings",),
                            ]
                        )
                    ]
                )
            )
        if page.route == "/settings":
            page.views.clear()
            page.views.append(
                View(
                    "/settings",
                    [
                        #settings,
                        ft.CupertinoNavigationBar(
                            selected_index = 2,
                            bgcolor=ft.colors.BLUE_GREY_50,
                            inactive_color=ft.colors.GREY,
                            active_color=ft.colors.BLACK,
                            on_change= on_navigation_change,
                            destinations = [
                                ft.NavigationBarDestination(icon=ft.icons.CREATE, label="Create",selected_icon = ft.icons.BORDER_COLOR),
                                ft.NavigationBarDestination(icon=ft.icons.SHOW_CHART, label="Showchart",selected_icon = ft.icons.AUTO_GRAPH),
                                ft.NavigationBarDestination(icon=ft.icons.SETTINGS,selected_icon= ft.icons.SETTINGS_SUGGEST,label="Settings",),
                            ]
                        )
                    ]
                )
            )
        page.update()
    
    def view_pop(e):
        page.views.pop()
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.BLUE_GREY_50,
        inactive_color=ft.colors.GREY,
        active_color=ft.colors.BLACK,
        on_change= on_navigation_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.CREATE, label="Create",selected_icon = ft.icons.BORDER_COLOR),
            ft.NavigationBarDestination(icon=ft.icons.SHOW_CHART, label="Showchart",selected_icon=ft.icons.AUTO_GRAPH),
            ft.NavigationBarDestination(
                icon=ft.icons.SETTINGS,
                selected_icon=ft.icons.BOOKMARK,
                label="Settings",
            ),
        ]
    )
    page.go(page.route)
    
ft.app(main)
