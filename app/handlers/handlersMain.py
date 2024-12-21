import json
import datetime
import flet as ft
import csv
import pandas as pd
from models.models import DataModel

#ページ遷移の共通ハンドラを定義
class Handlers_Main:
    @staticmethod
    def on_navigation_change(e,page):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/")
        elif selected_index == 1:
            page.go("/chart")
        elif selected_index == 2:
            page.go("/settings")