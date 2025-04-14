

import pandas as pd
import ast
import plotly.express as px

# 全ての行と列を表示する設定
pd.set_option('display.max_rows', None)  # 行を省略せずに表示
pd.set_option('display.max_columns', None)  # 列を省略せずに表示
pd.set_option('display.expand_frame_repr', False)  # データフレームを横にスクロールせずに表示
pd.set_option('display.max_colwidth', None)  # 列の幅を省略せずに表示

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
#####時間帯（time列）ごとにどのタスクが多いかを分析。
#時間帯ごとにその種類のtaskが行われた回数（件数とは別       ）
#時間帯ごとにgroupbyして集計する
group_time_df=dataframes.groupby(["time","task"]).size().reset_index(name="counts")

# 時間帯ごとのタスクを積み上げ棒グラフで可視化
fig = px.bar(
    group_time_df,
    x="time",
    y="counts",
    color="task",
    title="Task Distribution by Time",
    labels={"time": "Time", "counts": "Task Count", "task": "Task"},
    barmode="stack",
)

# グラフを表示
#fig.show()
#各タスクがどの時間帯に集中しているかを分析するヒートマップ
#業務内容ー時間帯
task_per_time_heatmap=dataframes.groupby(["task","time"]).size().reset_index(name="counts")
#時間帯ごとのタスクをヒートマップで可視化
fig = px.density_heatmap(
    task_per_time_heatmap,
    x="time",
    y="task",
    z="counts",
    title="Task Distribution by Time (Heatmap)",
    labels={"time": "Time", "task": "Task", "counts": "Task Count"},
)
# グラフを表示
#fig.show()

####各タスクのcount列の合計値や平均値を計算
#あとで表示期間を選択して、期間ごとの合計値や平均値を計算するようにする
# 各タスクの合計値を計算
task_sum=dataframes.groupby("task")["count"].sum().reset_index()
#切り替えボタンを設置して病棟ごとの合計を出すか
# 各タスクの平均値を計算
#表示期間あたり、1日あたりの平均が妥当か
task_mean=dataframes.groupby("task")["count"].mean().reset_index()

####各タスクがどの場所（locate列）で行われたかを集計。 時間ー業務ー場所 一番目の時間と類似している
locate_df=dataframes.groupby(["locate","task"]).size().reset_index(name="counts")
#locateごとのタスクを積み上げ棒グラフで可視化
fig = px.bar(
    locate_df,
    x="locate",
    y="counts",
    color="task",
    title="Task Distribution by Location",
    labels={"locate": "Location", "counts": "Task Count", "task": "Task"},
    barmode="stack",
)
# グラフを表示
#fig.show()

###各タスクがどの時間帯に集中しているかを分析
#業務内容ー時間帯
task_per_time = dataframes.groupby(["task", "time"]).size().reset_index(name="counts")  # 修正: "coutns" -> "counts"
#時間帯に業務が記録されていない時は時間帯ー０にて補完したい

#業務内容ごとにグラフを作成する
for task in task_per_time["task"].unique():
    task_data = task_per_time[task_per_time["task"] == task]
    fig = px.bar(
        task_data,
        x="time",
        y="counts",  # 修正: "coutns" -> "counts"
        title=f"Task Distribution for {task}",
        labels={"time": "Time", "counts": "Task Count"},
    )
#   fig.show  
# グラフを表示


#date列を基に、日付ごとのタスクの分布を分析
#date列をdatetime型に変換
date_par_task=dataframes
date_par_task["date"]=pd.to_datetime(date_par_task["date"])
#date列を基に、日付ごとのタスクの分布を分析
#date列を基に、日付ごとのタスクの分布を分析
date_group_df=date_par_task.groupby(["date","task"]).size().reset_index(name="counts")
#counts は時間になる*15をすると作業時間となる
#dateごとのタスクを積み上げ棒グラフで可視化
fig = px.bar(
    date_group_df,
    x="date",
    y="counts",
    color="task",
    title="Task Distribution by Date",
    labels={"date": "Date", "counts": "Task Count", "task": "Task"},
    barmode="stack",
)
# グラフを表示
#fig.show()


##件数あたりに要した時間の算出
#件数列を合計しておく
count_per_task=dataframes.groupby(["task"])["count"].sum().reset_index(name="counts")
count_per_task["locate"]="all"
#病棟ごとに件数の合計を算出
count_per_task_locate=loc_dataframes.groupby(["locate","task"])["count"].sum().reset_index(name="counts")
#count_per_task_locateとcount_per_taskを結合
sum_task_counts=pd.merge(
    count_per_task_locate,
    count_per_task,
    on=["locate", "task","counts"],
    how="outer",
)#病棟全ての合計と病棟ごとの合計

#時間の算出
time_per_task_all=dataframes.groupby(["task"]).size().reset_index(name="times")
time_per_task_all["counts"]=count_per_task["counts"]
#times列に*15することで、時間に変換
time_per_task_all["times"]=time_per_task_all["times"]*15
time_per_task_all["locate"]="all"   
#病棟ごとに同様に算出
time_per_task_locate=loc_dataframes.groupby(["locate","task"]).size().reset_index(name="times")
time_per_task_locate["counts"]=count_per_task_locate["counts"]
#times列に*15することで、時間に変換
time_per_task_locate["times"]=time_per_task_locate["times"]*15
#time_per_task_allとtime_per_task_locateを結合
time_per_task=pd.merge(
    time_per_task_locate,
    time_per_task_all,
    on=["locate", "task","times","counts"],
    how="outer",
)
#新しいtime/taskにて１件あたりに要した時間を計算
time_per_task["time_per_task"]=time_per_task["times"]/time_per_task["counts"]
#fletアプリ上にてデータフレームを表示
#time_per_taskをcsvファイルとして保存
time_per_task.to_csv("time_per_task.csv", index=False)