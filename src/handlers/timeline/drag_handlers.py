from models.models import DataModel
import flet as ft
from .handdrag_will_accept import Add_will_accept
from .color_handlers import ColorHandlers
from flet import BoxShape
from .make_popup import MakePopup
from .counter_handlers import CounterHandlers

class DragHandlers:
    @staticmethod
    def drag_accepted(
        e,
        page,
        draggable_data,
        columns,
        comments,
        times,
        drag_data,
        comment,
        count_dict,
        phNameList,
        phName,
        comment_dict,
        draggable_data_for_move,
        customDrawerAm,
        customDrawerPm,
        update_location_data,
        radio_selected_data,
        date,
    ):
        model = DataModel()

        # print(e.target)
        src_id_str = e.src_id.replace("_", "")
        try:
            src_id_int = int(src_id_str)
            # 次カラム
            next_id = f"_{src_id_int + 4}"
        except:
            pass
        if page.get_control(e.src_id):
            src = page.get_control(e.src_id)
            try:
                if isinstance(src.data["task"], dict):
                    key = src.data["task"]["task"]
                else:
                    key = src.data["task"]
            except:
                key = src.data["task"]

        elif e.src_id in draggable_data and "task":
            key = draggable_data[e.src_id]["task"]

        elif page.get_control(e.target):
            src = page.get_control(e.target)
            try:
                if isinstance(src.data["task"], dict):
                    key = src.data["task"]["task"]
                else:
                    key = src.data["task"]
            except:
                key = src.data["task"]

        e.control.content = ft.Column(
            controls=[
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    visible=False,
                    icon_size=20,
                    icon_color="red",
                    on_click=lambda e: DragHandlers.delete_content(
                        e=e,
                        page=page,
                        phNameList=phNameList,
                        phName=phName,
                        drag_data=drag_data,
                        count_dict=count_dict,
                        comment_dict=comment_dict,
                        columns=columns,
                        draggable_data_for_move=draggable_data_for_move,
                        comments=comments,
                        times=times,
                        comment=comment,
                        draggable_data=draggable_data,
                        update_location_data=update_location_data,
                        customDrawerAm=customDrawerAm,
                        customDrawerPm=customDrawerPm,
                        radio_selected_data=radio_selected_data,
                        date=date,
                    ),
                    data={"num": e.control.data["num"]},
                ),
                ft.Draggable(
                    group="timeline_accepted",
                    content=ft.Container(
                        content=ft.Text(
                            key, color="white", text_align=ft.TextAlign.CENTER
                        ),
                        width=50,
                        height=130,
                        bgcolor=ColorHandlers.change_color(key),
                        border_radius=ft.border_radius.only(top_left=5, bottom_left=5),
                        shape=BoxShape.RECTANGLE,
                    ),
                    data={
                        "time": e.control.data["time"],
                        "num": e.control.data["num"],
                        "task": key,
                    },
                ),
                ft.PopupMenuButton(
                    items=[
                        MakePopup.add_popup(
                            time=e.control.data["time"],
                            update_location_data=update_location_data,
                            num=e.control.data["num"],
                            columns=columns,
                            page=page,
                            radio_selected_data=radio_selected_data,
                            date=date,
                        ),
                    ],
                    tooltip="編集",
                    icon=ft.icons.MORE_VERT,
                    icon_size=20,
                    on_open=lambda e: MakePopup.pop_up_reload(
                        e=e,
                        customDrawerAm=customDrawerAm,
                        customDrawerPm=customDrawerPm,
                        page=page,
                    ),
                    data={
                        "time": e.control.data["time"],
                    },
                ),
                ft.Container(),
            ],
            height=370,
            spacing=0,
            data={
                "time": e.control.data["time"],
                "num": e.control.data["num"],
                "task": key,
            },
        )
        e.control.on_will_accept = None
        e.control.on_accept = None

        columns[e.control.data["num"]].content.data["task"] = key

        match key:
            case "その他":
                e.control.content.controls.append(comments[e.control.data["num"]])
            case (
                "混注時間"
                | "休憩"
                | "委員会"
                | "WG活動"
                | "勉強会参加"
                | "1on1"
                | "カンファレンス"
                | "業務調整"
            ):
                pass
            case _:
                e.control.content.controls.append(
                    CounterHandlers.create_counter(e.control.data["time"], count_dict)
                )

        drag_data[e.control.data["time"]] = {"task": key}
        if e.control.data["task"] == "その他":
            comments[e.control.data["num"]].data = {
                "time": e.control.data["time"],
                "num": e.control.data["num"],
            }
        e.control.group = "timeline_accepted"
        page.update()

    @staticmethod
    def delete_content(
        e,
        page,
        phNameList,
        phName,
        drag_data,
        count_dict,
        comment_dict,
        columns,
        draggable_data_for_move,
        comments,
        times,
        comment,
        draggable_data,
        update_location_data,
        customDrawerAm,
        customDrawerPm,
        radio_selected_data,
        date,
    ):
        from handlers.timeline.drag_leave import DragLeave

        col_num = e.control.data["num"]
        columns[col_num].content = ft.DragTarget(
            group="delete_toggle",
            content=ft.Container(
                width=50,
                height=370,
                bgcolor="#CBDCEB",
                border_radius=5,
            ),
            on_will_accept=lambda e: Add_will_accept.drag_will_accept(
                e, page, columns, drag_data
            ),
            on_accept=lambda e: DragHandlers.drag_accepted(
                e=e,
                page=page,
                draggable_data_for_move=draggable_data_for_move,
                columns=columns,
                comments=comments,
                times=times,
                drag_data=drag_data,
                comment=comment,
                count_dict=count_dict,
                phNameList=phNameList,
                phName=phName,
                comment_dict=comment_dict,
                draggable_data=draggable_data,
                update_location_data=update_location_data,
                customDrawerAm=customDrawerAm,
                customDrawerPm=customDrawerPm,
                radio_selected_data=radio_selected_data,
                date=date,
            ),
            on_leave=lambda e: DragLeave.drag_leave(e, page),
            data={"time": times[col_num], "num": col_num, "task": ""},
        )

        right_col_num = e.control.data["num"] + 1
        try:
            right_key = columns[right_col_num].content.data["task"]
        except:
            right_key = None

        page.add(columns[col_num].content.content)

        model = DataModel()

        while right_key == "will_accept":
            columns[right_col_num].content = ft.DragTarget(
                group="delete_toggle",
                content=ft.Container(
                    width=50,
                    height=370,
                    bgcolor="#CBDCEB",
                    border_radius=5,
                ),
                data={"time": times[right_col_num], "num": right_col_num, "task": ""},
                on_accept=lambda e: DragHandlers.drag_accepted(
                    e=e,
                    page=page,
                    draggable_data_for_move=draggable_data_for_move,
                    columns=columns,
                    comments=comments,
                    times=times,
                    drag_data=drag_data,
                    comment=comment,
                    count_dict=count_dict,
                    phNameList=phNameList,
                    phName=phName,
                    comment_dict=comment_dict,
                    draggable_data=draggable_data,
                    update_location_data=update_location_data,
                    customDrawerAm=customDrawerAm,
                    customDrawerPm=customDrawerPm,
                    radio_selected_data=radio_selected_data,
                    date=date,
                ),
                on_leave=lambda e: DragLeave.drag_leave(e, page),
                on_will_accept=lambda e: Add_will_accept.drag_will_accept(
                    e, page, columns, drag_data
                ),
            )
            del drag_data[model.times()[right_col_num]]
            if model.times()[right_col_num] in count_dict:
                del count_dict[model.times()[right_col_num]]
            if model.times()[right_col_num] in comment_dict:
                del comment_dict[model.times()[right_col_num]]

            right_col_num += 1
            right_key = columns[right_col_num].content.data["task"]
        else:
            pass
        page.update()

        del drag_data[model.times()[col_num]]
        if model.times()[col_num] in count_dict:
            del count_dict[model.times()[col_num]]
        if model.times()[col_num] in comment_dict:
            del comment_dict[model.times()[col_num]]