import flet as ft

class UpdateCalendar:
    @staticmethod
    def update_calendar_with_schedule_data(e, schedule_data, page, calendar, card_name=None, filter_name=None):
        """スケジュールデータに基づいてカレンダーの色を更新"""
        print(f"[DEBUG CALENDAR] 更新開始: データ件数={len(schedule_data)} card_name={card_name} filter_name={filter_name}")
        
        # データのサンプルを表示（最初の3件）
        if schedule_data:
            print(f"[DEBUG CALENDAR] データサンプル:")
            for i, item in enumerate(schedule_data[:3]):
                print(f"  {i+1}: 日付={item.get('date')} 場所={item.get('locate')} 名前={item.get('phName')} ファイル={item.get('file_name')}")
        
        updated_cells = 0
        total_cells = 0
        
        # カレンダーの各セルを確認してスケジュールがある日を色付け
        for row_idx, row in enumerate(calendar):
            if hasattr(row, 'controls'):
                for cell_idx, cell in enumerate(row.controls):
                    total_cells += 1
                    if hasattr(cell, 'data') and cell.data and 'date' in cell.data:
                        cell_date = cell.data['date']
                        
                        # その日にスケジュールがあるかチェック
                        matching_schedules = []
                        
                        # デバッグ: セルの日付を出力
                        print(f"[DEBUG CALENDAR] セル日付: {cell_date}")
                        
                        for item in schedule_data:
                            item_date = str(item.get('date', ''))
                            item_locate = str(item.get('locate', ''))
                            item_name = str(item.get('phName', ''))
                            item_file = str(item.get('file_name', '不明'))
                            
                            # 日付マッチングの改善（ゼロパディングの違いを吸収）
                            date_match = False
                            if item_date and cell_date:
                                try:
                                    from datetime import datetime
                                    # セルの日付をパース
                                    cell_date_obj = datetime.strptime(cell_date, "%Y-%m-%d")
                                    
                                    # データの日付をパース（手動でパース）
                                    parts = item_date.split('-')
                                    if len(parts) == 3:
                                        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                                        item_date_obj = datetime(year, month, day)
                                        date_match = cell_date_obj.date() == item_date_obj.date()
                                        
                                        # デバッグ: 日付比較の詳細
                                        if date_match:
                                            print(f"[DEBUG CALENDAR] 日付マッチ: セル={cell_date} データ={item_date} ファイル={item_file}")
                                    else:
                                        date_match = item_date == cell_date
                                        if date_match:
                                            print(f"[DEBUG CALENDAR] 文字列マッチ: セル={cell_date} データ={item_date} ファイル={item_file}")
                                except ValueError:
                                    # フォールバック：文字列として完全一致を試す
                                    date_match = item_date == cell_date
                                    if date_match:
                                        print(f"[DEBUG CALENDAR] フォールバックマッチ: セル={cell_date} データ={item_date} ファイル={item_file}")
                            
                            # 場所とフィルタ名のマッチング
                            locate_match = card_name is None or item_locate == card_name
                            name_match = filter_name is None or item_name == filter_name
                            
                            # デバッグ: 場所マッチングの詳細
                            if date_match:
                                print(f"[DEBUG CALENDAR] 場所比較: カード名='{card_name}' データ場所='{item_locate}' マッチ={locate_match}")
                            
                            if date_match and locate_match and name_match:
                                matching_schedules.append(item)
                                print(f"[DEBUG CALENDAR] マッチング成功: 日付={item_date} 場所={item_locate} 名前={item_name} ファイル={item_file}")
                                
                        print(f"[DEBUG CALENDAR] セル {cell_date}: {len(matching_schedules)} 件のマッチ")
                        
                        has_schedule = len(matching_schedules) > 0
                        
                        if has_schedule:
                            print(f"[DEBUG CALENDAR] 色更新: セル {cell_date} を青色に変更")
                            old_bgcolor = cell.bgcolor
                            cell.bgcolor = ft.colors.BLUE_200
                            updated_cells += 1
                            
                            # セルの現在の状態を確認
                            print(f"[DEBUG CALENDAR] セル状態変更: {old_bgcolor} → {cell.bgcolor}")
                            
                            # セル単体での更新を試行
                            try:
                                cell.update()
                                print(f"[DEBUG CALENDAR] セル {cell_date} 個別更新成功")
                            except Exception as e:
                                print(f"[DEBUG CALENDAR] セル {cell_date} 個別更新失敗: {e}")
                        else:
                            cell.bgcolor = ft.colors.WHITE
        
        print(f"[DEBUG CALENDAR] カレンダー更新完了: {updated_cells}/{total_cells} セルを更新")
        
        # カレンダーを更新
        print(f"[DEBUG CALENDAR] カレンダー行数: {len(calendar)}")
        for row_idx, row in enumerate(calendar):
            if hasattr(row, 'update'):
                try:
                    print(f"[DEBUG CALENDAR] 行 {row_idx} を更新中...")
                    row.update()
                    print(f"[DEBUG CALENDAR] 行 {row_idx} 更新成功")
                except AssertionError as e:
                    print(f"[DEBUG CALENDAR] 行 {row_idx} 更新失敗 (AssertionError): {e}")
                    # ページに追加されていない場合はスキップ
                    pass
                except Exception as e:
                    print(f"[DEBUG CALENDAR] 行 {row_idx} 更新失敗 (Exception): {e}")
                    pass
            else:
                print(f"[DEBUG CALENDAR] 行 {row_idx} にupdateメソッドがありません")
        
        # ページ全体も更新を試行
        try:
            print(f"[DEBUG CALENDAR] ページ全体の更新を試行...")
            page.update()
            print(f"[DEBUG CALENDAR] ページ全体の更新成功")
        except Exception as e:
            print(f"[DEBUG CALENDAR] ページ全体の更新失敗: {e}")
        
        print(f"[DEBUG CALENDAR] カレンダー更新処理完了")
