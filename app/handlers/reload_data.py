import json
import datetime
import flet as ft
import csv
import pandas as pd
from models.models import DataModel


#ドロワーを展開する
#保管しているデータを取得して表示する
#右側にtimeline適用用のボタンを合わせて表示する
class ReloadDataHandler:
    @staticmethod
    def toggle_Reload_Data(e,page,drawer):
        page.open(drawer)
        
    
