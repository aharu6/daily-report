import pandas as pd
import flet as ft
import plotly.express as px
from flet.plotly_chart import PlotlyChart
from handlers.chart.download_handler import Chart_Download_Handler
from handlers.chart.period_handler import PeriodHandler
import datetime
import chardet
from handlers.chart.preview_chart import PreviewChartHandler
pd.set_option('display.max_columns', None) 
pd.set_option('display.max_rows', None)

# 定数定義
MINUTES_PER_RECORD = 15  # 1レコードあたりの分数
CHART_WIDTH_MULTIPLIER = 33  # グラフ幅の計算係数
CHART_HEIGHT_MULTIPLIER = 33  # グラフ高さの計算係数
MIN_CHART_SIZE = 1400  # 最小チャートサイズ

# 色マッピング定義
TASK_COLOR_MAP = {
    '薬剤使用状況の把握等（情報収集）':'#239DDA',#青
    '服薬指導+記録作成':'#2980AF',
    '無菌調整関連業務':'#1D50A2',
    '薬剤セット・確認':'#007D8E',
    '持参薬を確認':'#0068B7',
    '薬剤服用歴等について保険薬局へ紹介':'#008DB7',
    '処方代理修正':'#00A0E9',
    'TDM実施':'#3A8DAA',
    'カンファレンス':'#26499D',
    '医師からの相談':'#BCE2E8',#水色
    '看護師からの相談':'#A0D8EF',
    'その他の職種からの相談':'#007C45',#緑
    '委員会':'#4F8A5D',
    '勉強会参加':'#005842',
    'WG活動':'#67BE8D',
    '1on1':'#009854',
    'ICT/AST':'#A2D7DD',#水色
    '褥瘡':'#89C3EB',
    'TPN評価':'#64BCC7',
    '手術後使用薬剤確認':'#C8D921',#黄緑
    '手術使用薬剤準備':'#C4C46A',
    '周術期薬剤管理関連':'#AFD147',
    '麻酔科周術期外来':'#D7CF3A',
    '手術使用麻薬確認・補充':'#9D973B',
    '術後疼痛管理チーム回診':'#C5DE93',
    '脳卒中ホットライン対応':'#9DC04C',
    '業務調整':'#68B7A1',#青緑
    '休憩': '#7EBEAB',
    'その他':'#005243',
    '管理業務':'#7FABA9',
    'NST':'#259F94',
    '問い合わせ応需':'#FFD900',#黄色
    'マスター作成・変更':'#FCC800',
    '薬剤情報評価':'#F5E56B',
    '後発品選定':'#D2B74E',
    '会議資料作成':'#F8B500',
    '配信資料作成':'#FFF33F',
    'フォーミュラリー作成':'#FFF2B8',
    '外来処方箋修正':'#FFDC00',
    '勉強会資料作成・開催':'#FFF262',
    'お役立ち情報作成':'#BF7834',#茶色
    '薬剤使用期限確認':'#814336',
    '抗菌薬相談対応':'#762E05',
    '事前準備':'#507687',
    'カンファ・ラウンド':'#507687',
    '記録作成':'#507687',
}

