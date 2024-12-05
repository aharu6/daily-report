# dairy-report

- 病棟データの午前午後の定義 午前午後ごとに病棟データをつける
  本来 12:30-13:00 は空白だが、午後にまとめることにする

- データの基本形 {時間 == time,業務種類 == task,件数 == count,病棟 ==
  locate,薬剤師名 == PhName}

### やること

- 削除ボタン 入力したデータの削除
タイムライン左に編集ボタン
押したらタスク上に赤いマイナスボタンが出てくる
押したら削除

- 日付を選択したときのリロード

- ~伸ばしたときのコピー実装~

- 最後に動かした task がコピーされるようになっている。
  最後にクリックした時点で lastdata に入れる-コピーに反映する

- ~動的に srcid のリスト生成~

- 切り替えスライドボタンで業種ごとの業務内容表示or非表示に

- 伸ばしたときの見た目修正

メモデータベースの項目数を増やした時は、前の sql データベースは一回削除する
