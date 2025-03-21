import json
from .dropdown_handlers import DropdownHandlers
class AddNameHandlers:
    @staticmethod
    def add_name(e, phNameList, name_field, page, phName, dialog):
        new_name = name_field.value.strip()
        delspace1=new_name.replace("　","")
        delspace2=delspace1.replace(" ","")
        try:
            phName_List = (
                json.loads(phNameList) if isinstance(phNameList, str) else phNameList
                )
        except:
            phName_List = []

        if delspace2:
            phName_List.append({"name": delspace2})
            page.client_storage.set("phName", phName_List)
            name_field.value = ""
            DropdownHandlers.update_dropdown(phName, phName_List, page)
            dialog.open = False
            page.update()
