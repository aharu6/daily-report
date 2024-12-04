import flet as ft
from flet import View, Page
import datetime
import csv
import pandas as pd
import json

class ChartPage(ft.Column):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.today = datetime.date.today()
        self.controls = [
            ft.Text("chart", size = 24),
        ]