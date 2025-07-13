import flet as ft

class UpdateCalendar:
    @staticmethod
    def update_calendar_with_schedule_data(e, schedule_data, page, calendar, card_name, filter_name=None):
        """スケジュールデータでカレンダーの色を更新"""
        if not schedule_data or not calendar:
            return
        
        # カレンダーの各セルを確認してスケジュールがある日を色付け
        for row in calendar:
            if hasattr(row, 'controls'):
                for cell in row.controls:
                    if hasattr(cell, 'data') and cell.data and 'date' in cell.data:
                        cell_date = cell.data['date']
                        
                        # その日にスケジュールがあるかチェック
                        has_schedule = any(
                            item.get('date') == cell_date and 
                            (filter_name is None or item.get('phName') == filter_name) and
                            item.get('locate') == card_name
                            for item in schedule_data
                        )
                        
                        if has_schedule:
                            cell.bgcolor = ft.colors.LIGHT_BLUE_100
                        else:
                            cell.bgcolor = ft.colors.WHITE
        
        # カレンダーを更新
        for row in calendar:
            if hasattr(row, 'update'):
                row.update()
