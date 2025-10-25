import datetime
import flet as ft

class UpdateCard:
    @staticmethod
    def create_card_for_month(year, month, label):
        """月の各日のカードを作成"""
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
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("担当者名")), 
                                    ft.DataCell(ft.Text("AM or PM"))
                                ])
                            ]
                        )
                    ],
                    data={"date": f"{year}-{month:02d}-{day:02d}", "locate": label},  
                ),
            )
            cards.append(card)
        return cards
    
    @staticmethod
    def update_cards_with_schedule_data(e, schedule_data, page, card_name, card):
        """カードの内容をスケジュールデータで更新"""
        # schedule_data=[] の場合はclientstorageからデータを取得する
        if not schedule_data:
            try:
                schedule_data = page.client_storage.get("schedule_data")
                if schedule_data is None:
                    schedule_data = []
            except Exception as e:
                schedule_data = []
        else:
            schedule_data = schedule_data   # あればそのまま使用する
        
        if not card_name:
            return
        
        if card_name:
            filtered_data = [data for data in schedule_data if data['locate'] == card_name]
        else:
            return
        
        # カードの内容を更新
        # card の中にtab_calendar.controlsが入っている
        # 中のft.Cardを更新する
        for i, control in enumerate(card):
            if isinstance(control, ft.Card):
                # カードの日付を取得（年月日を抽出）
                date_text = ""
                if hasattr(control.content, 'data') and control.content.data and 'date' in control.content.data:  # 日付は完全一致にする
                    date_text = control.content.data["date"]
                    
                    # filtered_dataから該当する日付のデータを検索
                    matching_data = []
                    for data in filtered_data:
                        # データの日付フォーマットに応じて比較ロジックを調整
                        if 'date' in data:
                            data_date = data['date']
                            
                            # 日付を正規化して比較（ゼロパディングの違いを吸収）
                            if isinstance(data_date, str):
                                # 両方の日付をdatetimeオブジェクトに変換して比較
                                try:
                                    from datetime import datetime
                                    # カードの日付をパース
                                    card_date = datetime.strptime(date_text, "%Y-%m-%d")
                                    
                                    # データの日付をパース（複数のフォーマットに対応）
                                    data_date_obj = None
                                    for fmt in ["%Y-%m-%d", "%Y-%m-%d", "%Y-%-m-%-d"]:
                                        try:
                                            data_date_obj = datetime.strptime(data_date, fmt)
                                            break
                                        except ValueError:
                                            continue
                                    
                                    # フォーマットが合わない場合は手動でパース
                                    if data_date_obj is None:
                                        parts = data_date.split('-')
                                        if len(parts) == 3:
                                            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                                            data_date_obj = datetime(year, month, day)
                                    
                                    # 日付が一致するかチェック
                                    if data_date_obj and card_date.date() == data_date_obj.date():
                                        matching_data.append(data)
                                        
                                except ValueError as e:
                                    # フォールバック：文字列として完全一致を試す
                                    if date_text == data_date:
                                        matching_data.append(data)
                    
                    # マッチするデータがある場合、DataTableの行を更新
                    # 午前データならばdatacellの0番目に
                    # 午後データならばdataellの1番目に配置
                    if matching_data and len(control.content.controls) > 1:
                        data_table = control.content.controls[1]
                        if isinstance(data_table, ft.DataTable):
                            # 既存の行をクリア
                            data_table.rows.clear()
                            
                            # filtered_dataの内容で行を追加
                            for data in matching_data:
                                staff_name = data.get('staff_name') or data.get("phName", "不明")
                                time = data.get('time', "不明")  # 病棟名はcard_nameを使用
                                
                                # 時間帯に応じて背景色を設定
                                row_color = None
                                if time == "am":
                                    row_color = ft.Colors.PINK_100  # 午前は薄いピンク
                                elif time == "pm":
                                    row_color = ft.Colors.BLUE_100  # 午後は薄い青
                                new_row = ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(staff_name)),
                                        ft.DataCell(ft.Text(time))
                                    ],
                                    color=row_color  # colorプロパティを使用
                                )
                                
                                data_table.rows.append(new_row)
                        else:
                            pass
                    else:
                        if not matching_data:
                            pass
                        if len(control.content.controls) <= 1:
                            pass
                    
                    # マッチするデータがない場合はデフォルトの行を保持
                    # 別フォルダを読み込んだとき、日付に該当するデータがない場合はcardのデータフレームを削除
                    if not matching_data and len(control.content.controls) > 1:
                        data_table = control.content.controls[1]
                        data_table.rows.clear()
                        # デフォルトの行を追加
                        if isinstance(data_table, ft.DataTable) and not data_table.rows:
                            # デフォルトの行を追加
                            default_row = ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("担当者名")),
                                    ft.DataCell(ft.Text("AM or PM"))
                                ]
                            )
                            data_table.rows.append(default_row)
                    try:
                        if len(control.content.controls) > 1:
                            control.content.controls[1].update()
                    except AssertionError as e:
                        # ページに追加されていない場合はスキップ
                        pass
                    except Exception as e:
                        pass
                else:
                    # データテーブルがある場合には削除
                    pass
        
        # ページを再描画（ページに追加されている場合のみ）
        try:
            page.update()
        except AssertionError as e:
            # ページに追加されていない場合はスキップ
            pass
        except Exception as e:
            pass
