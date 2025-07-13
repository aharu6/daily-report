import flet as ft

class UpdateCalendar:
    @staticmethod
    def update_calendar_with_schedule_data(e, schedule_data, page, calendar, card_name=None, filter_name=None):
        """スケジュールデータに基づいてカレンダーの色を更新"""
        print(f"[DEBUG CALENDAR] 更新開始: データ件数={len(schedule_data)} card_name={card_name} filter_name={filter_name}")
        
        # データのサンプルを表示（最初の3件）
        if schedule_data:
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
                                        
                                        
                                    else:
                                        date_match = item_date == cell_date

                                except ValueError:
                                    # フォールバック：文字列として完全一致を試す
                                    date_match = item_date == cell_date
                        
                            # 場所とフィルタ名のマッチング
                            locate_match = card_name is None or item_locate == card_name
                            name_match = filter_name is None or item_name == filter_name
                            
                            
                            if date_match and locate_match and name_match:
                                matching_schedules.append(item)
                                
                        
                        has_schedule = len(matching_schedules) > 0
                        
                        if has_schedule:
                            old_bgcolor = cell.bgcolor
                            cell.bgcolor = ft.colors.BLUE_200
                            updated_cells += 1
                            
                            
                            # セル単体での更新を試行
                            try:
                                cell.update()
                            except Exception as e:
                                pass
                        else:
                            cell.bgcolor = ft.colors.WHITE
        
        
        # カレンダーを更新
        for row_idx, row in enumerate(calendar):
            if hasattr(row, 'update'):
                try:
                    row.update()
                except AssertionError as e:
                    # ページに追加されていない場合はスキップ
                    pass
                except Exception as e:
                    pass
            else:
                pass
            
        
        # ページ全体も更新を試行
        try:
            page.update()
        except Exception as e:
            pass
        
