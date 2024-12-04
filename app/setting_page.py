import flet as ft
from flet import View, Page
import datetime
import csv
import pandas as pd
import json

class SettingPage(ft.Column):
    def __init__(self):
        super().__init__()
        self.today = datetime.date.today()
        self.controls = [
            ft.Text("setting", size = 24),
        ]