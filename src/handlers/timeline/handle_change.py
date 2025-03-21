class HandleChange:
    @staticmethod
    def handle_change(e, Date, page):
        """_summary_
        選択した日付にてカレンダーを更新する
        デフォルトは今日の日付
        カレンダーは過去の日付も選択できるように
        Args:
            e (_type_): 日付選択
            Date (_type_): _description_
            page (_type_): _description_
        """
        selected_date = e.control.value  # 例えば2021-01-01のような形式
        # 年月日を取得して表示用のテキストに変換
        Date.text = f"{selected_date.year}/{selected_date.month}/{selected_date.day}"
        Date.data = selected_date
        page.update()