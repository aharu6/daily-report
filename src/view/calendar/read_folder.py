import os
import flet as ft

class ReadFolder:
    @staticmethod
    def read_folder(e, schedule_data, page, folder_name, checkboxes=None):
        """フォルダからスケジュールデータを読み込み"""
        if not e.path:
            return
        
        try:
            # フォルダパスを保存
            page.client_storage.set("folder_name", e.path)
            folder_name.value = f"選択中のフォルダ: {os.path.basename(e.path)}"
            
            # フォルダ内のファイルを読み込み（仮実装）
            # 実際の実装では、CSVやExcelファイルを読み込んでスケジュールデータを作成
            
            # サンプルデータを作成（実際はファイルから読み込み）
            sample_data = [
                {
                    "date": "2025-07-15",
                    "phName": "田中太郎",
                    "locate": "ICU"
                },
                {
                    "date": "2025-07-16", 
                    "phName": "佐藤花子",
                    "locate": "OR"
                },
                {
                    "date": "2025-07-17",
                    "phName": "鈴木次郎",
                    "locate": "ICU"
                }
            ]
            
            # schedule_dataを更新
            schedule_data.clear()
            schedule_data.extend(sample_data)
            
            # クライアントストレージにも保存
            page.client_storage.set("schedule_data", schedule_data)
            
            print(f"フォルダから {len(schedule_data)} 件のデータを読み込みました")
            
            # UIを更新
            folder_name.update()
            
        except Exception as ex:
            print(f"フォルダ読み込みエラー: {ex}")
            folder_name.value = "フォルダ読み込みエラー,読み込むフォルダを選択してください"
            folder_name.update()
