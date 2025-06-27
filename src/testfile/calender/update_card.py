import datetime
import flet as ft

class UpdateCard:
    @staticmethod
    def create_card_for_month(year, month):
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
                    ]
                ),
            )
            cards.append(card)
        return cards