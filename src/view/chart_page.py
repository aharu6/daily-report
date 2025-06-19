import flet as ft
from flet import View
from handlers.handlersMain import Handlers_Main
from handlers.chart.handlers_chart import Handlers_Chart
from components.compoments_chart import FilePickCard
from handlers.chart.analyze_handler import Handlers_analyze
from handlers.chart.select_directory import SelectDirectoryHandler
class ChartPage:
    def __init__(self, page):
        self.page = page

        # データフレームを定義しておく
        # ファイルのアップロードにてデータフレームの作成まで
        self.dataframe = None
        self.all_df=None
        self.locate_df=None
        self.self_df=None
        self.file_picker_Button = ft.TextButton(
            "フォルダを選択",
            on_click=lambda _: self.file_picker.get_directory_path()
        )
        self.select = ft.Row(
            controls=[
                FilePickCard(self.file_picker_Button).create(),
            ],
        )
        #選択したファイル名の表示
        self.selected_file_name=ft.Column()
        #ファイル絞り込み用のハンドラ
        self.file_filer = ft.Tabs(
            selected_index=0,
            animation_duration=500,
            tabs=[],
        )

        self.file_picker = ft.FilePicker(
            on_result=lambda e: SelectDirectoryHandler.get_directory_result(
                e=e,
                page=self.page,
                card=self.selected_file_name, 
                parent_instance=self,
                selected_files = self.selected_files,
                file_filer_content=self.file_filer,
                ),
        )
        self.selected_files = ft.Text()
        self.page.overlay.append(self.file_picker)
        
        #各タスク（task列）の合計時間を計算。
        self.subtitle = ft.Text("全体", size = 20)
        self.horizon_subtitle = ft.Divider()
        self.chart1_field = ft.ResponsiveRow()

        self.chart1card = ft.Card(
            content=ft.TextButton(
                text="グラフを生成",
                on_click=lambda _: Handlers_Chart.ComponentChart_for_standard(
                    dataframe=self.dataframe,chart_field= self.chart1_field,page= page,
                    parent_instance_standard=self,
                ),
            )
        )

        self.subtitle2 = ft.Text("病棟ごとの集計",size = 20)
        self.chart2_field_info= ft.ResponsiveRow()
        self.chart2_field = ft.ResponsiveRow(controls=[])
        self.chart2card = ft.Card(
            content=ft.TextButton(
                "グラフを生成",
                on_click=lambda _: Handlers_Chart.ComponentChart_for_location(
                    dataframe=self.dataframe, chart_field=self.chart2_field, page=page,
                    chart2_info=self.chart2_field_info,
                    parent_instance_locate=self,
                ),
            )
        )

        self.subtitle3 = ft.Text("個人ごとの集計",size = 20)
        self.chart3_field = ft.ResponsiveRow()
        # あとでファイルを選択していない状態でボタンを押したときにはエラーメッセージを表示するようにする
        self.chart3card = ft.Card(
            content=ft.TextButton(
                "グラフを生成",
                on_click=lambda _: Handlers_Chart.ComponentChart_for_self(
                    dataframe=self.dataframe, chart_field=self.chart3_field,page=page,
                    parent_instance_self_df=self,
                ),
            )
        )

        #総時間数、件数あたりの時間　件数あたりに要した時間の算出
        self.subtitle4=ft.Text("総時間と件数あたりの時間",size=15)
        self.chart4_field=ft.ResponsiveRow()
        self.chart4card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.count_par_time(
                    dataframe=self.dataframe, result_field=self.chart4_field, page=self.page,
                    all_df=self.all_df
                )
            )
        )

        #業務内容ごとの件数
        self.subtitle5=ft.Text("業務内容ごとの件数",size=15)
        self.chart5_field=ft.ResponsiveRow()
        self.chart5card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.task_par_count(
                    dataframe=self.dataframe, result_field=self.chart5_field, page=self.page,
                    all_df=self.all_df
                )
            )
        )

        #各タスクがどの場所（locate列）で行われたかを集計。
        self.subtitle6=ft.Text("業務内容ごとの場所",size=15)
        self.chart6_field=ft.ResponsiveRow()
        self.chart6card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.task_par_location(
                    dataframe=self.dataframe, result_field=self.chart6_field, page=self.page,
                    all_df=self.all_df,
                )
            )
        )

        #各タスクがどの時間帯に集中しているかを分析。　ヒートマップ
        self.subtitle7=ft.Text("時間帯ごとに業務が記録された回数",size=15)
        self.chart7_field=ft.ResponsiveRow()
        self.chart7card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.time_task_analysis(
                    dataframe=self.dataframe, result_field=self.chart7_field, page=self.page,
                    all_df=self.all_df,
                )
            )
        )
        #その他コメントの表示
        self.subtitle8=ft.Text("その他コメント",size=15)
        self.chart8_field=ft.ResponsiveRow()
        self.chart8card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.comment_analysis(
                    dataframe=self.dataframe, result_field=self.chart8_field, page=self.page,
                    all_df=self.all_df,
                )
            )
        )
        #date列を基に、日付ごとのタスクの分布を分析
        self.subtitle9=ft.Text("日付ごとの業務分布",size=15)
        self.chart9_field=ft.ResponsiveRow()
        self.chart9card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.date_task_analysis(
                    dataframe=self.dataframe, result_field=self.chart9_field, page=self.page,
                    all_df=self.all_df,
                )
            )
        )

        #個人ごと
        #個人ごとの総時間数,1業務あたりの平均時間数,件数あたりの時間数、
        self.subtitle10_0=ft.Text("個人ごとの総時間数",size=15)
        self.chart10_0_field=ft.ResponsiveRow()
        self.chart10_0card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.self_analysis_total_time(
                    dataframe=self.dataframe, result_field=self.chart10_0_field, page=self.page,self_df=self.self_df
                )
            )
        )
        #個人ごとに業務にかかった総時間数と１件あたりどれくらい時間がかかっているのか
        self.subtitle10=ft.Text("個人ごとの時間数・件数・１件あたりの時間・平均値",size=15)
        self.chart10_field=ft.ResponsiveRow()
        self.chart10card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.self_analysis(
                    dataframe=self.dataframe, result_field=self.chart10_field, page=self.page,
                    self_df=self.self_df,
                )
            )
        )

        ##病棟ごと
        #locateごとの総時間数、記録回数、件数、平均値の算出
        self.subtitle11=ft.Text("病棟ごとの時間数・件数・１件あたりの時間・平均値",size=15)
        self.chart11_field=ft.ResponsiveRow()
        self.chart11card=ft.Card(
            content=ft.TextButton(
                "集計",
                on_click=lambda _:Handlers_analyze.locate_analysis(
                    dataframe=self.dataframe, result_field=self.chart11_field, page=self.page,
                    locate_df=self.locate_df,
                )
            )
        )
        #comment列が記載されている行と空白の行を比較


        #特定のタスクに絞って、時間帯やcountの分布を分析。
        
        
    
    def create(self):
        return View(
            "/chart",
            [
                self.select,
                self.selected_file_name,
                self.selected_files,
                self.file_filer,
                self.subtitle,
                self.horizon_subtitle,
                self.chart1card,#全体
                self.chart1_field,
                
                self.subtitle4,
                self.chart4card,
                self.chart4_field,
                self.subtitle5,
                self.chart5card,
                self.chart5_field,
                self.subtitle6,
                self.chart6card,
                self.chart6_field,
                self.subtitle7,
                self.chart7card,
                self.chart7_field,
                self.subtitle8,
                self.chart8card,
                self.chart8_field,
                self.subtitle9,
                self.chart9card,
                self.chart9_field,
                self.subtitle2,
                self.horizon_subtitle,
                self.chart2card,#病棟ごと
                self.chart2_field_info,
                self.chart2_field,
                self.subtitle11,
                self.chart11card,
                self.chart11_field,

                self.subtitle3,
                self.horizon_subtitle,
                self.chart3card,# 個人ごと
                self.chart3_field,
                self.subtitle10_0,
                self.chart10_0card,
                self.chart10_0_field,
                self.subtitle10,
                self.chart10card,
                self.chart10_field,
                # chartPage,
                ft.CupertinoNavigationBar(
                    selected_index=1,
                    bgcolor=ft.colors.BLUE_GREY_50,
                    inactive_color=ft.colors.GREY,
                    active_color=ft.colors.BLACK,
                    on_change=lambda e: Handlers_Main().on_navigation_change(
                        e, self.page
                    ),
                    destinations=[
                        ft.NavigationBarDestination(
                            icon=ft.icons.CREATE,
                            label="Create",
                            selected_icon=ft.icons.BORDER_COLOR,
                        ),
                        ft.NavigationBarDestination(
                            icon=ft.icons.SHOW_CHART,
                            label="Showchart",
                            selected_icon=ft.icons.AUTO_GRAPH,
                        ),
                        ft.NavigationBarDestination(
                            icon=ft.icons.SETTINGS,
                            selected_icon=ft.icons.SETTINGS_SUGGEST,
                            label="Settings",
                        ),
                    ],
                ),
            ],
            scroll=True,
        )
