import flet as ft
import datetime
class DataframeDownloadHandler:
    def __init__(self):
        self

    @staticmethod
    def open_directory_for_dataframe(page,dataframe,name):
        #保存先を指定
        #フォルダを開く
        select_directory=ft.FilePicker(
            on_result=lambda e:DataframeDownloadHandler.download_dataframe(
                dataframe=dataframe,
                file_name=name,
                selectdirectory=select_directory,
                )
        )
        page.overlay.append(select_directory)
        page.update()
        select_directory.get_directory_path()

    @staticmethod
    def download_dataframe(dataframe,file_name,selectdirectory):
        today = datetime.date.today()
        if selectdirectory.result:
            try:
                import os
                file_path=os.path.join(
                    selectdirectory.result.path,
                    f'{today.strftime("%Y%m%d")}_{file_name}.csv'
                )
                dataframe.to_csv(file_path, index=True)
            except Exception as e:
                print(e)
                return
        #csvファイルとして保存する