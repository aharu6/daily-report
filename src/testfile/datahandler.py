import pandas as pd
import ast
import plotly.express as px


folder_path = "/Users/aizawaharuka/Documents/output_csv/"
#folder_path内のcsvファイルを取得
import os
import glob
file_list=glob.glob(os.path.join(folder_path, "*.csv"))
#csvファイルを読み込む
dataframes=pd.concat([
    pd.read_csv(file) for file in file_list
])

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
 #   fig.show()
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


#件数あたりに要した時間の算出
#件数列を合計しておく
time_per_task=dataframes.groupby(["task"]).size().reset_index(name="times")
count_per_task=dataframes.groupby(["task"])["count"].sum().reset_index(name="counts")
time_per_task["counts"]=count_per_task["counts"]
#times列に*15することで、時間に変換
time_per_task["times"]=time_per_task["times"]*15
#新しいtime/taskにて１件あたりに要した時間を計算
time_per_task["time_per_task"]=time_per_task["times"]/time_per_task["counts"]
print(time_per_task)
#fletアプリ上にてデータフレームを表示