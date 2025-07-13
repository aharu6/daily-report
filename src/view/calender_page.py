import flet as ft
from flet import View, Page
import datetime
import math

# Calendar関連のクラスをインポート
from handlers.calender.create_calendar import CreateCalendar
from handlers.calender.read_folder import ReadFolder  
from handlers.calender.update_card import UpdateCard
from handlers.calender.update_calendar import UpdateCalendar
from handlers.calender.tab_content_creator import TabContentCreator
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
        
        # 起動時に保存されたフォルダがある場合は自動読み込み
        auto_loaded = self._auto_load_saved_folder()
        
        if auto_loaded:
            print(f"Calendar page initialized with {len(self.schedule_data)} schedule items")
        else:
            print("Calendar page initialized with no saved data")
        
        # フォルダ名表示
        folder_name = ft.Text(
            "選択中のフォルダ名",
        )
        
        # folder_nameをインスタンス変数として保存
        self.folder_name = folder_name
        
        # 自動読み込みされた場合はフォルダ名を更新
        self._update_folder_name_if_auto_loaded()
        
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
        
        # tabsをインスタンス変数として保存
        self.tabs = tabs

        # ファイルピッカー
        file_picker = ft.FilePicker(
            on_result=self._handle_folder_selection,
        )
        
        # ページにファイルピッカーを追加
        self.page.overlay.append(file_picker)
        self.page.update()
        
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
                self.tabs.tabs = [
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
                self.tabs.tabs = [ft.Tab(
                    text="個人名絞り込み",
                    content=TabContentCreator.create_tab_content(
                        label="個人名絞り込み",
                        page=self.page,
                        schedule_data=self.schedule_data,
                        switch_value=e.control.value
                    )
                )]
            self.tabs.update()
        
        change_filter.on_change = handle_filter_change

        # メインコンテンツ
        main_content = ft.Column(
            [
                ft.Text("記録した日付の確認", size=20, weight=ft.FontWeight.BOLD),
                read_folder_button,
                folder_name,
                change_filter,
                self.tabs,
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

        # 起動時のフォルダ読み込み処理は_auto_load_saved_folderで実行済み

        # Viewを作成
        view = View(
            "/calendar",
            controls=[
                main_content,
                navigation_bar,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        # データがある場合の初期化処理（View作成後に実行）
        if self.schedule_data:
            try:
                # 最初のタブのカードリストを取得して更新
                first_tab_content = self.tabs.tabs[0].content
                if hasattr(first_tab_content, 'controls') and len(first_tab_content.controls) > 2:
                    calendar_controls = first_tab_content.controls[2].controls
                    
                    UpdateCard.update_cards_with_schedule_data(
                        e=None,
                        schedule_data=self.schedule_data,
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
                import traceback
                traceback.print_exc()

        return view

    def _handle_folder_selection(self, e):
        """フォルダ選択時の処理"""
        if e.path:
            # ReadFolder.read_folderを使用してデータを読み込み
            ReadFolder.read_folder(
                e=e,
                schedule_data=self.schedule_data,
                page=self.page,
                folder_name=self.folder_name,
                checkboxes=None
            )
            
            # データ読み込み後にUIを更新
            if self.schedule_data:
                try:
                    # 最初のタブのカードリストを取得して更新
                    if hasattr(self.tabs, 'tabs') and len(self.tabs.tabs) > 0:
                        first_tab_content = self.tabs.tabs[0].content
                        
                        if hasattr(first_tab_content, 'controls') and len(first_tab_content.controls) > 2:
                            calendar_controls = first_tab_content.controls[2].controls
                            
                            # UpdateCard処理
                            UpdateCard.update_cards_with_schedule_data(
                                e=None,
                                schedule_data=self.schedule_data,
                                page=self.page,
                                card_name=self.locate_labels[0],
                                card=calendar_controls
                            )
                            
                            # UpdateCalendar処理
                            UpdateCalendar.update_calendar_with_schedule_data(
                                e=None,
                                schedule_data=self.schedule_data,
                                page=self.page,
                                calendar=calendar_controls[1:],
                                card_name=self.locate_labels[0],
                                filter_name=None
                            )
                            
                            # ページ全体を更新
                            self.page.update()
                        
                except Exception as e:
                    import traceback
                    traceback.print_exc()

    def _auto_load_saved_folder(self):
        """起動時に保存されたフォルダがあれば自動読み込み"""
        try:
            # クライアントストレージから保存されたフォルダパスを取得
            stored_folder_path = self.page.client_storage.get("folder_name")
            
            if stored_folder_path:
                import os
                # フォルダが存在するかチェック
                if os.path.exists(stored_folder_path) and os.path.isdir(stored_folder_path):
                    print(f"Auto-loading saved folder: {stored_folder_path}")
                    
                    # フォルダから最新データを再読み込み（常にフォルダの最新状態を読み込み）
                    self._reload_folder_data(stored_folder_path)
                    
                    # フォルダ名を保存（後で設定用）
                    self._saved_folder_name = f"選択中のフォルダ: {os.path.basename(stored_folder_path)}"
                    
                    return True
                else:
                    # フォルダが存在しない場合、保存されたデータがあれば使用
                    stored_schedule_data = self.page.client_storage.get("schedule_data")
                    if stored_schedule_data:
                        print(f"Folder not found, but using saved data: {len(stored_schedule_data)} items")
                        self.schedule_data.clear()
                        self.schedule_data.extend(stored_schedule_data)
                        
                        self._saved_folder_name = f"選択中のフォルダ: {os.path.basename(stored_folder_path)} (フォルダ移動済み)"
                        return True
                    else:
                        print(f"Saved folder not found and no backup data: {stored_folder_path}")
                        # 無効なパスはクリア
                        self.page.client_storage.remove("folder_name")
                        return False
            else:
                print("No saved folder found")
                return False
                
        except Exception as e:
            print(f"Error during auto-load: {e}")
            return False
    
    def _reload_folder_data(self, folder_path):
        """フォルダからデータを再読み込み"""
        try:
            # MockEventクラスを作成
            class MockEvent:
                def __init__(self, path):
                    self.path = path
            
            mock_event = MockEvent(path=folder_path)
            
            # データを再読み込み
            ReadFolder.read_folder(
                e=mock_event,
                schedule_data=self.schedule_data,
                page=self.page,
                folder_name=self.folder_name,  # フォルダ名テキストを渡す
                checkboxes=None
            )
            
            print(f"Successfully reloaded {len(self.schedule_data)} schedule items")
            
        except Exception as e:
            print(f"Error reloading folder data: {e}")
            # エラーの場合は保存されたデータを使用
            stored_schedule_data = self.page.client_storage.get("schedule_data")
            if stored_schedule_data:
                self.schedule_data.clear()
                self.schedule_data.extend(stored_schedule_data)
                print(f"Fallback to saved data: {len(self.schedule_data)} items")
    
    def _update_folder_name_if_auto_loaded(self):
        """自動読み込みされた場合にフォルダ名を更新"""
        if hasattr(self, '_saved_folder_name') and hasattr(self, 'folder_name'):
            self.folder_name.value = self._saved_folder_name
            try:
                self.folder_name.update()
            except AssertionError:
                # ページに追加されていない場合はスキップ
                pass
