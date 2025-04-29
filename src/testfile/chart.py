import pandas as pd
import ast


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
df=pd.DataFrame(loc_dataframes)


# テスト
#df1 = read_csv["locate"].apply(ast.literal_eval)
# locateはリスト形式になっているからバラす必要がある
# AMを除くもしくはリストでないものをスキップする

# からのデータフレームを作成
"""
new_rows = []

for index, row in read_csv.iterrows():
    tarn_row = ast.literal_eval(row["locate"])
    for loc in range(len(tarn_row)):
        new_row = row.copy()
        new_row["locate"] = tarn_row[loc]
        new_rows.append(new_row)

df = pd.DataFrame(new_rows)
"""
# データをまとめる
# 病棟ごとに業務でかかった時間の割合を示す円グラフにしたい
# 病棟かつ業務内容ごとにgroupbyして集計する
group_df = df.groupby(["locate", "task"]).size().reset_index(name="counts")
group_df_locate = df.groupby(["locate"]).size().reset_index(name="counts")

# 入力した名前にスペース（全角、半角）が含まれている場合は削除する

# 病棟分円グラフを作成する
import plotly.express as px
import plotly as py


fig = px.pie(group_df[group_df["locate"] == "4B"], values="counts", names="task")
#fig.show()


# 個人グラフの作成
# horizontal bar chart orientation = "h"にて作成可能
fig_bar_test = px.bar(
    group_df, x="counts", y="locate", color="task", barmode="stack", orientation="h"
)
#fig_bar_test.show()

# 　個人ごとにデータをまとめ直す
# csvファイルは個人ごとに保存する必要があるから、あとでcsvファイル保存名を変更する
gorup_by_person = df.groupby(["phName", "task"]).size().reset_index(name="counts")
fig_bar = px.bar(
    gorup_by_person,
    x="counts",
    y="phName",
    color="task",
    barmode="stack",
    orientation="h",
)
pri=df.groupby("task").size().reset_index(name="counts")
print(gorup_by_person["phName"].unique())
fig_bar.show()

# bubble chart
group_bubble = df.groupby(["locate", "task", "count"]).size().reset_index(name="times")
# Countsが0の場合とそれ以外に分かれるので、それぞれを合計する
group_bubble2 = (
    group_bubble.groupby(["locate", "task"]).sum(numeric_only=True).reset_index()
)
# times*15 = かかった時間となるので計算しなおす
group_bubble2["times"] = group_bubble2["times"] * 15
fig_bubble = px.scatter(
    group_bubble2,
    x="times",
    y="count",
    color="task",
    text="task",
)
fig_bubble.update_layout(yaxis=dict(title="件数"), xaxis=dict(title="かかった時間"))
fig_bubble.update_traces(textposition="top center")
#fig_bubble.show()
