import json
class DeleteNameHandler:
    @staticmethod
    def delete_name(e, phNameList, page):
        """_summary_

        Args:
            e (_type_): _description_
            phNameList (_type_): _description_
            page (_type_): _description_
        """
        new_phNameList = phNameList.remove(e.control.data)
        page.set("phName", json.dumps(new_phNameList, ensure_ascli=False))
        page.update()