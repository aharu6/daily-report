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
        self.folder_name = None  # 初期化時はNone、createメソッドで設定
        # ページレベルでのスクロール設定を削除（Viewレベルで制御）
        
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
        
        # フォルダ名表示を最初に初期化
        folder_name = ft.Text(
            "選択中のフォルダ名",
        )
        
        # folder_nameをインスタンス変数として保存
        self.folder_name = folder_name
        
        # ページ遷移時にフォルダを再読み込み（folder_name初期化後）
        self._reload_folder_on_navigation()
        
        # 起動時に保存されたフォルダがある場合は自動読み込み
        auto_loaded = self._auto_load_saved_folder()
        
        if auto_loaded:
            print(f"Calendar page initialized with {len(self.schedule_data)} schedule items")
            # データが正常に読み込まれた場合、最新データを保存
            self._save_current_data()
        else:
            print("Calendar page initialized with no saved data")
        
        # 自動読み込みされた場合はフォルダ名を更新
        self._update_folder_name_if_auto_loaded()
        
        # 病棟絞り込みと名前絞り込み機能の切り替え
        change_filter = ft.Switch(
            label="病棟絞り込み",
            value=True,
        )

        # タブを作成（expandを削除してスクロールを改善）
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
            # 安全にタブを更新
            try:
                if hasattr(self.tabs, 'page') and self.tabs.page is not None:
                    self.tabs.update()
                else:
                    self.page.update()
            except Exception as tabs_update_error:
                print(f"Error updating tabs in filter change: {tabs_update_error}")
                try:
                    self.page.update()
                except Exception as page_update_error:
                    print(f"Fallback page update failed: {page_update_error}")
        
        change_filter.on_change = handle_filter_change

        # メインコンテンツ（スクロール可能）
        main_content = ft.Column(
            [
                ft.Text("記録した日付の確認", size=20, weight=ft.FontWeight.BOLD),
                read_folder_button,
                folder_name,
                change_filter,
                ft.Container(
                    content=self.tabs,
                    expand=True,
                    height=800,  # 最小高さを指定してスクロール領域を確保
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            on_scroll_interval=4,
            spacing=10,  # 要素間のスペースを追加
        )
        
        # スクロールバーのテーマを設定
        main_content.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.ControlState.HOVERED: ft.colors.AMBER,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                },
                track_visibility=True,
                track_border_color=ft.colors.BLUE,
                thumb_visibility=True,
                thumb_color={
                    ft.ControlState.HOVERED: ft.colors.RED,
                    ft.ControlState.DEFAULT: ft.colors.GREY_300,
                },
                thickness=30,
                radius=15,
                main_axis_margin=5,
                cross_axis_margin=10,
            ),
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

        # Viewを作成（ナビゲーションバーを固定し、メインコンテンツをスクロール可能にする）
        view = View(
            "/calendar",
            controls=[
                ft.Container(
                    content=main_content,
                    expand=True,
                ),
                navigation_bar,
            ],
            scroll=ft.ScrollMode.HIDDEN,  # Viewレベルではスクロールを無効化
        )
        
        # Viewにもスクロールバーテーマを設定
        view.theme = ft.Theme(
            scrollbar_theme=ft.ScrollbarTheme(
                track_color={
                    ft.ControlState.HOVERED: ft.colors.AMBER,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                },
                track_visibility=True,
                track_border_color=ft.colors.BLUE,
                thumb_visibility=True,
                thumb_color={
                    ft.ControlState.HOVERED: ft.colors.RED,
                    ft.ControlState.DEFAULT: ft.colors.GREY_300,
                },
                thickness=30,
                radius=15,
                main_axis_margin=5,
                cross_axis_margin=10,
            ),
        )

        # データがある場合の初期化処理（View作成後に実行）
        if self.schedule_data:
            # UI更新処理を実行
            self._update_ui_after_data_load()
        else:
            print("No schedule data available for UI update")

        return view

    def _handle_folder_selection(self, e):
        """フォルダ選択時の処理"""
        if e.path:
            # schedule_dataをクリアして最新データから読み込み
            self.schedule_data.clear()
            
            # ReadFolder.read_folderを使用してデータを読み込み
            ReadFolder.read_folder(
                e=e,
                schedule_data=self.schedule_data,
                page=self.page,
                folder_name=self.folder_name,
                checkboxes=None
            )
            
            # 正常に読み込めた場合、最新データを保存
            if self.schedule_data:
                self._save_current_data()
                print(f"Folder selection completed with {len(self.schedule_data)} schedule items")
            
            # データ読み込み後にUIを更新
            self._update_ui_after_data_load()

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
                    success = self._reload_folder_data(stored_folder_path)
                    
                    if success:
                        # フォルダ名を保存（後で設定用）
                        self._saved_folder_name = f"選択中のフォルダ: {os.path.basename(stored_folder_path)}"
                        
                        # デバッグ情報出力
                        print(f"Successfully auto-loaded {len(self.schedule_data)} schedule items")
                        for item in self.schedule_data[:5]:  # 最初の5件を表示
                            print(f"  - {item.get('date')}: {item.get('phName')} @ {item.get('locate')}")
                        
                        return True
                    else:
                        print("Failed to reload folder data, trying backup")
                        # 失敗した場合、保存されたデータを使用
                        return self._load_backup_data(stored_folder_path)
                else:
                    print(f"Saved folder not found: {stored_folder_path}")
                    # フォルダが存在しない場合、保存されたデータがあれば使用
                    return self._load_backup_data(stored_folder_path)
            else:
                print("No saved folder found")
                return False
                
        except Exception as e:
            print(f"Error during auto-load: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _load_backup_data(self, original_folder_path):
        """バックアップデータから読み込み"""
        try:
            stored_schedule_data = self.page.client_storage.get("schedule_data")
            if stored_schedule_data:
                print(f"Using backup data: {len(stored_schedule_data)} items")
                self.schedule_data.clear()
                self.schedule_data.extend(stored_schedule_data)
                
                import os
                self._saved_folder_name = f"選択中のフォルダ: {os.path.basename(original_folder_path)} (フォルダ移動済み)"
                return True
            else:
                print("No backup data available")
                # 無効なパスはクリア
                self.page.client_storage.remove("folder_name")
                return False
        except Exception as e:
            print(f"Error loading backup data: {e}")
            return False
    
    def _reload_folder_data(self, folder_path):
        """フォルダからデータを再読み込み"""
        try:
            # データをクリアして最新状態から読み込み
            self.schedule_data.clear()
            
            # MockEventクラスを作成
            class MockEvent:
                def __init__(self, path):
                    self.path = path
            
            mock_event = MockEvent(path=folder_path)
            
            # 読み込み前のアイテム数を記録
            initial_count = len(self.schedule_data)
            
            # folder_nameが存在しない場合はNoneを渡す
            folder_name_ref = getattr(self, 'folder_name', None)
            
            # データを再読み込み
            ReadFolder.read_folder(
                e=mock_event,
                schedule_data=self.schedule_data,
                page=self.page,
                folder_name=folder_name_ref,  # folder_name属性が存在しない場合はNone
                checkboxes=None
            )
            
            final_count = len(self.schedule_data)
            print(f"Successfully reloaded {final_count} schedule items from folder (was {initial_count})")
            
            # データが読み込まれた場合は成功
            if final_count > 0:
                # 正常に読み込めた場合、最新データを保存
                self._save_current_data()
                return True
            else:
                print("Warning: No data loaded from folder")
                return False
            
        except Exception as e:
            print(f"Error reloading folder data: {e}")
            import traceback
            traceback.print_exc()
            
            # エラーの場合は保存されたデータを使用
            stored_schedule_data = self.page.client_storage.get("schedule_data")
            if stored_schedule_data:
                self.schedule_data.clear()
                self.schedule_data.extend(stored_schedule_data)
                print(f"Fallback to saved data: {len(self.schedule_data)} items")
                return True
            else:
                return False
    
    def _update_folder_name_if_auto_loaded(self):
        """自動読み込みされた場合にフォルダ名を更新"""
        if hasattr(self, '_saved_folder_name') and hasattr(self, 'folder_name') and self.folder_name is not None:
            self.folder_name.value = self._saved_folder_name
            try:
                self.folder_name.update()
            except AssertionError:
                # ページに追加されていない場合はスキップ
                pass
            except Exception as e:
                print(f"Error updating folder name: {e}")

    def _reload_folder_on_navigation(self):
        """ページ遷移時にフォルダを再読み込み"""
        try:
            # クライアントストレージから保存されたフォルダパスを取得
            stored_folder_path = self.page.client_storage.get("folder_name")
            
            if stored_folder_path:
                import os
                # フォルダが存在するかチェック
                if os.path.exists(stored_folder_path) and os.path.isdir(stored_folder_path):
                    print(f"Reloading folder on navigation: {stored_folder_path}")
                    
                    # フォルダからデータを再読み込み（最新データを取得）
                    success = self._reload_folder_data(stored_folder_path)
                    
                    if success:
                        # フォルダ名を更新
                        self._saved_folder_name = f"選択中のフォルダ: {os.path.basename(stored_folder_path)}"
                        print(f"Navigation reload successful: {len(self.schedule_data)} items loaded")
                    else:
                        print("Navigation reload failed, using existing data")
                else:
                    print(f"Folder not found during navigation reload: {stored_folder_path}")
                    # フォルダが見つからない場合、無効なパスをクリア
                    self.page.client_storage.remove("folder_name")
            else:
                print("No saved folder found during navigation")
                
        except Exception as e:
            print(f"Error during folder reload on navigation: {e}")
            import traceback
            traceback.print_exc()

    def _update_ui_after_data_load(self):
        """データ読み込み後のUI更新処理"""
        try:
            if self.schedule_data and hasattr(self, 'tabs'):
                print(f"Updating UI with {len(self.schedule_data)} schedule items")
                
                # 全てのタブを更新する
                for tab_index, tab in enumerate(self.tabs.tabs):
                    try:
                        tab_content = tab.content
                        tab_label = self.locate_labels[tab_index] if tab_index < len(self.locate_labels) else "個人名絞り込み"
                        
                        if hasattr(tab_content, 'controls') and len(tab_content.controls) > 2:
                            calendar_controls = tab_content.controls[2].controls
                            
                            # UpdateCard処理
                            UpdateCard.update_cards_with_schedule_data(
                                e=None,
                                schedule_data=self.schedule_data,
                                page=self.page,
                                card_name=tab_label,
                                card=calendar_controls
                            )
                            
                            # UpdateCalendar処理
                            UpdateCalendar.update_calendar_with_schedule_data(
                                e=None,
                                schedule_data=self.schedule_data,
                                page=self.page,
                                calendar=calendar_controls[1:],
                                card_name=tab_label,
                                filter_name=None
                            )
                            
                            print(f"Updated tab {tab_index} ({tab_label})")
                    except Exception as tab_error:
                        print(f"Error updating tab {tab_index}: {tab_error}")
                        continue
                
                # タブ全体を更新
                try:
                    # Tabsがページに追加されているか確認してから更新
                    if hasattr(self.tabs, 'page') and self.tabs.page is not None:
                        self.tabs.update()
                        print("All tabs UI updated after data load")
                    else:
                        # Tabsがページに追加されていない場合はページ全体を更新
                        self.page.update()
                        print("Page updated instead of tabs (tabs not yet added to page)")
                except Exception as update_error:
                    print(f"Error updating tabs: {update_error}")
                    # フォールバック: ページ全体を更新
                    try:
                        self.page.update()
                    except Exception as fallback_error:
                        print(f"Fallback page update also failed: {fallback_error}")
                        
        except Exception as e:
            print(f"Error updating UI after data load: {e}")
            import traceback
            traceback.print_exc()

    def _save_current_data(self):
        """現在のデータをクライアントストレージに保存"""
        try:
            # schedule_dataを保存
            self.page.client_storage.set("schedule_data", self.schedule_data)
            print(f"Saved {len(self.schedule_data)} schedule items to client storage")
        except Exception as e:
            print(f"Error saving current data: {e}")
