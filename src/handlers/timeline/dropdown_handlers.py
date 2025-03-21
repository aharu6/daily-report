import json
import flet as ft

class DropdownHandlers:
    @staticmethod
    def dropdown_changed(e, phName, dialog, page, require_error_message):
        """_summary_

        Args:
            e (_type_): _description_
            phName (_type_): _description_
            dialog (_type_): _description_
            page (_type_): _description_
        """
        if phName.value == "Add":
            dialog.open = True
            page.update()
        else:
            require_error_message.content = None
            page.update()

    @staticmethod
    def update_dropdown(phName, phNameList, page):
        """_summary_

        Args:
            phName (_type_): _description_
            phNameList (_type_): _description_
            page (_type_): _description_
        """
        if isinstance(phNameList, str):
            phNameList = json.loads(phNameList)
        options = []
        try:
            options = [
                ft.dropdown.Option(item["name"], data=item["name"])
                for item in phNameList
            ]
        except:
            options = [ft.dropdown.Option("名前が登録されていません", data="noName")]

        options.append(ft.dropdown.Option("Add"))

        phName.options = options
        page.update()
