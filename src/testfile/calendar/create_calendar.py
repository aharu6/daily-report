import flet as ft
import datetime
import math
from update_card import UpdateCard
    # 月カレンダーのようなUIを自作して表示する

class CreateCalendar:
    @staticmethod
    def create_calendar(year, month):
        # 曜日ヘッダー（日曜始まり）
        weekdays = ["S", "M", "T", "W", "T", "F", "S"]
        cell_width = 50  # セルの幅
        cell_height = 40  # セルの高さ
        weekday_row = ft.Row(
            [ft.Container(
                ft.Text(day, size=20, weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER),
                height=cell_height,
                width=cell_width,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.WHITE,  # 曜日部分の背景色
                ) for day in weekdays],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # 月の最初の日を取得
        first_day = datetime.date(year, month, 1)
        # 月の最終日を取得
        if month == 12:
            last_day = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        # 月の最初の日の曜日を取得（日曜始まりに変換）
        first_weekday = (first_day.weekday() + 1) % 7  # 0=Sunday, 6=Saturday
        # 月の日数
        days_in_month = (last_day - first_day).days + 1
        # 必要なセル数
        total_cells = first_weekday + days_in_month
        rows = math.ceil(total_cells / 7)

        # カレンダーのセルを作成
        calendar_cells = [weekday_row]
        for week in range(rows):
            week_cells = []
            for day in range(7):
                day_number = week * 7 + day - first_weekday + 1
                if 1 <= day_number <= days_in_month:
                    date = datetime.date(year, month, day_number)
                    week_cells.append(ft.Container(
                        content=ft.Text(str(date.day), size=20),
                        width=cell_width,
                        height=cell_height,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.WHITE,
                        data={"date": f"{year}-{month:01d}-{day_number:01d}"}  # 日付をデータ属性として保存
                    ))
                else:
                    week_cells.append(ft.Container(
                        content=ft.Text(""),
                        width=cell_width,
                        height=cell_height,
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.WHITE,
                    ))
            calendar_cells.append(ft.Row(week_cells, alignment=ft.MainAxisAlignment.CENTER))
        calendar = ft.Column(calendar_cells, alignment=ft.MainAxisAlignment.CENTER)
        # カスタム属性として年月を保存
        calendar.year = year
        calendar.month = month
        return calendar
    
    @staticmethod
    def forward_month(e,page, calendar,card_name):
        #表示中のカレンダー年月を取得
        current_set_year=calendar.year
        current_set_month=calendar.month
        #次の月を計算
        if current_set_month == 12:
            next_year = current_set_year + 1
            next_month = 1
        else:
            next_year = current_set_year
            next_month = current_set_month + 1
        
        #次の月のカレンダーを作成
        next_calendar = CreateCalendar.create_calendar(next_year, next_month)

        #ページのカレンダーを更新
        calendar.controls.clear()        
        calendar.controls.extend(next_calendar.controls)
        #カレンダーの年月を更新
        calendar.year = next_year
        calendar.month = next_month
        #ページを再描画
        calendar.update()


    @staticmethod
    def back_month(e,page, calendar,card_name):
        """_summary_

        Args:
            e (_type_): _description_
            page (_type_): _description_
            calendar (_type_): _description_
            card_name (_type_): 更新する病棟名,tab上の名前を取得する
        """
        #表示中のカレンダー年月を取得
        current_set_year=calendar.year
        current_set_month=calendar.month
        #前の月を計算
        if current_set_month == 1:
            prev_year = current_set_year - 1
            prev_month = 12
        else:
            prev_year = current_set_year
            prev_month = current_set_month - 1
        
        #前の月のカレンダーを作成
        prev_calendar = CreateCalendar.create_calendar(prev_year, prev_month)

        #ページのカレンダーを更新
        calendar.controls.clear()
        calendar.controls.extend(prev_calendar.controls)
        #カレンダーのデータを更新
        calendar.year = prev_year
        calendar.month = prev_month
        #ページを再描画
        calendar.update()
