#ドロワーを展開する
#保管しているデータを取得して表示する
#右側にtimeline適用用のボタンを合わせて表示する
class ReloadDataHandler:
    @staticmethod
    def toggle_Reload_Data(e,page,drawer):
        page.open(drawer)
        #保存しているデータを読み出す
        #write csv時の保存名：timeline_data
        dat = page.client_storage.get("timeline_data")
        #save_data = {"date_phName":dict_data}
        #日付と名前それぞれのデータを取り出す
        #ドロワーには保管されている　key = date_phNameにて表示
        #編集ボタンを追加して、押すと再編集できるように
        print(dat)
        
    
