import flet as ft

class CounterHandlers:
    @staticmethod
    def counterPlus(e, count_field, count_dict, time):
        old_Count = int(count_field.value)
        new_Count = old_Count + 1
        count_field.value = new_Count
        count_field.update()
        count_dict[time]["count"] = new_Count

    @staticmethod
    def counterMinus(e, count_field, count_dict, time):
        old_Count = int(count_field.value)
        new_Count = old_Count - 1
        if new_Count < 0:
            new_Count = 0
            e.control.value = 0
            e.control.update()
        count_field.value = new_Count
        count_field.update()
        count_dict[time]["count"] = new_Count
    
    @staticmethod
    def counter_Change(e,count_dict,time):
        """カウンターの値が変更されたら呼ばれる
        count_dictの値を更新する"""
        try:
            value = int(e.control.value)
        except (TypeError, ValueError):
            return # 値が整数に変換できない場合は何もしない
        if value <0:
            value = 0
        count_dict[time]["count"] = value
            

    @staticmethod
    def create_counter(e, count_dict):
        count = 0
        time = e
        count_field = ft.TextField(
            count,
            width=40,
            text_align=ft.TextAlign.CENTER,
            text_size=10,
            border_color=None,
            on_change=lambda e:CounterHandlers.counter_Change(e, count_dict, time)
        )
        count_dict[e] = {"count": count}
        return ft.Column(
            [
                ft.IconButton(
                    ft.icons.ARROW_DROP_UP_OUTLINED,
                    icon_size=25,
                    on_click=lambda e: CounterHandlers.counterPlus(
                        e, count_field, count_dict, time
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
                count_field,
                ft.IconButton(
                    ft.icons.ARROW_DROP_DOWN_OUTLINED,
                    icon_size=25,
                    on_click=lambda _: CounterHandlers.counterMinus(
                        e, count_field, count_dict, time
                    ),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                ),
            ]
        )
