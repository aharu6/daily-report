import datetime
import flet as ft

class UpdateCard:
    @staticmethod
    def create_card_for_month(year, month,label):
        """_summary_

        Args:
            year (_type_): _description_
            month (_type_): _description_
            label (_type_): 病棟名

        Returns:
            _type_: _description_
        """
        cards = []
        if month == 12:
            days_in_month = (datetime.date(year + 1, 1, 1) - datetime.date(year, month, 1)).days
        else:
            days_in_month = (datetime.date(year, month + 1, 1) - datetime.date(year, month, 1)).days
        
        for day in range(1, days_in_month + 1):
            card = ft.Card(
                content=ft.Column(
                    controls=[
                        ft.Text(f"{year}年{month}月{day}日"),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(label=ft.Text("担当者名"), numeric=True),
                                ft.DataColumn(label=ft.Text("病棟名"), numeric=True),
                            ],
                            rows=[
                                # 担当者の名前が入る
                                ft.DataRow(cells=[ft.DataCell(ft.Text("担当者1")), ft.DataCell(ft.Text("病棟名"))])
                            ]
                        )
                    ],
                    data={"date": f"{year}-{month:01d}-{day:01d}", "locate": label},  
                ),
            )
            cards.append(card)
        return cards
    
    @staticmethod
    def update_cards_with_schedule_data(e, schedule_data, page, card_name, card):
        """
        カードの内容をスケジュールデータで更新する
        :param cards: 更新対象のカードリスト
        :param schedule_data: スケジュールデータ（辞書のリスト）
        card_name:更新する病棟名
        """
        #schedule_data=[] の場合はclientstorageからデータを取得する
        if not schedule_data:
            try:
                schedule_data = page.client_storage.get("schedule_data")
                if schedule_data is None:
                    schedule_data = []
            except Exception as e:
                schedule_data = []
        else:
            schedule_data = schedule_data   #あればそのまま使用する

        filtered_data= [data for data in schedule_data if data['locate'] == card_name]
        #カードの内容を更新
        #card の中にtab_calendar.controlsが入っている
        #中のft.Cardを更新する
        for i, control in enumerate(card):
            if isinstance(control, ft.Card):
                # カードの日付を取得（年月日を抽出）
                date_text = ""
                if hasattr(control.content, 'data') and control.content.data and 'date' in control.content.data:#日付は完全一致にする
                    date_text = control.content.data["date"]
                    
                    # filtered_dataから該当する日付のデータを検索
                    matching_data = []
                    for data in filtered_data:
                        # データの日付フォーマットに応じて比較ロジックを調整
                        if 'date' in data:
                            data_date = data['date']
                            # 日付の比較処理　完全一致の場合にmatching_dataに追加
                            if isinstance(data_date, str) and date_text in data_date:
                                matching_data.append(data)
                    # マッチするデータがある場合、DataTableの行を更新
                    #午前データならばdatacellの0番目に
                    #午後データならばdataellの1番目に配置

                    if matching_data and len(control.content.controls) > 1:
                        data_table = control.content.controls[1]
                        if isinstance(data_table, ft.DataTable):
                            # 既存の行をクリア
                            data_table.rows.clear()
                            
                            # filtered_dataの内容で行を追加
                            for data in matching_data:
                                staff_name = data.get('staff_name',data["phName"])
                                time = data.get('time', data["time"])  # 病棟名はcard_nameを使用
                                
                                # 時間帯に応じて背景色を設定
                                row_color = None
                                if time == "am":
                                    row_color = ft.colors.PINK_100  # 午前は薄いピンク
                                elif time == "pm":
                                    row_color = ft.colors.BLUE_100  # 午後は薄い青
                                new_row = ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(staff_name)),
                                        ft.DataCell(ft.Text(time))
                                    ],
                                    color=row_color  # colorプロパティを使用
                                )
                                
                                data_table.rows.append(new_row)
                            
                    
                    # マッチするデータがない場合はデフォルトの行を保持
                    # 別フォルダを読み込んだとき、日付に該当するデータがない場合はcardのデータフレームを削除
                    elif len(control.content.controls) > 1:
                        data_table = control.content.controls[1]
                        data_table.rows.clear()
                        # デフォルトの行を追加
                        if isinstance(data_table, ft.DataTable) and not data_table.rows:
                            # デフォルトの行を追加
                            default_row = ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("name")),
                                    ft.DataCell(ft.Text("AM or PM"))
                                ]
                            )
                            data_table.rows.append(default_row)
                    control.content.controls[1].update()
                else:
                    #データテーブルがある場合には削除
                    pass

                    
        #ページを再描画
        page.update()