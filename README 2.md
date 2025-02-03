# dairy-report

## 概要説明・機能

#### timeline_page

日誌としての入力・編集、書き出し

#### chart_page

timeline_pageにて書き出したcsvファイルを使用して、グラフの書き出し

#### setting_page

本体保存データの削除

起動時にデフォルトで追加する業務のon/off切り替え機能

## 使用環境

exeファイルに書き出し　→ windows10以上

## 使い方

pyinstaller にてexeファイルに書き出して使用

## インストール方法

## 開発環境

Python 3.11.11

パッケージ　→ requirements.txt

フレームワーク　flet 0.24.1

## ファイル構成

``` {.python .R}
""""
.
├── README.md
├── TextFile1.txt
├── TextFile2.txt
├── appicon
│   ├── diary-left-svgrepo-com.png
│   └── diary-left-svgrepo-com.svg
├── assets
│   └── icon.png
├── components
│   ├── __pycache__
│   │   ├── compoments_chart.cpython-313.pyc
│   │   ├── components.cpython-311.pyc
│   │   ├── components.cpython-313.pyc
│   │   ├── components_setting.cpython-311.pyc
│   │   └── components_setting.cpython-313.pyc
│   ├── compoments_chart.py
│   ├── components.py
│   └── components_setting.py
├── handlers
│   ├── __pycache__
│   │   ├── drag_move.cpython-311.pyc
│   │   ├── drag_move.cpython-313.pyc
│   │   ├── handlers.cpython-311.pyc
│   │   ├── handlers.cpython-313.pyc
│   │   ├── handlersMain.cpython-311.pyc
│   │   ├── handlersMain.cpython-313.pyc
│   │   ├── handlers_chart.cpython-311.pyc
│   │   ├── handlers_chart.cpython-313.pyc
│   │   ├── handlers_setting.cpython-311.pyc
│   │   ├── handlers_setting.cpython-313.pyc
│   │   ├── pageScroll.cpython-311.pyc
│   │   ├── pageScroll.cpython-313.pyc
│   │   ├── reload_data.cpython-311.pyc
│   │   └── reload_data.cpython-313.pyc
│   ├── drag_move.py
│   ├── handlers.py
│   ├── handlersMain.py
│   ├── handlers_chart.py
│   ├── handlers_setting.py
│   ├── pageScroll.py
│   └── reload_data.py
├── main.py
├── models
│   ├── __pycache__
│   │   ├── models.cpython-311.pyc
│   │   └── models.cpython-313.pyc
│   └── models.py
├── output_csv
│   ├── 2024-11-22.csv
│   ├── 2024-11-23.csv
│   ├── 2024-11-24.csv
│   ├── 2024-11-26.csv
│   ├── 2024-11-27.csv
│   ├── 2024-11-28.csv
│   ├── 2024-11-29.csv
│   ├── 2024-11-30.csv
│   ├── 2024-12-05.csv
│   ├── 2024-12-09.csv
│   ├── 2024-12-14.csv
│   ├── 2024-12-15.csv
│   ├── 2024-12-18.csv
│   ├── 2024-12-23.csv
│   ├── 2024-12-24.csv
│   ├── 2024-12-25.csv
│   ├── 2025-01-05.csv
│   └── 2025-01-13.csv
├── requirements.txt
├── testfile
│   ├── chart.py
│   ├── chartplotly.py
│   ├── cupertino.py
│   ├── drawer_memo.py
│   ├── drawertest.py
│   ├── layout.py
│   └── requirements.txt
├── timelime.db-journal
└── view
    ├── __pycache__
    │   ├── chart_page.cpython-311.pyc
    │   ├── chart_page.cpython-313.pyc
    │   ├── setting_page.cpython-311.pyc
    │   ├── setting_page.cpython-313.pyc
    │   ├── timeline_page.cpython-311.pyc
    │   └── timeline_page.cpython-313.pyc
    ├── chart_page.py
    ├── setting_page.py
    └── timeline_page.py

13 directories, 75 files""""
```

## 

-   病棟データの午前午後の定義 ：午前午後ごとに病棟データをつける 本来 12:30-13:00 は空白だが、午後にまとめることにする

-   {時間 == time,業務種類 == task,件数 == count,病棟 == locate,薬剤師名 == PhName,その他コメント==comment}
