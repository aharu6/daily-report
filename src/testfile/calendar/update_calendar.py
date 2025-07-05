import flet as ft
class UpdateCalendar:
    @staticmethod
    def update_calendar_with_schedule_data(e, schedule_data, page, calendar,card_name):
        """
        カレンダーのセルをデータに応じて更新する
        データがあればカレンダーft.Container(bgcolor=)の色をつける
        calendar: カレンダーのセル群 calendar[5:]が日付のセル部分になる
        tabs (ft.Tabs)
├── selected_index: 0
├── animation_duration: 300
├── indicator_color: ft.colors.BLUE
└── tabs: [ft.Tab, ft.Tab, ...] (19個のタブ)
    ├── tabs[0] (ICU)
    │   ├── text: "ICU"
    │   └── content: ft.Column
    │       └── controls: [arrow, update_button, tab_calendar]
    │           ├── [0] arrow (ft.Row)
    │           │   └── controls: [back_button, date_text, next_button]
    │           ├── [1] update_button (ft.ElevatedButton)
    │           └── [2] tab_calendar (ft.Column - CreateCalendar.create_calendar()の結果)
    │               └── controls: [カレンダー表示部分, カード1, カード2, ..., カード31]
    │                   ├── [0] カレンダーヘッダー・セル (ft.Row等)← calendar引数は今ここ
    │                   ├── [1] 7月1日のカード (ft.Card)
    │                   ├── [2] 7月2日のカード (ft.Card)
    │                   ├── ...
    │                   └── [31] 7月31日のカード (ft.Card)
    ├── tabs[1] (OR)
    │   ├── text: "OR"
    │   └── content: (同様の構造)
    ├── ...
    └── tabs[18] (DI)
        ├── text: "DI"
        └── content: (同様の構造)

        calendar[0].controls 1週目の日付群
        calendar[1].controls 2週目の日付群
        calendar[2].controls 3週目の日付群
        calendar[3].controls 4週目の日付群 ...
        以後cardが続く

        """
        if not schedule_data:
            try:
                schedule_data = page.client_storage.get("schedule_data")
                if schedule_data is None:
                    schedule_data = []
            except Exception as e:
                schedule_data = []
        else:
            schedule_data = schedule_data
        
        # schedule_dataからcard_nameに該当するデータを抽出
        filtered_data = [data for data in schedule_data if data['locate'] == card_name]
        print(f"Filtered data for {card_name}: {filtered_data}")
        #calendarの長さ
        for i,control in enumerate(calendar):
            if isinstance(control,ft.Row):#calendar[i]== ft.Rowならその中に一週間分の日付セルが入っている
                for j in calendar[i].controls:
                    date_text=""
                    if j.data and isinstance(j.data, dict):
                        date_text = j.data["date"]
                        print(f"Date text: {date_text}")
                    # 日付のデータを抽出
                    matching_data = []
                    for data in filtered_data:
                        if 'date' in data:
                            data_date = data['date']
                            # 日付の比較処理　完全一致の場合にmatching_dataに追加
                            if isinstance(data_date, str) and date_text==data_date:
                                matching_data.append(data)
                    print(f"Matching data for {date_text}: {matching_data}")
                    # 午前データと午後データが両方揃っている場合に色をつける
                    if matching_data:
                        has_am=any(data["time"] =="am" for data in matching_data)
                        has_pm=any(data["time"] =="pm" for data in matching_data)
                        if has_am and has_pm:
                            j.bgcolor = ft.colors.GREEN
                        else:
                            pass
                    j.update()
                else:
                    pass
