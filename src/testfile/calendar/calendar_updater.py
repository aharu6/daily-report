import flet as ft
from create_calendar import CreateCalendar
from update_card import UpdateCard
from update_calendar import UpdateCalendar

class CalendarUpdater:
    @staticmethod
    def update_calendar_and_text(e, is_forward, page, tab_calendar, label, schedule_data, tab_header, switch_value):
        """カレンダー更新時に年月表示、カードも更新する関数
        
        Args:
            e: イベント
            is_forward (bool): True=次の月, False=前の月
            page: ページオブジェクト
            tab_calendar: カレンダーオブジェクト
            label (str): 病棟名
            schedule_data: スケジュールデータ
            tab_header: 年月表示用テキスト
        """
        # switch_valueがFalse（個人名絞り込み）の場合はチェックボックスを保持
        if switch_value is False:
            # チェックボックス要素を一時保存（月変更前に実行）
            saved_checkboxes = []
            checkbox_container = None
            
            def find_checkboxes_recursive(element):
                """再帰的にチェックボックスを探す関数"""
                checkboxes = []
                
                # 直接チェックボックスかどうかを確認
                if isinstance(element, ft.Checkbox):
                    print(f"Found checkbox: {element.label}, value: {element.value}")
                    checkboxes.append({
                        'label': element.label,
                        'value': element.value,
                        'data': element.data,
                    })
                    return checkboxes
                
                # controlsプロパティがある場合、その中を検索
                if hasattr(element, 'controls') and element.controls:
                    for control in element.controls:
                        checkboxes.extend(find_checkboxes_recursive(control))
                
                # contentプロパティがある場合、その中を検索
                if hasattr(element, 'content') and element.content:
                    checkboxes.extend(find_checkboxes_recursive(element.content))
                
                return checkboxes

            # チェックボックスを保存
            saved_checkboxes = find_checkboxes_recursive(tab_calendar)

            # チェックボックスのコンテナを探す
            def find_checkbox_container(element):
                if hasattr(element, 'controls') and element.controls:
                    for control in element.controls:
                        if isinstance(control, ft.Checkbox):
                            return element
                        # ResponsiveRowの場合、その中のチェックボックスを確認
                        if hasattr(control, 'controls') and control.controls:
                            for sub_control in control.controls:
                                if isinstance(sub_control, ft.Checkbox):
                                    return control
                        container = find_checkbox_container(control)
                        if container:
                            return container
                if hasattr(element, 'content') and element.content:
                    return find_checkbox_container(element.content)
                return None

            checkbox_container = find_checkbox_container(tab_calendar)

            # 月を変更
            if is_forward:
                CreateCalendar.forward_month(e=e, page=page, calendar=tab_calendar, card_name=label)
            else:
                CreateCalendar.back_month(e=e, page=page, calendar=tab_calendar, card_name=label)

            # 年月表示を更新
            tab_header.value = f"{tab_calendar.year}年{tab_calendar.month}月"
            tab_header.update()

            # カレンダーセルの色のみ更新
            UpdateCalendar.update_calendar_with_schedule_data(
                e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls,
                card_name=None, filter_name=None
            )
            
            # チェックボックスを復元（状態も含めて）
            if saved_checkboxes:
                # 説明テキストを追加
                has_instruction_text = False
                for control in tab_calendar.controls:
                    if isinstance(control, ft.Text) and "絞り込みを行う名前を選択" in str(control.value):
                        has_instruction_text = True
                        break
                
                if not has_instruction_text:
                    tab_calendar.controls.append(
                        ft.Text("絞り込みを行う名前を選択、選択後は再度更新ボタンを押す")
                    )
                
                # チェックボックスを復元
                restored_checkboxes = []
                for checkbox_data in saved_checkboxes:
                    new_checkbox = ft.Checkbox(
                        label=checkbox_data['label'],
                        value=checkbox_data['value'],  # 選択状態を復元
                        data=checkbox_data['data'],
                    )
                    restored_checkboxes.append(new_checkbox)
                
                # ResponsiveRowでチェックボックスをラップ
                checkbox_row = ft.ResponsiveRow(controls=restored_checkboxes)
                tab_calendar.controls.append(checkbox_row)
                print(f"復元したチェックボックスの数: {len(restored_checkboxes)}")
            
            tab_calendar.update()
            return

        # 通常の処理（病棟絞り込みの場合）
        if is_forward:
            CreateCalendar.forward_month(e=e, page=page, calendar=tab_calendar, card_name=label)
        else:
            CreateCalendar.back_month(e=e, page=page, calendar=tab_calendar, card_name=label)

        # 年月表示を更新
        tab_header.value = f"{tab_calendar.year}年{tab_calendar.month}月"
        tab_header.update()
        
        #カードの更新
        #既存のカードを削除
        calendar_controls_content = len([control for control in tab_calendar.controls if not isinstance(control, ft.Card)])
        while len(tab_calendar.controls) > calendar_controls_content:
            tab_calendar.controls.pop()

        # 新しいカードを作成・追加
        new_cards = UpdateCard.create_card_for_month(year=tab_calendar.year, month=tab_calendar.month, label=label)
        for index, card in enumerate(new_cards):
            tab_calendar.controls.append(
                ft.Card(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"{tab_calendar.month}月{index + 1}日"),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(label=ft.Text("name"), numeric=True),
                                    ft.DataColumn(label=ft.Text("AM or PM"), numeric=True),
                                ],
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("担当者名")),
                                            ft.DataCell(ft.Text("AM or PM"))
                                        ]
                                    )   # 仮のデータ行
                                ]
                            )
                        ],
                        data={"date": f"{tab_calendar.year}-{tab_calendar.month:01d}-{index + 1:01d}", "locate": label},
                    )
                )
            )
        tab_calendar.update()

        # カードの内容を更新 
        UpdateCard.update_cards_with_schedule_data(
            e=e, schedule_data=schedule_data, page=page, card_name=label,
            card=tab_calendar.controls[calendar_controls_content:]
        )

        #カレンダーセルの色を更新
        UpdateCalendar.update_calendar_with_schedule_data(
            e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls[calendar_controls_content:],
            card_name=label,
        )


    @staticmethod
    def update_card_calendar(e, schedule_data, page, label, tab_calendar):
        """カードとカレンダーの更新
        
        Args:
            e: イベント
            schedule_data: スケジュールデータ
            page: ページオブジェクト
            label (str): 病棟名
            tab_calendar: カレンダーオブジェクト
        """
        # カード以外のコントロール数を取得
        calendar_controls_content = len([control for control in tab_calendar.controls if not isinstance(control, ft.Card)])
        
        #カードの更新
        UpdateCard.update_cards_with_schedule_data(
            e=e, schedule_data=schedule_data, page=page, card_name=label,
            card=tab_calendar.controls[calendar_controls_content:]
        )

        #カレンダーセルの色を更新
        UpdateCalendar.update_calendar_with_schedule_data(
            e=e, schedule_data=schedule_data, page=page, calendar=tab_calendar.controls,
            card_name=label,filter_name=None
        )

    @staticmethod
    def personal_filter(check_names, checkboxes):
        check_names.clear()
        for checkbox in checkboxes.controls:
            if isinstance(checkbox, ft.Checkbox) and checkbox.value:
                check_names.append(checkbox.data)
                print(f"選択された名前: {checkbox.data}")
            return check_names
        
    #個人名絞り込みのページにおいて、update_calendar_with_schedule_dataとpersonal_filterを統合した関数
    @staticmethod
    def update_calendar_with_personal_data(e,  page, checkboxes, tab_calendar):
        #スケジュールデータの更新
        #パラメーターとしてschedule_dataを渡すと最新データに更新されないので、ここでclient_storageに保存されているデータから読み込み直す
        schedule_data = CalendarUpdater.update_schedule_data(page=page, schedule_data=None)
        #チェックボックス選択データの入力
        check_names = CalendarUpdater.personal_filter(check_names=[], checkboxes=checkboxes)
        #
        UpdateCalendar.update_calendar_with_schedule_data(
                e=e,schedule_data=schedule_data,page=page,calendar=tab_calendar,card_name=None,
                filter_name=check_names
            )#label=絞り込んだチェックボックスに入れた名前のリスト　絞り込みの対象リスト
        

    @staticmethod
    def update_schedule_data(page,schedule_data):
        """スケジュールデータを更新し、ページに保存
        
        Args:
            schedule_data: 更新するスケジュールデータ
            page: ページオブジェクト
        """
        schedule_data=page.client_storage.get("schedule_data")
        if schedule_data is None:
            schedule_data = []
        else:
            schedule_data = schedule_data
        return schedule_data