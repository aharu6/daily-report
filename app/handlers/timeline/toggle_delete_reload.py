#reload後のdeletebutton用のtoggle関数
class Toggle_delete_reload:
    @staticmethod
    def toggle_delete_button(page,columns):
        for i in range(len(columns)):
            task = columns[i].content.data["task"]
            match task:
                case "will_acept":
                    pass
                case "":
                    pass
                case _:
                    columns[i].content.controls[0].visible = not columns[i].content.controls[0].visible
        
