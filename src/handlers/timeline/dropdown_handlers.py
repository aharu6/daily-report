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

    @staticmethod
    def ensure_name_option(phName, name):
        # 読み込んだ名前が選択肢に無いとき、一時的に選択肢へ追加する（#323）
        # 登録リスト自体は変更しない
        if not name:
            return
        options = list(phName.options or [])
        if name not in [option.key for option in options]:
            options.append(ft.dropdown.Option(name))
            phName.options = options

    @staticmethod
    def register_name(page, phName, name):
        # 保存時、未登録の名前なら端末の名前リストへ登録する（#323）
        if not name or name == "Add":
            return
        raw = page.client_storage.get("phName")
        if raw is None:
            name_list = []
        elif isinstance(raw, str):
            try:
                name_list = json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                name_list = []
        else:
            name_list = raw
        if not isinstance(name_list, list):
            name_list = []
        if any(
            isinstance(item, dict) and item.get("name") == name
            for item in name_list
        ):
            return
        name_list.append({"name": name})
        page.client_storage.set("phName", name_list)
        DropdownHandlers.update_dropdown(phName, name_list, page)
