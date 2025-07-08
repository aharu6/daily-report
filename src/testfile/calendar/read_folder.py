import os
import pandas as pd
import chardet
from normalise_locate import NormaliseLocate
from update_card import UpdateCard
class ReadFolder:
    @staticmethod
    def detect_encoding(file_path):
        with open(file_path,'rb') as f:
            result=chardet.detect(f.read())

        return result['encoding']
    

    @staticmethod
    def read_folder(e,schedule_data,page, folder_name):
        folder_path =e.path

        #フォルダ内のcsvファイルを読み込み、病棟名と担当者名を抽出する
        csv_files=[f for f in os.listdir(e.path) if f.endswith('.csv')]
        #抽出してjson形式のデータに変換
        if not csv_files:
            print("No CSV files found in the selected folder.")
            return []
        
        data = []
        for csv_file in csv_files:
            try:
                #午前0行目、午後16行目
                file_path=os.path.join(folder_path,csv_file)
                df=pd.read_csv(file_path,encoding=ReadFolder.detect_encoding(file_path=os.path.join(folder_path,csv_file)))
                
                #病棟名と時間と名前が必要
                #午前で複数病棟担当している場合、先頭行から16行目までの全てのデータを取得してまとめる
                #病棟名と名前の頭16行のユニークな内容を取得する
                am_data=df.loc[:15,["locate","phName","date"]].drop_duplicates().reset_index(drop=True)
                am_data=NormaliseLocate.normalise_locate(am_data,"am")
                data.extend(am_data)
                
                #午後のデータも同様に取得する
                #午後は16行目からのデータを取得する
                pm_data=df.loc[16:,["locate","phName","date"]].drop_duplicates().reset_index(drop=True)
                pm_data=NormaliseLocate.normalise_locate(pm_data,"pm")  
                data.extend(pm_data)
                
            except Exception as e:
                print(f"Error processing file {csv_file}: {e}")
                continue
        #読み込んだデータをclientstorageに保存する
        page.client_storage.set("schedule_data", data)  

        #現在のフォルダ名表示
        folder_name.value = f"選択中のフォルダ: {folder_path}"
        folder_name.update()
        #フォルダ名はclientstorageに保管する
        page.client_storage.set("folder_name", folder_path)
        
        return schedule_data, page