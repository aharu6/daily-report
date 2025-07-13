import flet as ft
from flet import View, Page
import datetime
import math

# Calendar関連のクラスをインポート
from .calendar.create_calendar import CreateCalendar
from .calendar.read_folder import ReadFolder  
from .calendar.update_card import UpdateCard
from .calendar.update_calendar import UpdateCalendar
from .calendar.tab_content_creator import TabContentCreator
from handlers.handlersMain import Handlers_Main

class CalenderPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.schedule_data = []
        
        # 現在の日付を取得
        self.today = datetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        
        # 病棟ラベル
        self.locate_labels = [
            "ICU", "OR", "HR", "1E", "3A", "3B", "3C", "CCU",
            "4A", "4B", "4C", "4D", "HCU",
            "5A", "5B", "5C", "5D", "DI"
        ]

    def create(self):
        """カレンダーページのViewを作成"""
        
        # フォルダ名表示
        folder_name = ft.Text(
            "選択中のフォルダ名",
        )
        
        # 病棟絞り込みと名前絞り込み機能の切り替え
        change_filter = ft.Switch(
            label="病棟絞り込み",
            value=True,
        )

        # タブを作成
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text=label, 
                    content=TabContentCreator.create_tab_content(
                        label=label, 
                        page=self.page, 
                        schedule_data=self.schedule_data,
                        switch_value=None
                    )
                ) for label in self.locate_labels
            ],
            expand=True,
            animation_duration=300,
            indicator_color=ft.colors.BLUE,
        )

        # ファイルピッカー
        file_picker = ft.FilePicker(
            on_result=self._handle_folder_selection,
        )
        
        # オーバーレイに追加（エラーハンドリング付き）
        try:
            if hasattr(self.page, 'overlay') and file_picker not in self.page.overlay.controls:
                self.page.overlay.append(file_picker)
        except Exception as e:
            print(f"FilePicker overlay error: {e}")
        
        # フォルダ読み込みボタン
        read_folder_button = ft.ElevatedButton(
            text="読み込むフォルダを選択",
            on_click=lambda _: file_picker.get_directory_path(),
            icon=ft.icons.FOLDER_OPEN,
        )

        # フィルター変更ハンドラー
        def handle_filter_change(e):
            if e.control.value == True:
                # 病棟絞り込みモード
                tabs.tabs = [
                    ft.Tab(
                        text=label, 
                        content=TabContentCreator.create_tab_content(
                            label=label, 
                            page=self.page, 
                            schedule_data=self.schedule_data,
                            switch_value=None
                        )
                    ) for label in self.locate_labels
                ]
            elif e.control.value == False:
                # 個人名絞り込みモード
                tabs.tabs = [ft.Tab(
                    text="個人名絞り込み",
                    content=TabContentCreator.create_tab_content(
                        label="個人名絞り込み",
                        page=self.page,
                        schedule_data=self.schedule_data,
                        switch_value=e.control.value
                    )
                )]
            tabs.update()
        
        change_filter.on_change = handle_filter_change

        # メインコンテンツ
        main_content = ft.Column(
            [
                ft.Text("Calendar", size=30, weight=ft.FontWeight.BOLD),
                read_folder_button,
                folder_name,
                change_filter,
                tabs,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # ナビゲーションバー
        navigation_bar = ft.CupertinoNavigationBar(
            selected_index=2,  # Calendarタブを選択状態に
            bgcolor=ft.colors.BLUE_GREY_50,
            inactive_color=ft.colors.GREY,
            active_color=ft.colors.BLACK,
            on_change=lambda e: Handlers_Main().on_navigation_change(e, self.page),
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.TIMELINE,
                    label="Timeline",
                    selected_icon=ft.icons.BORDER_COLOR,
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.AUTO_GRAPH,
                    label="Chart",
                    selected_icon=ft.icons.AUTO_GRAPH,
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.CALENDAR_MONTH,
                    label="Calendar",
                    selected_icon=ft.icons.CALENDAR_TODAY,
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SETTINGS,
                    label="Settings",
                    selected_icon=ft.icons.SETTINGS,
                ),
            ],
        )

        # 起動時のフォルダ読み込み処理
        self._load_stored_folder(folder_name)

        # データがある場合の初期化処理
        if self.schedule_data:
            try:
                # 最初のタブのカードリストを取得して更新
                first_tab_content = tabs.tabs[0].content
                if hasattr(first_tab_content, 'controls') and len(first_tab_content.controls) > 2:
                    calendar_controls = first_tab_content.controls[2].controls
                    
                    UpdateCard.update_cards_with_schedule_data(
                        schedule_data=self.schedule_data,
                        e=None,
                        page=self.page,
                        card_name=self.locate_labels[0],
                        card=calendar_controls
                    )
                    
                    UpdateCalendar.update_calendar_with_schedule_data(
                        e=None,
                        schedule_data=self.schedule_data,
                        page=self.page,
                        calendar=calendar_controls[1:],
                        card_name=self.locate_labels[0],
                        filter_name=None
                    )
            except Exception as e:
                print(f"初期化エラー: {e}")

        return View(
            "/calendar",
            controls=[
                main_content,
                navigation_bar,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def _handle_folder_selection(self, e):
        """フォルダ選択時の処理"""
        if e.path:
            # ReadFolder.read_folderを使用してデータを読み込み
            ReadFolder.read_folder(
                e=e,
                schedule_data=self.schedule_data,
                page=self.page,
                folder_name=None,  # folder_nameは後で更新
                checkboxes=None
            )

    def _load_stored_folder(self, folder_name):
        """起動時の保存済みフォルダ読み込み"""
        try:
            stored_folder_path = self.page.client_storage.get("folder_name")
            if stored_folder_path:
                folder_name.value = f"選択中のフォルダ: {stored_folder_path}"
                print(f"読み込み済みのフォルダ: {stored_folder_path}")
                
                # データ読み込み処理
                class MockEvent:
                    def __init__(self, path):
                        self.path = path
                
                mock_event = MockEvent(path=stored_folder_path)
                
                ReadFolder.read_folder(
                    e=mock_event,
                    schedule_data=self.schedule_data,
                    page=self.page,
                    folder_name=folder_name,
                    checkboxes=None
                )
                
                folder_name.update()
        except Exception as e:
            print(f"フォルダの読み込み中にエラーが発生しました: {e}")
            pass
