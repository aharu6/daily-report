from .handle_change import HandleChange
from .dropdown_handlers import DropdownHandlers
from .dialog_handlers import DialogHandlers
from .drag_handlers import DragHandlers
from .color_handlers import ColorHandlers
from .counter_handlers import CounterHandlers
from .choice_change_handlers import ChoiceChangeHandlers
from .drawer_handlers import DrawerHandlers
from .add_name_handlers import AddNameHandlers
from .delete_name_handlers import DeleteNameHandler
from .toggle_delete_handler import DeleteButtonHandler
class Handlers:
    handle_change = HandleChange.handle_change
    dropdown_changed = DropdownHandlers.dropdown_changed
    update_dropdown = DropdownHandlers.update_dropdown
    close_dialog = DialogHandlers.close_dialog
    create_dialog_for_comment = DialogHandlers.create_dialog_for_comment
    add_comment_for_dict = DialogHandlers.add_comment_for_dict
    drag_accepted = DragHandlers.drag_accepted
    delete_content = DragHandlers.delete_content
    change_color = ColorHandlers.change_color
    counterPlus = CounterHandlers.counterPlus
    counterMinus = CounterHandlers.counterMinus
    create_counter = CounterHandlers.create_counter
    dlg_close=DialogHandlers.close_dialog
    dlg_open=DialogHandlers.create_dialog_for_comment
    change_choice_button=ChoiceChangeHandlers.change_choice_button
    open_Drawer=DrawerHandlers.open_Drawer
    add_name=AddNameHandlers.add_name
    delete_name=DeleteNameHandler.delete_name
    toggle_delete_button=DeleteButtonHandler.toggle_delete_button
