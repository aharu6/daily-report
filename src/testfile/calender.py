import flet as ft
from flet import View
import datetime
import math

def main(page: ft.Page):
    page.title = "calendar"
    page.window.width = 1400
    page.window.height = 1000
    page.scroll = True
    back_month_button=ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_size=30,
        on_click=lambda e: page.add(ft.Text("前の月を表示する処理をここに追加")),
        tooltip="前の月",
    )
    next_month_button=ft.IconButton(
        icon=ft.icons.ARROW_FORWARD,
        icon_size=30,
        on_click=lambda e: page.add(ft.Text("次の月を表示する処理をここに追加")),
        tooltip="次の月",
    )   
    # 月カレンダーのようなUIを自作して表示する
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
                bgcolor=None,
                
                ) for day in weekdays],
            alignment=ft.MainAxisAlignment.CENTER
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
        print(f"first_weekday: {first_weekday}, first_day: {first_day}, last_day: {last_day}")
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
        return ft.Column(calendar_cells, alignment=ft.MainAxisAlignment.CENTER)

    # 現在の日付を取得
    today = datetime.date.today()
    # 現在の年と月を取得
    current_year = today.year
    current_month = today.month

    # カレンダーを作成
    calendar = create_calendar(current_year, current_month)
    # ページにカレンダーを追加
    page.add(ft.Text(f"calender", size=30, weight=ft.FontWeight.BOLD))
    arrow=ft.Row([
        back_month_button,
        ft.Text(f"{current_year}年{current_month}月", size=30, weight=ft.FontWeight.BOLD),
        next_month_button
    ])
    page.add(arrow, calendar)

ft.app(main)
