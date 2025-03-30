#グラフの描画期間を選択するハンドラ
class PeriodHandler:
    @staticmethod
    def select_period(e,dp_event):
        #選択された日付をElevatedButtonのdataとして格納する
        e.control.data=dp_event.data
        #日付更新
        date=dp_event.data
        date=date.split("T")[0]
        e.control.text=date
        e.control.update()

