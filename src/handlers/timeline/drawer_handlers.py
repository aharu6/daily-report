class DrawerHandlers:
    @staticmethod
    def open_Drawer(e, customDrawerTile, customDrawer, page):
        customDrawerTile.visible = not customDrawerTile.visible
        customDrawer.visible = not customDrawer.visible
        page.update()