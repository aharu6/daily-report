class RequireLocationMessage:
    @staticmethod
    def change_require_location(e,require_location,page):
        require_location.visible = False
        page.update()