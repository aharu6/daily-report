import flet as ft
import datetime
class Chart_Download_Handler:
    @staticmethod
    def open_directory(page,barchart,chart_name):
        #保存先を指定
        #フォルダを開く 
        select_directory1=ft.FilePicker(
            on_result=lambda e:Chart_Download_Handler.download_chart(
                e=e,
                selectdirectory=select_directory1,
                barchart=barchart,
                chart_name=chart_name,
            )
        )
        page.overlay.append(select_directory1)
        page.update()
        select_directory1.get_directory_path()
    
    
    @staticmethod
    def download_chart(e,barchart,selectdirectory,chart_name):
        today = datetime.date.today()
        if selectdirectory.result:
            try:
                file_path=(
                    selectdirectory.result.path
                    +"/"
                    +today.strftime("%Y%m%d")
                    +chart_name
                    +".jpg"
                    )
                # 画像の形式を指定
                barchart.write_image(file_path)
            except Exception as e:
                print(e)
                return
            