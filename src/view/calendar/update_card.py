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
                                ft.DataColumn(label=ft.Text("担当者名")),
                                ft.DataColumn(label=ft.Text("病棟名")),
                            ],
                            rows=[
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text("担当者1")), 
                                    ft.DataCell(ft.Text("病棟名"))
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
    def update_cards_with_schedule_data(schedule_data, e, page, card_name, card):
        """カードの内容をスケジュールデータで更新"""
        if not schedule_data:
            return
        
        # スケジュールデータに基づいてカードを更新
        for item in schedule_data:
            if item.get("locate") == card_name:
                # カードの内容を更新
                date = item.get("date")
                name = item.get("phName", "不明")
                locate = item.get("locate", "不明")
                
                # 対応するカードを見つけて更新
                for card_item in card:
                    if hasattr(card_item, 'content') and hasattr(card_item.content, 'data'):
                        if card_item.content.data.get("date") == date:
                            # DataTableの行を更新
                            if card_item.content.controls and len(card_item.content.controls) > 1:
                                data_table = card_item.content.controls[1]
                                if hasattr(data_table, 'rows'):
                                    data_table.rows = [
                                        ft.DataRow(cells=[
                                            ft.DataCell(ft.Text(name)), 
                                            ft.DataCell(ft.Text(locate))
                                        ])
                                    ]
