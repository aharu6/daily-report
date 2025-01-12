import pandas as pd
import ast

read_csv = pd.read_csv(
    "/Users/aizawaharuka/Documents/GitHub/dailyreport/daily-report/app/output_csv/2025-01-12.csv"
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
print(group_df_locate["locate"].unique())


# 病棟分円グラフを作成する
import plotly.express as px
import plotly

fig = px.pie(group_df[group_df["locate"] == "3B"], values="counts", names="Task")
fig.show()
