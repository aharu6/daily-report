import os
import flet as ft
import pandas as pd
import chardet

class ReadFolder:
    @staticmethod
    def detect_encoding(file_path):
        """ファイルの文字エンコーディングを自動検出"""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    @staticmethod
    def read_folder(e, schedule_data, page, folder_name, checkboxes=None):
        """フォルダからスケジュールデータを読み込み"""
        if not e.path:
            return
        
        try:
            folder_path = e.path
            
            # フォルダ内のCSVファイルを読み込み
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
            #一つ下の階層のフォルダがあれば読みにいく
            check_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path,f))]
            if check_folders:
                for sub_folder in check_folders:
                    sub_folder_path = os.path.join(folder_path,sub_folder)
                    sub_csv_files = [f for f in os.listdir(sub_folder_path) if f.endswith('.csv')]
                    for sub_csv in sub_csv_files:
                        csv_files.append(os.path.join(sub_folder,sub_csv))
            
            if not csv_files:
                # folder_nameがNoneでない場合のみエラーメッセージを設定
                if folder_name is not None:
                    folder_name.value = "CSVファイルが見つかりません"
                    try:
                        folder_name.update()
                    except AssertionError:
                        # ページに追加されていない場合はスキップ
                        pass
                return

            # schedule_dataをクリア
            schedule_data.clear()
            
            for csv_file in csv_files:
                try:
                    file_path = os.path.join(folder_path, csv_file)
                    encoding = ReadFolder.detect_encoding(file_path)
                    
                    df = pd.read_csv(file_path, encoding=encoding)
                    
                    # 必要な列が存在するかチェック
                    required_columns = ["locate", "phName", "date"]
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if missing_columns:
                        continue
                    
                    # 午前のデータ（0-15行）
                    am_data = df.loc[:15, required_columns].drop_duplicates().reset_index(drop=True)
                    
                    am_count = 0
                    for _, row in am_data.iterrows():
                        # 空の行をスキップ
                        if pd.isna(row["locate"]) or pd.isna(row["phName"]) or pd.isna(row["date"]):
                            continue
                        
                        # 病棟名の正規化（リスト形式の文字列を処理）
                        locate_raw = str(row["locate"])
                        print(f"[DEBUG READ] 元の場所データ: '{locate_raw}'")
                        
                        if locate_raw.startswith("['") and locate_raw.endswith("']"):
                            # "['ICU']" -> ["ICU"] または "['ICU', '3A']" -> ["ICU", "3A"]
                            content = locate_raw[2:-2]  # 外側の括弧とクォートを除去
                            if "', '" in content:
                                # 複数の場所がある場合
                                locate_clean = [loc.strip("'\"") for loc in content.split("', '")]
                            else:
                                # 単一の場所の場合
                                locate_clean = [content.strip("'\"")]
                        elif locate_raw == "[]" or locate_raw.lower() in ["nan", "none", ""]:
                            # 空のリストや無効なデータはスキップ
                            continue
                        else:
                            # その他の形式の処理
                            locate_clean = [locate_raw.strip("'\"")]
                                
                        print(f"[DEBUG READ] 正規化後の場所データ: {locate_clean}")
                        
                        # 複数の場所がある場合、それぞれの場所に対してデータエントリを作成
                        for single_locate in locate_clean:
                            # 個人名の検証
                            phName_raw = str(row["phName"])
                            if phName_raw.lower() in ["nan", "none", ""] or pd.isna(row["phName"]):
                                continue
                            
                            # 日付の正規化（必要に応じてゼロパディング）
                            date_raw = str(row["date"])
                            try:
                                # 日付を解析して標準形式に変換
                                from datetime import datetime
                                if '-' in date_raw:
                                    # 年-月-日 形式
                                    parts = date_raw.split('-')
                                    if len(parts) == 3:
                                        year, month, day = parts
                                        date_normalized = f"{year}-{int(month)}-{int(day)}"
                                    else:
                                        date_normalized = date_raw
                                else:
                                    date_normalized = date_raw
                            except ValueError:
                                # パースできない場合はそのまま使用
                                date_normalized = date_raw
                            
                            data_entry = {
                                "date": date_normalized,
                                "phName": str(row["phName"]),
                                "locate": single_locate,
                                "time": "am",
                                "file_name": csv_file
                            }
                            schedule_data.append(data_entry)
                            am_count += 1
                    
                    
                    # 午後のデータ（16行目以降）
                    pm_count = 0
                    if len(df) > 16:
                        pm_data = df.loc[16:, required_columns].drop_duplicates().reset_index(drop=True)
                        
                        for _, row in pm_data.iterrows():
                            # 空の行をスキップ
                            if pd.isna(row["locate"]) or pd.isna(row["phName"]) or pd.isna(row["date"]):
                                continue
                            
                            # 病棟名の正規化（リスト形式の文字列を処理）
                            locate_raw = str(row["locate"])
                            print(f"[DEBUG READ] 元の場所データ: '{locate_raw}'")
                            
                            if locate_raw.startswith("['") and locate_raw.endswith("']"):
                                # "['ICU']" -> ["ICU"] または "['ICU', '3A']" -> ["ICU", "3A"]
                                content = locate_raw[2:-2]  # 外側の括弧とクォートを除去
                                if "', '" in content:
                                    # 複数の場所がある場合
                                    locate_clean = [loc.strip("'\"") for loc in content.split("', '")]
                                else:
                                    # 単一の場所の場合
                                    locate_clean = [content.strip("'\"")]
                            elif locate_raw == "[]" or locate_raw.lower() in ["nan", "none", ""]:
                                # 空のリストや無効なデータはスキップ
                                continue
                            else:
                                # その他の形式の処理
                                locate_clean = [locate_raw.strip("'\"")]
                                    
                            print(f"[DEBUG READ] 正規化後の場所データ: {locate_clean}")
                            
                            # 複数の場所がある場合、それぞれの場所に対してデータエントリを作成
                            for single_locate in locate_clean:
                                # 個人名の検証
                                phName_raw = str(row["phName"])
                                if phName_raw.lower() in ["nan", "none", ""] or pd.isna(row["phName"]):
                                    continue
                                
                                # 日付の正規化
                                date_raw = str(row["date"])
                                try:
                                    if '-' in date_raw:
                                        # 年-月-日 形式
                                        parts = date_raw.split('-')
                                        if len(parts) == 3:
                                            year, month, day = parts
                                            date_normalized = f"{year}-{int(month)}-{int(day)}"
                                        else:
                                            date_normalized = date_raw
                                    else:
                                        date_normalized = date_raw
                                except ValueError:
                                    date_normalized = date_raw
                                
                                data_entry = {
                                    "date": date_normalized,
                                    "phName": str(row["phName"]),
                                    "locate": single_locate,
                                    "time": "pm",
                                    "file_name": csv_file
                                }
                                schedule_data.append(data_entry)
                                pm_count += 1
                    
                    
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    continue
            
            
            # フォルダパスを保存
            page.client_storage.set("folder_name", folder_path)
            page.client_storage.set("schedule_data", schedule_data)
            
            # フォルダ名表示を更新（folder_nameがNoneでない場合のみ）
            if folder_name is not None:
                folder_name.value = f"選択中のフォルダ: {os.path.basename(folder_path)}"
                
                # UIを更新
                try:
                    folder_name.update()
                except AssertionError:
                    # ページに追加されていない場合はスキップ
                    pass
            
            # 個人絞り込みページのチェックボックスの更新
            if checkboxes:
                ReadFolder.update_check_boxes(checkboxes, schedule_data)
            
        except Exception as ex:
            import traceback
            traceback.print_exc()
            # folder_nameがNoneでない場合のみエラーメッセージを設定
            if folder_name is not None:
                folder_name.value = "フォルダ読み込みエラー,読み込むフォルダを選択してください"
                try:
                    folder_name.update()
                except AssertionError:
                    # ページに追加されていない場合はスキップ
                    pass

    @staticmethod
    def update_check_boxes(checkboxes, schedule_data):
        """チェックボックスリストを更新"""
        checkboxes.controls.clear()
        unique_names = set(item["phName"] for item in schedule_data if "phName" in item)
        checkboxes.controls = [
            ft.Checkbox(
                label=name,
                value=False,
                data=name,
            )
            for name in unique_names
        ]
        checkboxes.update()
