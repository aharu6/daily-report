import flet as ft

class UpdateCalendar:
    @staticmethod
    def update_calendar_with_schedule_data(e, schedule_data, page, calendar, card_name, filter_name=None):
        """スケジュールデータでカレンダーの色を更新"""
        if not schedule_data or not calendar:
            return
        
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
                            
                            date_match = item_date == cell_date
                            locate_match = item_locate == card_name
                            name_match = filter_name is None or item_name == filter_name
                            
                            if date_match and locate_match and name_match:
                                matching_schedules.append(item)
                        
                        has_schedule = len(matching_schedules) > 0
                        
                        if has_schedule:
                            cell.bgcolor = ft.colors.BLUE_200
                            updated_cells += 1
                        else:
                            cell.bgcolor = ft.colors.WHITE
        
        # カレンダーを更新
        for row in calendar:
            if hasattr(row, 'update'):
                try:
                    row.update()
                except AssertionError:
                    # ページに追加されていない場合はスキップ
                    pass
