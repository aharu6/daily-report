from handlers.timeline.drag_move import DragMoveHandler
class DragMoveAddHandler:
    @staticmethod
    def drag_move_handler_add(
        e,page,
        draggable_data,
        delete_buttons,
        columns,
        comments,
        times,
        drag_data,
        comment,
        count_dict,
        ):
        e.control.on_move = DragMoveHandler.drag_move(
            e,
            page,
            draggable_data,
            delete_buttons,
            columns,
            comments,
            times,
            drag_data,
            comment,
            count_dict,
        )
        e.control.update()