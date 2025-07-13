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
            
            if not csv_files:
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
                    print(f"\n--- {csv_file} の処理開始 ---")
                    file_path = os.path.join(folder_path, csv_file)
                    encoding = ReadFolder.detect_encoding(file_path)
                    print(f"検出されたエンコーディング: {encoding}")
                    
                    df = pd.read_csv(file_path, encoding=encoding)
                    print(f"CSVファイルの形状: {df.shape}")
                    print(f"利用可能な列: {list(df.columns)}")
                    
                    # 必要な列が存在するかチェック
                    required_columns = ["locate", "phName", "date"]
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if missing_columns:
                        print(f"必要な列が見つかりません: {missing_columns}")
                        print(f"利用可能な列: {list(df.columns)}")
                        continue
                    
                    print(f"データの最初の5行:")
                    print(df[required_columns].head())
                    
                    # 午前のデータ（0-15行）
                    am_data = df.loc[:15, required_columns].drop_duplicates().reset_index(drop=True)
                    print(f"午前データ: {len(am_data)} 件")
                    if not am_data.empty:
                        print(f"午前データサンプル:")
                        print(am_data.head(3))
                    
                    for _, row in am_data.iterrows():
                        # 病棟名の正規化（リスト形式の文字列を処理）
                        locate_raw = str(row["locate"])
                        if locate_raw.startswith("['") and locate_raw.endswith("']"):
                            # "['ICU']" -> "ICU"
                            locate_clean = locate_raw[2:-2]
                        elif locate_raw == "[]":
                            # 空のリストはスキップ
                            continue
                        else:
                            locate_clean = locate_raw
                        
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
                            "locate": locate_clean,
                            "time": "am"
                        }
                        schedule_data.append(data_entry)
                        print(f"追加された午前データ: {data_entry}")
                    
                    # 午後のデータ（16行目以降）
                    if len(df) > 16:
                        pm_data = df.loc[16:, required_columns].drop_duplicates().reset_index(drop=True)
                        print(f"午後データ: {len(pm_data)} 件")
                        if not pm_data.empty:
                            print(f"午後データサンプル:")
                            print(pm_data.head(3))
                        
                        for _, row in pm_data.iterrows():
                            # 病棟名の正規化（リスト形式の文字列を処理）
                            locate_raw = str(row["locate"])
                            if locate_raw.startswith("['") and locate_raw.endswith("']"):
                                # "['ICU']" -> "ICU"
                                locate_clean = locate_raw[2:-2]
                            elif locate_raw == "[]":
                                # 空のリストはスキップ
                                continue
                            else:
                                locate_clean = locate_raw
                            
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
                                "locate": locate_clean,
                                "time": "pm"
                            }
                            schedule_data.append(data_entry)
                            print(f"追加された午後データ: {data_entry}")
                    else:
                        print("午後のデータはありません（16行以下のファイル）")
                    
                    print(f"--- {csv_file} の処理完了 ---")
                    
                except Exception as e:
                    print(f"Error processing file {csv_file}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print(f"\n=== 全ファイル処理完了 ===")
            print(f"総データ件数: {len(schedule_data)}")
            print(f"スケジュールデータの内容:")
            for i, item in enumerate(schedule_data[:10]):  # 最初の10件を表示
                print(f"  {i+1}: {item}")
            if len(schedule_data) > 10:
                print(f"  ... 他 {len(schedule_data) - 10} 件")
            
            # フォルダパスを保存
            page.client_storage.set("folder_name", folder_path)
            page.client_storage.set("schedule_data", schedule_data)
            
            # フォルダ名表示を更新
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
            print(f"フォルダ読み込みエラー: {ex}")
            import traceback
            traceback.print_exc()
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
