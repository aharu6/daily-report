import flet as ft
import datetime
from models.models import DataModel
from handlers.handlers import Handlers

class Panel:
    def __init__(self,page):
        self.page = page
        
    def create(self,page):
        return ft.ExpansionPanelList(
            elevation  = 8,
            controls = [
                ft.ExpansionPanel(
                    expanted = True,
                )
            ]
        )