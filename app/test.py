import flet as ft

def main(page:ft.Page):
    page.title = "timeline"
    page.add(ineditButton)
    page.add(delete_button)     
    
# 削除ボタンの定義
delete_button = ft.IconButton(
    icon=ft.icons.REMOVE,
    icon_size=25,
    on_click=lambda _: print("Delete"),
    width=100,
    height=40,
    visible=False  # 初期状態では非表示
)

# editButtonの定義
editButton = ft.TextButton(
    "Edit",
    icon=ft.icons.EDIT,
    on_click=lambda e: toggle_delete_button(e)
)

# 削除ボタンの表示/非表示を切り替える関数
def toggle_delete_button(e):
    delete_button.visible = not delete_button.visible
    delete_button.update()

# e.control.contentにdelete_buttonを追加
def update_content(e, key):
    e.control.content = ft.Column(
        controls=[
            ft.Draggable(
                group="timeline",
                content=ft.Container(
                    ft.Text(key, color="white"),
                    width=50,
                    height=140,
                    bgcolor=ft.colors.BLUE_GREY_500,
                ),
            ),
            create_counter(e.control.data),
            delete_button  # delete_buttonを追加
        ],
        height=300,
        spacing=0,
    )
    e.control.update()

# 他のコード...

# カウンターの関数
def counterPlus(e, count_filed):
    old_Count = int(count_filed.value)
    new_Count = old_Count + 1
    # 更新した値にてカウンター内を更新
    count_filed.value = new_Count
    count_filed.update()
    # dict内の値を更新
    count_dict[e] = {"count": new_Count}

# 他のコード...

# 初期表示
ineditButton = ft.Row(
    controls=[editButton],
    alignment=ft.MainAxisAlignment.END,
)

 # delete_buttonをページに追加

ft.app(main)