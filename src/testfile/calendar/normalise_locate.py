import ast
import pandas as pd

class NormaliseLocate:
    @staticmethod
    def normalise_locate(df,time):
        rows=[]
        for _,row in df.iterrows():
            #locateの値がリスト形式の場合、リストを展開して行を追加
            try:
                locs=ast.literal_eval(row['locate'])
                if not isinstance(locs,list):
                    locs=[row['locate']]

            except Exception:
                locas=[row["locate"]]

            for loc in locs:
                if loc and loc != '[]':

                    rows.append({'locate':loc,'phName':row["phName"],'date':row["date"],'time':time})
        return rows
    