import pandas as pd
import ast

read_csv = pd.read_csv(
    "/Users/aizawaharuka/Documents/GitHub/daily/app/output_csv/2025-01-13.csv"
)

# テスト
df1 = read_csv["locate"].apply(ast.literal_eval)
# locateはリスト形式になっているからバラす必要がある

# からのデータフレームを作成

new_rows = []

for index, row in read_csv.iterrows():
    tarn_row = ast.literal_eval(row["locate"])
    for loc in range(len(tarn_row)):
        new_row = row.copy()
        new_row["locate"] = tarn_row[loc]
        new_rows.append(new_row)

df = pd.DataFrame(new_rows)

# データをまとめる
# 病棟ごとに業務でかかった時間の割合を示す円グラフにしたい
# 病棟かつ業務内容ごとにgroupbyして集計する
group_df = df.groupby(["locate", "Task"]).size().reset_index(name="counts")
group_df_locate = df.groupby(["locate"]).size().reset_index(name="counts")


# 病棟分円グラフを作成する
import plotly.express as px
import plotly

fig = px.pie(group_df[group_df["locate"] == "3B"], values="counts", names="Task")
fig.show()


#個人グラフの作成
# horizontal bar chart orientation = "h"にて作成可能
fig_bar_test = px.bar(group_df, x="counts", y="locate", color="Task", barmode="stack",orientation="h")
fig_bar_test.show()

#　個人ごとにデータをまとめ直す
# csvファイルは個人ごとに保存する必要があるから、あとでcsvファイル保存名を変更する
gorup_by_person = df.groupby(["PhName","Task"]).size().reset_index(name="counts")
fig_bar = px.bar(gorup_by_person,x = "counts",y = "PhName",color = "Task",barmode = "stack",orientation = "h")
fig_bar.show()

# bubble chart
group_bubble = df.groupby(["locate","Task","Count"]).size().reset_index(name="times")
#Countsが0の場合とそれ以外に分かれるので、それぞれを合計する
group_bubble2 = group_bubble.groupby(["locate","Task"]).sum(numeric_only=True).reset_index()
#times*15 = かかった時間となるので計算しなおす
group_bubble2["times"] = group_bubble2["times"]*15
fig_bubble = px.scatter(group_bubble2,x = "times",y = "Count",color = "Task",text = "Task" ,
                        )
fig_bubble.update_layout(yaxis =dict(title = "件数"),
                        xaxis = dict(title = "かかった時間")
                        )
fig_bubble.update_traces(textposition='top center')
fig_bubble.show()

