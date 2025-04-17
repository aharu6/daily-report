import pandas as pd
import ast
import plotly.express as px


# 全ての行と列を表示する設定
pd.set_option('display.max_rows', None)  # 行を省略せずに表示
pd.set_option('display.max_columns', None)  # 列を省略せずに表示
pd.set_option('display.expand_frame_repr', False)  # データフレームを横にスクロールせずに表示
pd.set_option('display.max_colwidth', None)  # 列の幅を省略せずに表示
pd.options.mode.use_inf_as_na=True
folder_path = "/Users/aizawaharuka/Documents/output_csv/"
#folder_path内のcsvファイルを取得
import os
import glob
file_list=glob.glob(os.path.join(folder_path, "*.csv"))
#csvファイルを読み込む
dataframes=pd.concat([
    pd.read_csv(file) for file in file_list
])
#病棟名のリストはバラす
loc_dataframes=[]
for index,row in dataframes.iterrows():
    try:

        if isinstance(row["locate"], str):

            tarn_row=ast.literal_eval(row["locate"])
            for loc in range(len(tarn_row)):
                new_row=row.copy()
                new_row["locate"]=tarn_row[loc]
                loc_dataframes.append(new_row)
        else:
            continue

    except (ValueError, SyntaxError):
        # locate列がリスト形式でない場合はスキップ
        continue    

loc_dataframes=pd.DataFrame(loc_dataframes)

print(loc_dataframes.head())
#その他コメントの表示
#日付と場所と記録された時間帯、記録者、コメントの内容が必要か
#コメントを含む行のみを抽出する
comment_df=loc_dataframes[loc_dataframes["comment"].notna()]
#count列は不要なので削除する
comment_df=comment_df.drop(columns=["count","task"])
#time,locate,date,phName,comment列飲み抽出する
comment_df=comment_df[["time","locate","date","phName","comment"]]
print(comment_df)