# Chartページ用のハンドラ
class Handlers_Chart:
    @staticmethod
    def _calculate_chart_size(unique_items_count, multiplier=CHART_WIDTH_MULTIPLIER, min_size=MIN_CHART_SIZE):
        """チャートサイズを計算するヘルパーメソッド"""
        size = int(unique_items_count) * multiplier
        return size if size >= min_size else min_size
    
    @staticmethod
    def _create_period_selector_ui(start_date=None, end_date=None, page=None):
        """期間選択UIを作成するヘルパーメソッド"""
        start_text = start_date.strftime("%Y-%m-%d") if start_date else "開始日"
        end_text = end_date.strftime("%Y-%m-%d") if end_date else "終了日"
        
        return [
            ft.ListTile(
                title=ft.Text("表示期間"),
                leading=ft.Icon(ft.icons.DATE_RANGE),
                subtitle=ft.Text("選択後は、再度生成ボタンを押してください"),
            ),
            ft.Row(
                controls=[
                    ft.FilledButton(
                        text=start_text,
                        on_click=lambda e: page.open(
                            ft.DatePicker(
                                on_change=lambda dp_event: PeriodHandler.select_period(e, dp_event),
                            )
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.TRANSPARENT,
                            color=ft.colors.BLUE_900,
                        )
                    ),
                    ft.Text("~", size=20),
                    ft.FilledButton(
                        text=end_text,
                        on_click=lambda e: page.open(
                            ft.DatePicker(
                                on_change=lambda dp_event: PeriodHandler.select_period(e, dp_event),
                            )
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.TRANSPARENT,
                            color=ft.colors.BLUE_900,
                        )
                    )
                ],
                spacing=0,
            )
        ]
    
    @staticmethod
    def _create_download_button(page, chart, chart_name):
        """ダウンロードボタンを作成するヘルパーメソッド"""
        return ft.ElevatedButton(
            "保存",
            icon=ft.icons.DOWNLOAD,
            tooltip=ft.Tooltip("グラフを保存"),
            on_click=lambda _: Chart_Download_Handler.open_directory(
                page=page, 
                barchart=chart, 
                chart_name=chart_name
            ),
        )
    
    @staticmethod
    def _create_preview_button(chart,page):
        """プレビューボタンを作成するヘルパーメソッド"""
        return ft.IconButton(
            icon=ft.icons.PAGEVIEW,
            tooltip="拡大表示",
            on_click=lambda e: PreviewChartHandler.preview_chart(chart,page)
        )
    
    @staticmethod
    def _process_time_data(dataframe):
        """時間データを処理するヘルパーメソッド"""
        group_bubble = dataframe.groupby(["locate","task","count"]).size().reset_index(name="times")
        try:
            group_bubble.drop(index=group_bubble[group_bubble["locate"] == "self"].index, inplace=True)  # self列は除外する
        except KeyError:
            pass
        group_bubble2 = group_bubble.groupby(["locate","task"]).sum(numeric_only=True).reset_index()
        try:
            group_bubble2.drop(index=group_bubble2[group_bubble2["locate"] == "self"].index, inplace=True)  # self列は除外する
        except KeyError:
            pass
        group_bubble2["times"] = group_bubble2["times"] * MINUTES_PER_RECORD
        return group_bubble2
        
    @staticmethod
    def _create_bar_chart(data, width=None):
        """棒グラフを作成するヘルパーメソッド"""
        chart_width = width or Handlers_Chart._calculate_chart_size(len(data["task"].unique()))
        bar_chart = px.bar(data, x="task", y="times", width=chart_width)
        bar_chart.update_layout(
            yaxis=dict(title="かかった時間"),
            xaxis=dict(title="業務内容")
        )
        return bar_chart

    @staticmethod
    def _create_pie_chart(data, location_name):
        normal_radius=80
        hover_radius=120

        normal_text_style=ft.TextStyle(
            size=12,
            color=ft.colors.GREY_100,
            weight=ft.FontWeight.BOLD,
        )
        hover_text_style=ft.TextStyle(
            size=30,
            color=ft.colors.BLACK,
            weight=ft.FontWeight.BOLD,
        )

        def on_chart_event(e):
            for idx,section in enumerate(e.control.sections):
                if idx == e.section_index:
                    print("if")
                    section.radius = hover_radius
                    section.title_style = hover_text_style
                else:
                    print("else")
                    section.radius = normal_radius
                    section.title_style = normal_text_style
            e.control.update()

        """円グラフを作成するヘルパーメソッド"""
        chart_sections=[]    
        locate_data=data[data["locate"]==location_name]

        #割合を出すためのlocateごとの合計値
        total_counts=locate_data["counts"].sum()

        for _,row in locate_data.iterrows():
            task_name=row["task"]
            print(task_name)
            value=row["counts"]
            color=TASK_COLOR_MAP.get(task_name, "#CCCCCC")  # デフォルト

            print(value/total_counts*100)
            chart_sections.append(
                ft.PieChartSection(
                    value=float(value/total_counts) if total_counts > 0 else 0,
                    title=f"{task_name}\n{(value/total_counts*100):.1f}%" if total_counts > 0 else f"{task_name}\n0.0%",
                    color=color,
                    radius=normal_radius,
                )
            )
        
        return ft.PieChart(
            sections=chart_sections,
            width=400,
            height=400,
            sections_space=2,
            on_chart_event=on_chart_event,
        )
        
    @staticmethod
    def _create_plotly_piechart(data,location_data):
        """Plotlyの円グラフを作成するヘルパーメソッド"""
        locate_data=data[data["locate"]==location_data]

        #割合を出すためのlocateごとの合計値
        total_counts=locate_data["counts"].sum()

        labels = []
        values = []
        for _,row in locate_data.iterrows():
            task_name=row["task"]
            value=row["counts"]
            labels.append(task_name)
            values.append(float(value/total_counts) if total_counts > 0 else 0)

        fig = px.pie(
            names=labels,
            values=values,
            title=f"{location_data}の業務割合",
            height=1500
        )
        return fig
    @staticmethod
    def detect_encoding(file_path):
        """ファイルエンコーディングを安全に検出"""
        try:
            if not file_path or not isinstance(file_path, str):
                raise ValueError("無効なファイルパス")
                
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
                
            if result and result.get('encoding'):
                return result['encoding']
            else:
                print("エンコーディング検出に失敗、UTF-8を使用")
                return 'utf-8'
                
        except FileNotFoundError:
            print(f"ファイルが見つかりません: {file_path}")
            return 'utf-8'
        except Exception as e:
            print(f"エンコーディング検出エラー: {e}")
            return 'utf-8'

    @staticmethod
    def pick_file_name(file_name, card):
        """ファイル名を安全に表示"""
        try:
            if not file_name:
                file_name = []
            elif not isinstance(file_name, list):
                file_name = [str(file_name)]
                
            print(f"ファイル一覧: {file_name}")
            
            card_list = [
                ft.ExpansionPanelList(
                    controls=[
                        ft.ExpansionPanel(
                            bgcolor=None,
                            header=ft.ListTile(
                                leading=ft.Icon(ft.icons.LIST),
                                title=ft.Text("読み込んだファイル一覧"),
                            ),
                            content=ft.Column(
                                controls=[
                                    ft.ListTile(
                                        title=ft.Text(str(file_name[i]) if i < len(file_name) else "Unknown")
                                    )
                                    for i in range(max(len(file_name), 1))
                                ]
                            )
                        )
                    ]
                ),
            ]
            
            if hasattr(card, 'controls'):
                card.controls = card_list
                if hasattr(card, 'update'):
                    card.update()
            else:
                print("カードオブジェクトが無効です")
                
        except Exception as e:
            print(f"ファイル名表示エラー: {e}")
            # フォールバック表示
            try:
                card.controls = [
                    ft.Card(
                        content=ft.Text("ファイル一覧の表示に失敗しました", color=ft.colors.RED)
                    )
                ]
                card.update()
            except Exception:
                pass  # 完全に失敗した場合は何もしない

    @staticmethod
    def show_progress_bar(chart_field, page):
        """プログレスバーを安全に表示"""
        try:
            if not hasattr(chart_field, 'controls') or not hasattr(page, 'update'):
                print("無効なオブジェクトが渡されました")
                return
                
            chart_field.controls = [
                ft.Card(
                    content=ft.Column([
                        ft.Text("Loading..."),
                        ft.ProgressBar(width=200, height=20),
                    ]),
                )
            ]
            page.update()
            print("Loading...")
            
        except Exception as e:
            print(f"プログレスバー表示エラー: {e}")
            # フォールバック処理
            try:
                chart_field.controls = [ft.Text("読み込み中...")]
                page.update()
            except Exception:
                pass  # 完全に失敗した場合は何もしない

    @staticmethod
    def ComponentChart_for_standard(dataframe, chart_field, page, parent_instance_standard):
        """標準チャートを生成するメソッド"""
        try:
            # 期間情報の安全な取得
            start_date, end_date = Handlers_Chart._safe_parse_period_from_controls(chart_field)
            
            # プログレスバー表示
            Handlers_Chart.show_progress_bar(chart_field, page)
            
            # データフレームの安全な処理
            df = Handlers_Chart._safe_process_dataframe(dataframe, start_date, end_date)
            
            # 親インスタンスにデータを保存
            if hasattr(parent_instance_standard, 'all_df'):
                parent_instance_standard.all_df = df
            
            # UIボタンのテキスト更新
            if start_date and end_date:
                try:
                    chart_field.controls[1].controls[0].text = start_date.strftime("%Y-%m-%d")
                    chart_field.controls[1].controls[2].text = end_date.strftime("%Y-%m-%d")
                except (IndexError, AttributeError):
                    pass  # UI更新エラーは無視
            
            # データ処理とチャート作成
            group_bubble2 = Handlers_Chart._process_time_data(df)
            bar_chart = Handlers_Chart._create_bar_chart(group_bubble2)
            
            # UI作成
            period_ui = Handlers_Chart._create_period_selector_ui(start_date, end_date, page)
            expansion_button = Handlers_Chart._create_preview_button(chart=bar_chart,page=page)
            download_button = Handlers_Chart._create_download_button(page=page, chart=bar_chart, chart_name="barchart")

            chart_field.controls = [
                *period_ui,
                ft.Card(content=PlotlyChart(bar_chart, expand=True, original_size=False, isolated=True)),
                ft.ResponsiveRow(controls=[expansion_button, download_button])
            ]
            chart_field.update()

        except ValueError as e:
            print(f"データエラー: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, f"データエラー: {str(e)}")
            
        except pd.errors.EmptyDataError:
            print("空のデータフレームエラー")
            Handlers_Chart._handle_chart_error(chart_field, page, "データが空です")
            
        except KeyError as e:
            print(f"必要な列が見つかりません: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, f"データ列エラー: {str(e)}")
            
        except Exception as e:
            print(f"予期しないエラー: {e}")
            # フォールバック処理
            try:
                df = dataframe.copy() if dataframe is not None else pd.DataFrame()
                if not df.empty:
                    group_bubble2 = Handlers_Chart._process_time_data(df)
                    bar_chart = Handlers_Chart._create_bar_chart(group_bubble2)
                    
                    period_ui = Handlers_Chart._create_period_selector_ui(page=page)
                    expansion_button = Handlers_Chart._create_preview_button(chart=bar_chart,page=page)
                    download_button = Handlers_Chart._create_download_button(page, bar_chart, "barchart")
                    
                    chart_field.controls = [
                        *period_ui,
                        ft.ListTile(),  # 期間表示プレースホルダー
                        ft.Card(content=PlotlyChart(bar_chart, expand=True, original_size=False, isolated=True)),
                        ft.ResponsiveRow(controls=[expansion_button, download_button])
                    ]
                    page.update()
                else:
                    Handlers_Chart._handle_chart_error(chart_field, page, "データの読み込みに失敗しました")
            except Exception as fallback_error:
                print(f"フォールバック処理も失敗: {fallback_error}")
                Handlers_Chart._handle_chart_error(chart_field, page, "チャート生成に失敗しました")
        

        
    @staticmethod
    def ComponentChart_for_location(dataframe, chart_field, page, chart2_info, parent_instance_locate):
        """場所別チャートを生成するメソッド（エラーハンドリング改善版）"""
        try:
            # プログレスバー表示
            Handlers_Chart.show_progress_bar(chart_field, page)
            
            # 期間情報の安全な取得
            start_date, end_date = Handlers_Chart._safe_parse_period_from_controls(chart2_info)
            
            # データフレームの安全な処理
            df = Handlers_Chart._safe_process_dataframe(dataframe, start_date, end_date)
            
            # 親インスタンスにデータを保存
            if hasattr(parent_instance_locate, 'locate_df'):
                parent_instance_locate.locate_df = df

            # UIボタンのテキスト更新
            if start_date and end_date:
                try:
                    chart2_info.controls[1].controls[0].text = start_date.strftime("%Y-%m-%d")
                    chart2_info.controls[1].controls[2].text = end_date.strftime("%Y-%m-%d")
                except (IndexError, AttributeError):
                    pass  # UI更新エラーは無視

            # 必要な列の存在確認
            required_columns = ['locate', 'task']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"必要な列が見つかりません: {missing_columns}")

            # データのグループ化
            group_df_locate = df.groupby(["locate", "task"]).size().reset_index(name="counts")
            try:
                group_df_locate.drop(index=group_df_locate[group_df_locate["locate"] == "self"].index, inplace=True)  # self列は除外する
            except KeyError:
                pass
            
            if group_df_locate.empty:
                raise ValueError("グループ化後のデータが空です")

            # 期間選択UI作成
            chart2_info.controls = Handlers_Chart._create_period_selector_ui(start_date, end_date, page)
            
            # 各場所のチャート作成
            locate_chart_list = []
            unique_locations = group_df_locate["locate"].unique()
            
            if len(unique_locations) == 0:
                raise ValueError("場所データが見つかりません")

            for locate in unique_locations:
                try:
                    fig = Handlers_Chart._create_pie_chart(group_df_locate, locate)
                    fig_for_download = Handlers_Chart._create_plotly_piechart(group_df_locate,locate)
                    locate_chart_list.extend([
                        ft.Card(
                            content=ft.Column(
                                controls=[
                                    fig,
                                    ft.Text(locate),
                                    Handlers_Chart._create_download_button(page, fig_for_download, "piechart"),
                                    Handlers_Chart._create_preview_button(chart=fig,page=page)
                                ],
                                width="30%",
                            ),
                            col={"sm": 10, "md": 6, "xl": 4},
                        ),
                    ])
                except Exception as chart_error:
                    print(f"場所 '{locate}' のチャート作成エラー: {chart_error}")
                    # 個別のチャートエラーは継続処理
                    continue

            if not locate_chart_list:
                raise ValueError("チャートを作成できませんでした")

            chart_field.controls = locate_chart_list
            page.update()

        except ValueError as e:
            print(f"データエラー: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, f"データエラー: {str(e)}")
            
        except KeyError as e:
            print(f"必要な列が見つかりません: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, f"データ列エラー: {str(e)}")
            
        except Exception as e:
            print(f"予期しないエラー: {e}")
            # フォールバック処理
            try:
                df = dataframe.copy() if dataframe is not None else pd.DataFrame()
                if not df.empty and 'locate' in df.columns and 'task' in df.columns:
                    group_df_locate = df.groupby(["locate", "task"]).size().reset_index(name="counts")
                    try:
                        group_df_locate.drop(index=group_df_locate[group_df_locate["locate"] == "self"].index, inplace=True)  # self列は除外する
                    except KeyError:
                        pass
                    chart2_info.controls = Handlers_Chart._create_period_selector_ui(page=page)
                    
                    locate_chart_list = []
                    for locate in group_df_locate["locate"].unique():
                        try:
                            fig = Handlers_Chart._create_pie_chart(group_df_locate, locate)
                            fig_for_download = Handlers_Chart._create_plotly_piechart(group_df_locate,locate)
                            locate_chart_list.append(
                                ft.Card(
                                    content=ft.Column(
                                        controls=[
                                            fig,
                                            ft.Text(locate),
                                            #ダウンロード用にはplotlyの図を渡す
                                            Handlers_Chart._create_download_button(page, fig_for_download, f"piechart_{locate}"),
                                            Handlers_Chart._create_preview_button(chart=fig,page=page)
                                        ],
                                        width="30%",
                                    ),
                                    col={"sm": 10, "md": 6, "xl": 4},
                                )
                            )
                        except Exception:
                            continue  # 個別チャートエラーをスキップ
                    
                    chart_field.controls = locate_chart_list
                    page.update()
                else:
                    Handlers_Chart._handle_chart_error(chart_field, page, "データの読み込みに失敗しました")
            except Exception as fallback_error:
                print(f"フォールバック処理も失敗: {fallback_error}")
                Handlers_Chart._handle_chart_error(chart_field, page, "チャート生成に失敗しました")

    @staticmethod
    def ComponentChart_for_self(dataframe, chart_field, page, parent_instance_self_df):
        """個人別チャートを生成するメソッド（エラーハンドリング改善版）"""        
        try:
            # 期間情報の安全な取得
            start_date, end_date = Handlers_Chart._safe_parse_period_from_controls(chart_field)
            
            # プログレスバー表示
            Handlers_Chart.show_progress_bar(chart_field, page)
            
            # データフレームの安全な処理
            df = Handlers_Chart._safe_process_dataframe(dataframe, start_date, end_date)
            
            # 親インスタンスにデータを保存
            if hasattr(parent_instance_self_df, 'self_df'):
                parent_instance_self_df.self_df = df

            # UIボタンのテキスト更新
            if start_date and end_date:
                try:
                    chart_field.controls[1].controls[0].text = start_date.strftime("%Y-%m-%d")
                    chart_field.controls[1].controls[2].text = end_date.strftime("%Y-%m-%d")
                except (IndexError, AttributeError):
                    pass  # UI更新エラーは無視

            # 必要な列の存在確認
            required_columns = ['phName', 'task']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"必要な列が見つかりません: {missing_columns}")

            # データのグループ化と処理
            group_by_person = df.groupby(["phName", "task"]).size().reset_index(name="time")
            
            if group_by_person.empty:
                raise ValueError("個人データが見つかりません")

            # 合計時間と割合の計算
            group_by_person["total_time"] = group_by_person.groupby("phName")["time"].transform("sum")
            # ゼロ除算エラーを防ぐ
            mask = group_by_person["total_time"] != 0
            group_by_person.loc[mask, "percentage"] = (
                group_by_person.loc[mask, "time"] / group_by_person.loc[mask, "total_time"]
            ) * 100
            group_by_person.loc[~mask, "percentage"] = 0

            # チャートサイズ計算
            unique_names = group_by_person["phName"].unique()
            if len(unique_names) == 0:
                raise ValueError("薬剤師名が見つかりません")

            graph_height = Handlers_Chart._calculate_chart_size(
                len(unique_names), CHART_HEIGHT_MULTIPLIER
            )
            
            # チャート作成
            fig_bar = px.bar(
                group_by_person, 
                height=graph_height,
                x="percentage", 
                y="phName", 
                color="task", 
                barmode="stack", 
                orientation="h",
                color_discrete_map=TASK_COLOR_MAP,
            )
            fig_bar.update_layout(
                        height=graph_height,
                        xaxis=dict(title="業務割合(%)"),
                        yaxis=dict(title="薬剤師名"),
                        legend=dict(font=dict(size=10))
                    )
            
            # UI作成
            period_ui = Handlers_Chart._create_period_selector_ui(start_date, end_date, page)
            expansion_button = Handlers_Chart._create_preview_button(chart=fig_bar,page=page)
            download_button = Handlers_Chart._create_download_button(page, fig_bar, "selfchart")
            
            chart_field.controls = [
                *period_ui,
                ft.Card(content=PlotlyChart(fig_bar, expand=True, original_size=False, isolated=True)),
                ft.ResponsiveRow(controls=[expansion_button, download_button])
            ]
            page.update()

        except ValueError as e:
            print(f"データエラー: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, f"データエラー: {str(e)}")
            
        except KeyError as e:
            print(f"必要な列が見つかりません: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, f"データ列エラー: {str(e)}")
            
        except ZeroDivisionError as e:
            print(f"計算エラー: {e}")
            Handlers_Chart._handle_chart_error(chart_field, page, "計算エラーが発生しました")
            
        except Exception as e:
            print(f"予期しないエラー: {e}")
            # フォールバック処理
            try:
                df = dataframe.copy() if dataframe is not None else pd.DataFrame()
                if not df.empty and 'phName' in df.columns and 'task' in df.columns:
                    # 個人ごとにデータをまとめ直す
                    group_by_person = df.groupby(["phName", "task"]).size().reset_index(name="time")
                    
                    # 合計時間の計算
                    group_by_person["total_time"] = group_by_person.groupby("phName")["time"].transform("sum")
                    graph_height = Handlers_Chart._calculate_chart_size(
                        len(group_by_person["phName"].unique()), CHART_HEIGHT_MULTIPLIER
                    )
                    
                    # 割合の計算（ゼロ除算対策）
                    mask = group_by_person["total_time"] != 0
                    group_by_person.loc[mask, "percentage"] = (
                        group_by_person.loc[mask, "time"] / group_by_person.loc[mask, "total_time"]
                    ) * 100
                    group_by_person.loc[~mask, "percentage"] = 0
                    
                    # チャート作成
                    fig_bar = px.bar(
                        group_by_person, 
                        x="percentage", 
                        y="phName", 
                        color="task", 
                        barmode="stack", 
                        orientation="h"
                    )
                    fig_bar.update_layout(
                        height=graph_height,
                        xaxis=dict(title="業務割合(%)"),
                        yaxis=dict(title="薬剤師名"),
                        legend=dict(font=dict(size=10))
                    )
                    
                    # UI作成
                    period_ui = Handlers_Chart._create_period_selector_ui(page=page)
                    expansion_button = Handlers_Chart._create_preview_button(chart=fig_bar,page=page)
                    download_button = Handlers_Chart._create_download_button(page, fig_bar, "selfchart")
                    
                    chart_field.controls = [
                        *period_ui,
                        ft.Card(content=PlotlyChart(fig_bar, expand=True, original_size=False, isolated=True)),
                        ft.ResponsiveRow(controls=[expansion_button, download_button])
                    ]
                    page.update()
                else:
                    Handlers_Chart._handle_chart_error(chart_field, page, "データの読み込みに失敗しました")
            except Exception as fallback_error:
                print(f"フォールバック処理も失敗: {fallback_error}")
                Handlers_Chart._handle_chart_error(chart_field, page, "チャート生成に失敗しました")
    
    @staticmethod
    def _safe_parse_date(date_string, fallback=None):
        """安全な日付パースヘルパーメソッド"""
        if not date_string:
            return fallback
        
        try:
            return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
        except (ValueError, TypeError, AttributeError):
            try:
                # 別の形式も試行
                return datetime.datetime.strptime(date_string, "%Y-%m-%d")
            except (ValueError, TypeError, AttributeError):
                return fallback

    @staticmethod
    def _safe_parse_period_from_controls(chart_field):
        """コントロールから期間情報を安全に取得するヘルパーメソッド"""
        try:
            if (len(chart_field.controls) < 2 or 
                len(chart_field.controls[1].controls) < 3):
                return None, None
                
            start_data = getattr(chart_field.controls[1].controls[0], 'data', None)
            end_data = getattr(chart_field.controls[1].controls[2], 'data', None)
            
            start_date = Handlers_Chart._safe_parse_date(start_data)
            end_date = Handlers_Chart._safe_parse_date(end_data)
            
            return start_date, end_date
        except (IndexError, AttributeError) as e:
            print(f"期間解析エラー: {e}")
            return None, None

    @staticmethod
    def _safe_process_dataframe(dataframe, start_date=None, end_date=None):
        """データフレームを安全に処理するヘルパーメソッド"""
        try:
            if dataframe is None or dataframe.empty:
                raise ValueError("データフレームが空です")
            
            df = dataframe.copy()
            
            # 日付列の存在確認
            if 'date' not in df.columns:
                raise ValueError("日付列が見つかりません")
            
            df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors='coerce')
            
            # 無効な日付をチェック
            if df["date"].isnull().any():
                print("警告: 無効な日付データが含まれています")
                df = df.dropna(subset=['date'])
            
            # 日付フィルタリング
            if start_date and end_date:
                df = df[df["date"].between(start_date, end_date)]
                
            if df.empty:
                raise ValueError("フィルタリング後にデータが空になりました")
                
            return df
            
        except Exception as e:
            print(f"データ処理エラー: {e}")
            raise

    @staticmethod
    def _handle_chart_error(chart_field, page, error_message="エラーが発生しました"):
        """チャートエラーを処理するヘルパーメソッド"""
        chart_field.controls = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                    ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=50),
                    ft.Text(error_message, color=ft.colors.RED),
                    ft.Text("データを確認してください", size=12),
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.colors.RED_50
                )
                )
        ]
        page.update()