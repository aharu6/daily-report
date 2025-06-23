import flet as ft
import tempfile
import webbrowser
import os

class PreviewChartHandler:
    @staticmethod
    def preview_chart(fig):
        with tempfile.NamedTemporaryFile(delete=False,suffix=".html") as tmpfile:
            fig.write_html(tmpfile.name)
            heml_path = tmpfile.name

        webbrowser.open(f"file://{os.path.abspath(heml_path)}")