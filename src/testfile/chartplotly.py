import plotly.express as px

import flet as ft
from flet.plotly_chart import PlotlyChart

def main(page: ft.Page):

    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color="country")
    #グラフ画像を保存
    fig.write_image("fig_bar.jpg")
    page.add(PlotlyChart(fig, expand=True))

ft.app(main)