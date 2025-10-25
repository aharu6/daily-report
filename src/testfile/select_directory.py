import flet as ft
def main(page: ft.Page):

    def get_directory_result(e:ft.FilePickerResultEvent):
        if e.path:
            page.client_storage.set("selected_directory", e.path)
            page.update()
            print(f"Selected directory: {e.path}")
        else:
            print("No directory selected")
    get_directory = ft.FilePicker(on_result = get_directory_result)

    button = ft.ElevatedButton(
        text = "Select Directory",
        on_click = lambda _:get_directory.get_directory_path()
    )
    page.overlay.extend([get_directory])
    page.update()
    page.add(button)

ft.app(target = main)