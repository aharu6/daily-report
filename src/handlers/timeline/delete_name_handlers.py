class DeleteNameHandler:
    @staticmethod
    def delete_name(e, phNameList, page):
        """_summary_

        Args:
            e (_type_): _description_
            phNameList (_type_): _description_
            page (_type_): _description_
        """
        phNameList.remove(e.control.data)
        page.client_storage.set("phName", phNameList)
        page.update()