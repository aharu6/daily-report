class RequireLocationMessage:
    @staticmethod
    def change_require_location(e,require_location,page):
        print(require_location)
        require_location.visible = False
        page.update()