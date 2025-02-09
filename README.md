# dairy-report

## 概要説明・機能

#### timeline_page

日誌としての入力・編集、書き出し

#### chart_page

timeline_pageにて書き出したcsvファイルを使用して、グラフの書き出し

#### setting_page

本体保存データの削除

## 使用環境

exeファイルに書き出し → windows10以上

64bitのみ対応

## 使い方

pyinstaller にてexeファイルに書き出して使用

## インストール方法

## 開発環境

Python 3.11.11

パッケージ → requirements.txt

フレームワーク flet 0.24.1

## 定義

-   8:30-12:30:AM 

-   13:00- :PM

-   {時間 == time,業務種類 == task,件数 == count,病棟 == locate,薬剤師名 == PhName,その他コメント==comment}
