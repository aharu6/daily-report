import flet as ft
class UpdateCalendar:
    @staticmethod
    def update_calendar_with_schedule_data(e, schedule_data, page, calendar,card_name,filter_name):
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
        #病棟絞り込みページの時にはcard_nameに渡される病棟名を利用する
        if card_name:
            filtered_data = [data for data in schedule_data if data['locate'] == card_name]
        #個人名絞り込みの時にはチェックボックスで該当する名前の一覧だけで絞り込みを行う(filter_name)
        #名前は複数選択することができるので、filter_nameはリストになっている
        #リスト内に存在する名前で絞り込みデータを作成する
        elif filter_name:
            print(f"絞り込み対象の名前: {filter_name}")
            filtered_data=[]
            for i in filter_name:
                for data in schedule_data:
                    if data["phName"]==i:
                        filtered_data.append(data)
                    else:pass

        else:#card_nameもfilter_nameも存在しない場合には関数を修了する
            # 何もチエックボックスを選択せずに更新ボタンを押した場合の処理
            return

        if isinstance(calendar, ft.Column):
            calendar_controls=calendar.controls
        else:
            calendar_controls=calendar

        #calendarの長さ
        for i,control in enumerate(calendar_controls):
            if isinstance(control,ft.Row):#calendar[i]== ft.Rowならその中に一週間分の日付セルが入っている
                for j in control.controls:
                    date_text=""
                    if j.data and isinstance(j.data, dict):
                        date_text = j.data["date"]
                    # 日付のデータを抽出
                    matching_data = []
                    for data in filtered_data:
                        if 'date' in data:
                            data_date = data['date']
                            # 日付の比較処理　完全一致の場合にmatching_dataに追加
                            if isinstance(data_date, str) and date_text==data_date:
                                matching_data.append(data)
                    # 午前データと午後データが両方揃っている場合に色をつける
                    if matching_data:
                        has_am=any(data["time"] =="am" for data in matching_data)
                        has_pm=any(data["time"] =="pm" for data in matching_data)
                        if has_am and has_pm:
                            j.bgcolor = ft.colors.GREEN
                    else:
                        j.bgcolor=ft.colors.WHITE  # データがない場合は白色に戻す
                    j.update()
                    
                else:
                    pass
            else:
                pass
