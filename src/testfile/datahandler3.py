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


#sum,mean()関数を使用して、横長データフレームにした後に合計値列を平均値列を追加する
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
#病棟ごとに合計値を算出
count_per_task_locate=loc_dataframes.groupby(["locate","task"])["count"].sum().reset_index(name="counts")

#横長データフレームに変換
sum_task_counts=count_per_task_locate.pivot_table(
    index="task",values="counts",columns="locate",fill_value=0
    )

#合計値列と平均値列を追加する
sum_task_counts["sum"]=sum_task_counts.sum(axis=1)
sum_task_counts["mean"]=sum_task_counts.iloc[:,:-1].mean(axis=1)


#病棟ごとに合計時間と平均値を算出
count_per_task_locate=loc_dataframes.groupby(["locate","task"]).size().reset_index(name="times")
#*15にすることで実際の時間に変換　(1入力15ふん）
count_per_task_locate["times"]=count_per_task_locate["times"]*15
#横長データフレームに変換
sum_task_times=count_per_task_locate.pivot_table(
    index="task",values="times",columns="locate",fill_value=0
    )# 病棟ごとの合計時間

#病棟ごとの　1件あたりどれくらい時間がかかっているのか
time_locate_df=loc_dataframes.groupby(["locate"])["count"].sum().reset_index(name="count")
time_locate_times=loc_dataframes.groupby(["locate"]).size().reset_index(name="times")
#*15にすることで実際の時間に変換　(1入力15ふん）
time_locate_times["times"]=time_locate_times["times"]*15

time_for_locate_df=pd.merge(
    time_locate_df,
    time_locate_times,
    on="locate",
    how="left"
)#病棟ごとの件数と時間の合計
#１件あたりの列を追加
time_for_locate_df["time_per_task"]=time_for_locate_df["times"]/time_for_locate_df["count"]
print(time_for_locate_df)

#薬剤師ごとの件数と時間の合計
time_for_locate_phName_times=loc_dataframes.groupby(["phName","task"]).size().reset_index(name="times")
#*15にすることで実際の時間に変換　(1入力15ふん）
time_for_locate_phName_times["times"]=time_for_locate_phName_times["times"]*15
#薬剤師ごとの件数を算出
time_for_locate_phName_df=loc_dataframes.groupby(["phName","task"])["count"].sum().reset_index(name="count")
#薬剤師ごとの件数と時間の合計
time_for_locate_phName_df=pd.merge(
    time_for_locate_phName_df,
    time_for_locate_phName_times,
    on=["phName","task"],
    how="left"
)
#１件あたりの平均値を算出
time_for_locate_phName_df["time_per_task"]=time_for_locate_phName_df["times"]/time_for_locate_phName_df["count"]
print(time_for_locate_phName_df)