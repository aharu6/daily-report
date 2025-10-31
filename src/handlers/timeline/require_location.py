class RequireLocationMessage:
    @staticmethod
    def change_require_location(e,require_location,page):
        require_location.content.controls[0].visible = False
        page.update()

    @staticmethod
    def am_change_require_location(e,require_location,page,total_num):        
        if e.data=="true":
            total_num["count"]+=1
        elif e.data=="false":
            total_num["count"]-=1
        import flet as ft
        if total_num["count"]>0:
            require_location.content.controls[1].title.color="green"
            require_location.content.controls[1].leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color="green")
            require_location.content.controls[1].data="true"
        elif total_num["count"]==0:
            require_location.content.controls[1].title.color="red"
            require_location.content.controls[1].leading=ft.Icon(ft.icons.HIGHLIGHT_OFF, color="red")
            require_location.content.controls[1].data="false"
            require_location.content.controls[0].visible =True
            require_location.content.controls[2].visible =True

        if require_location.content.controls[1].data=="true" and require_location.content.controls[2].data=="true":
            require_location.content.controls[0].visible =False
            require_location.content.controls[1].visible =False
            require_location.content.controls[2].visible =False

        page.update()
        return total_num

    @staticmethod
    def pm_change_require_location(e,require_location,page,total_num):
        if e.data=="true":
            total_num["count"]+=1
        elif e.data=="false":
            total_num["count"]-=1

        import flet as ft
        if total_num["count"]>0:
            require_location.content.controls[2].title.color="green"
            require_location.content.controls[2].leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color="green")
            require_location.content.controls[2].data="true"
        elif total_num["count"]==0:
            require_location.content.controls[2].title.color="red"
            require_location.content.controls[2].leading=ft.Icon(ft.icons.HIGHLIGHT_OFF, color="red")
            require_location.content.controls[2].data="false"
            require_location.content.controls[0].visible =True
            require_location.content.controls[1].visible =True

        
        if require_location.content.controls[1].data=="true" and require_location.content.controls[2].data=="true":
            require_location.content.controls[0].visible =False
            require_location.content.controls[1].visible =False
            require_location.content.controls[2].visible=False
        page.update()
        return total_num