import plotly.express as px

import flet as ft
from flet.plotly_chart import PlotlyChart
import tempfile
import webbrowser
import os
def main(page: ft.Page):

    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color="country")
    fig.write_image("fig_bar.jpg")
    page.add(PlotlyChart(fig, expand=True))
    
    with tempfile.NamedTemporaryFile(delete=False,suffix=".html") as tmpfile:
        fig.write_html(tmpfile.name)
        html_path= tmpfile.name
    webbrowser.open(f"file://{os.path.abspath(html_path)}")


ft.app(main)