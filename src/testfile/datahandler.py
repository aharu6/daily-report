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
####件数の合計の算出
count_per_task=dataframes.groupby(["task"])["count"].sum().reset_index(name="counts")
count_per_task["locate"]="all"
#病棟ごとに件数の合計を算出
count_per_task_locate=loc_dataframes.groupby(["locate","task"])["count"].sum().reset_index(name="counts")
#平均値
count_per_task_locate_mean=loc_dataframes.groupby(["locate","task"])["count"].mean().reset_index(name="counts")
count_per_task_locate_mean["locate"]="mean"  
#count_per_task_locateとcount_per_taskを結合
sum_task_counts=pd.merge(
    [count_per_task_locate,
    count_per_task,
    count_per_task_locate_mean],
    on=["locate", "task","counts"],
    how="outer",
)#病棟全ての合計と病棟ごとの合計
#件数入力しない（混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンス）
task_counts_fil=sum_task_counts.query("task != '混注時間'")
task_counts_fil=task_counts_fil.query("task != '休憩'")
task_counts_fil=task_counts_fil.query("task != '委員会'")
task_counts_fil=task_counts_fil.query("task != 'WG活動'")
task_counts_fil=task_counts_fil.query("task != '勉強会参加'")
task_counts_fil=task_counts_fil.query("task != '1on1'")
task_counts_fil=task_counts_fil.query("task != 'カンファレンス'")

#
#task_counts_fil2=sum_task_counts[sum_task_counts["task"]!="混時"]

sum_task_counts_pi=sum_task_counts.pivot_table(
    values=["counts"],
    index=["task"],
    columns=["locate"],
    fill_value=0,
)
#件数集計していない業務は削除する
#件数入力しない（混注時間、休憩、委員会、WG活動,勉強会参加、1on1、カンファレンス）
#上記業務内容を入力していない場合はdropでエラーになるから、止まらないようにする
try:
    sum_task_counts_pi.drop(index=["無菌調製関連業務"],inplace=True)
    sum_task_counts_pi.drop(index=["混注時間"],inplace=True)#混注時間→無菌調製関連業務
    sum_task_counts_pi.drop(index=["休憩"],inplace=True)
    sum_task_counts_pi.drop(index=["委員会"],inplace=True)
    sum_task_counts_pi.drop(index=["WG活動"],inplace=True)
    sum_task_counts_pi.drop(index=["勉強会参加"],inplace=True)
    sum_task_counts_pi.drop(index=["1on1"],inplace=True)
    sum_task_counts_pi.drop(index=["カンファレンス"],inplace=True)
except KeyError:
    pass

#sum_task_counts_piの列名をcountsからlocateに変更
#最上位ラベルのcountsを削除
sum_task_counts_pi.columns=sum_task_counts_pi.columns.droplevel(0)
"""for i in range(len(sum_task_counts_pi.columns)):
    print(sum_task_counts_pi.columns[i])
#fletアプリ上にてデータフレームを表示
for row in sum_task_counts_pi.itertuples( name="Row"):
    for j in range(len(sum_task_counts_pi.columns)):
        print(row[j])
"""#時間の算出
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
#負の欠損ちinfはNanとして欠損値として扱う
#データフレームの列名をlocateに変更 横長に変換 (1件あたりに要した時間を計算)
#件数を入力しない業務はcountが0になるのでtime_per_taskはNaNになる
#NaNになると横長に直したとき自動的に削除される
#他のフレーム件数を入力しないものは除外するか
time_per_task_pi_time_per_task=time_per_task.pivot_table(
        values=["time_per_task"],
        index=["task"],
        columns=["locate"],
        fill_value=0,
        )

#同様に件数の合計フレームを作成
time_per_task_pi_count=time_per_task.pivot_table(
        values=["counts"],
        index=["task"], 
        columns=["locate"],
        fill_value=0,
)
#件数入力しない業務は削除する
try:
    time_per_task_pi_count.drop(index=["無菌調製関連業務"],inplace=True)#混注時間→無菌調製関連業務
    time_per_task_pi_count.drop(index=["混注時間"],inplace=True)
    time_per_task_pi_count.drop(index=["休憩"],inplace=True)
    time_per_task_pi_count.drop(index=["委員会"],inplace=True)
    time_per_task_pi_count.drop(index=["WG活動"],inplace=True)
    time_per_task_pi_count.drop(index=["勉強会参加"],inplace=True)
    time_per_task_pi_count.drop(index=["1on1"],inplace=True)
    time_per_task_pi_count.drop(index=["カンファレンス"],inplace=True)  
except KeyError:
    pass

#同様に時間の合計フレームを作成
time_per_task_pi_time=time_per_task.pivot_table(
        values=["times"],
        index=["task"], 
        columns=["locate"],
        fill_value=0,
)
#fletアプリ上にてデータフレームを表示
#time_per_taskをcsvファイルとして保存

#病棟ごとの件数あたりの時間算出も必要か

