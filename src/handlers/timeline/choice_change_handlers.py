class ChoiceChangeHandlers:
    @staticmethod
    def change_choice_button(e, selectColumns, page):
        # visible falseで重くなるようであればclearの使用を検討する
        # selectColumns[0].controls.clear()
        match int(e.data):
            case 0:  # 病棟担当
                selectColumns[0].visible = True  # 情報収集　指導
                selectColumns[1].visible = True  # 指導記録作成
                selectColumns[2].visible = True  # 混注時間
                selectColumns[3].visible = True  # 薬剤セット・確認
                selectColumns[4].visible = True  # 持参薬を確認
                selectColumns[5].visible = True  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = True  # 処方代理修正
                selectColumns[7].visible = True  # TDM実施
                selectColumns[8].visible = True  # カンファレンス
                selectColumns[9].visible = True  # 医師からの相談
                selectColumns[10].visible = True  # 看護師からの相談
                selectColumns[11].visible = True  # その他の職種からの相談

                # 非表示
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 褥瘡
                selectColumns[18].visible = False  # TPN評価
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 手術使用麻薬確認・補充
                selectColumns[24].visible = False  # 術後疼痛管理チーム回診
                selectColumns[25].visible = False  # 脳卒中ホットライン対応
                selectColumns[26].visible = False  # 業務調整
                selectColumns[27].visible = False  # 休憩
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 管理業務
                selectColumns[30].visible = False  # NST
                selectColumns[31].visible = False  # 問い合わせ応需
                selectColumns[32].visible = False  # マスター作成・変更
                selectColumns[33].visible = False  # 薬剤情報評価
                selectColumns[34].visible = False  # 後発品選定
                selectColumns[35].visible = False  # 会議資料作成
                selectColumns[36].visible = False  # 配信資料作成
                selectColumns[37].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成
                selectColumns[41].visible = False  # 薬剤使用期限確認
                selectColumns[42].visible = False  # 抗菌薬相談対応
                selectColumns[43].visible = False  # 事前準備
                selectColumns[44].visible = False  # カンファ・ラウンド
                selectColumns[45].visible = False  # 記録作成

                page.update()
            case 1:  # 12階
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 抗菌薬相談対応
                selectColumns[18].visible = False  # 褥瘡
                selectColumns[19].visible = False  # TPN評価
                # 表示
                selectColumns[20].visible = True  # 手術使用薬剤確認
                selectColumns[21].visible = True  # 手術使用薬剤準備
                selectColumns[22].visible = True  # 周術期薬剤管理関連
                selectColumns[23].visible = True  # 麻酔科周術期外来
                selectColumns[24].visible = True  # 手術後使用麻薬確認・補充
                selectColumns[25].visible = True  # 術後疼痛管理チーム回診
                selectColumns[26].visible = True  # 脳卒中ホットライン対応
                #非表示
                selectColumns[27].visible = False  # 業務調整
                selectColumns[28].visible = False  # 休憩
                selectColumns[29].visible = False  # その他
                selectColumns[30].visible = False  # 管理業務
                selectColumns[31].visible = False  # NST
                selectColumns[32].visible = False  # 問い合わせ応需
                selectColumns[33].visible = False  # マスター作成・変更
                selectColumns[34].visible = False  # 薬剤情報評価
                selectColumns[35].visible = False  # 後発品選定
                selectColumns[36].visible = False  # 会議資料作成
                selectColumns[37].visible = False  # 配信資料作成
                selectColumns[38].visible = False  # フォーミュラリー作成
                selectColumns[39].visible = False  # 外来処方箋修正
                selectColumns[40].visible = False  # 勉強会資料作成・開催
                selectColumns[41].visible = False  # お役立ち情報作成
                #表示
                selectColumns[42].visible = True  # 薬剤使用期限確認
                #非表示
                selectColumns[43].visible = False  # 事前準備
                selectColumns[44].visible = False  # カンファ・ラウンド
                selectColumns[45].visible = False  # 記録作成

                page.update()

            case 2:  # 役職者
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 抗菌薬相談対応
                selectColumns[18].visible = False  # 褥瘡
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 麻酔科周術期外来
                selectColumns[24].visible = False  # 手術使用麻薬確認・補充
                selectColumns[25].visible = False  # 術後疼痛管理チーム回診
                selectColumns[26].visible = False  # 脳卒中ホットライン対応
                selectColumns[27].visible = False  # 業務調整
                selectColumns[28].visible = False  # 休憩
                selectColumns[29].visible = False  # その他
                #表示
                selectColumns[30].visible = True  # 管理業務

                #非表示
                selectColumns[31].visible = False  # NST
                selectColumns[32].visible = False  # 問い合わせ応需
                selectColumns[33].visible = False  # マスター作成・変更
                selectColumns[34].visible = False  # 薬剤情報評価
                selectColumns[35].visible = False  # 後発品選定
                selectColumns[36].visible = False  # 会議資料作成
                selectColumns[37].visible = False  # 配信資料作成
                selectColumns[38].visible = False  # フォーミュラリー作成
                selectColumns[39].visible = False  # 外来処方箋修正
                selectColumns[40].visible = False  # 勉強会資料作成・開催
                selectColumns[41].visible = False  # お役立ち情報作成
                selectColumns[42].visible = False  # 薬剤使用期限確認
                selectColumns[43].visible = False  # 事前準備
                selectColumns[44].visible = False  # カンファ・ラウンド
                selectColumns[45].visible = False  # 記録作成

                page.update()

            case 3:  # その他
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                # 表示
                selectColumns[12].visible = True  # 委員会
                selectColumns[13].visible = True  # 勉強会参加
                selectColumns[14].visible = True  # WG活動
                selectColumns[15].visible = True  # 1on1

                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 抗菌薬相談対応
                selectColumns[18].visible = False  # 褥瘡
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # TPN評価
                selectColumns[21].visible = False  # 手術使用薬剤確認
                selectColumns[22].visible = False  # 手術使用薬剤準備
                selectColumns[23].visible = False  # 周術期薬剤管理関連
                selectColumns[24].visible = False  # 手術使用麻薬確認・補充
                selectColumns[25].visible = False  # 術後疼痛管理チーム回診
                selectColumns[26].visible = False  # 脳卒中ホットライン対応

                #表示
                selectColumns[27].visible = True  # 業務調整
                selectColumns[28].visible = True  # 休憩
                selectColumns[29].visible = True  # その他
                # 非表示
                selectColumns[30].visible = False  # 管理業務
                selectColumns[31].visible = False  # NST
                selectColumns[32].visible = False  # 問い合わせ応需
                selectColumns[33].visible = False  # マスター作成・変更
                selectColumns[34].visible = False  # 薬剤情報評価
                selectColumns[35].visible = False  # 後発品選定
                selectColumns[36].visible = False  # 会議資料作成
                selectColumns[37].visible = False  # 配信資料作成
                selectColumns[38].visible = False  # フォーミュラリー作成
                selectColumns[38].visible = False  # 外来処方箋修正
                selectColumns[39].visible = False  # 勉強会資料作成・開催
                selectColumns[40].visible = False  # お役立ち情報作成
                selectColumns[41].visible = False  # 薬剤使用期限確認
                selectColumns[42].visible = False  # 抗菌薬相談対応
                selectColumns[43].visible = False  # 事前準備
                selectColumns[44].visible = False  # カンファ・ラウンド
                selectColumns[45].visible = False  # 記録作成

                page.update()
            case 4:  # ICT/AST/NST/緩和・回診    
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
                selectColumns[4].visible = False  # 持参薬を確認
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # WG活動
                selectColumns[15].visible = False  # 1on1
                # 表示
                selectColumns[16].visible = True  # ICT/AST
                selectColumns[17].visible = True  # 抗菌薬相談対応
                selectColumns[18].visible = True  # 褥瘡
                selectColumns[19].visible = True  # TPN評価
                #非表示
                selectColumns[20].visible = False  # 手術使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 麻酔科周術期外来
                selectColumns[24].visible = False  # 手術使用麻薬確認・補充
                selectColumns[25].visible = False  # 術後疼痛管理チーム回診
                selectColumns[26].visible = False  # 脳卒中ホットライン対応
                selectColumns[27].visible = False  # 業務調整
                selectColumns[28].visible = False  # 休憩
                selectColumns[29].visible = False  # その他
                selectColumns[30].visible = False  # 管理業務
                #表示
                selectColumns[31].visible = True  # NST
                #非表示
                selectColumns[32].visible = False  # 問い合わせ応需
                selectColumns[33].visible = False  # マスター作成・変更
                selectColumns[34].visible = False  # 薬剤情報評価
                selectColumns[35].visible = False  # 後発品選定
                selectColumns[36].visible = False  # 会議資料作成
                selectColumns[37].visible = False  # 配信資料作成
                selectColumns[38].visible = False  # フォーミュラリー作成
                selectColumns[39].visible = False  # 外来処方箋修正
                selectColumns[40].visible = False  # 勉強会資料作成・開催
                selectColumns[41].visible = False  # お役立ち情報作成
                selectColumns[42].visible = False  # 薬剤使用期限確認
                #表示
                selectColumns[43].visible = True  # 事前準備
                selectColumns[44].visible = True  # カンファ・ラウンド
                selectColumns[45].visible = True  # 記録作成

                page.update()

            case 5:  # DI
                # 非表示
                selectColumns[0].visible = False  # 情報収集　指導
                selectColumns[1].visible = False  # 指導記録作成
                selectColumns[2].visible = False  # 混注時間
                selectColumns[3].visible = False  # 薬剤セット・確認
                # 表示
                selectColumns[4].visible = True  # 持参薬を確認
                # 非表示
                selectColumns[5].visible = False  # 薬剤服用歴等について保険k薬局へ照会
                selectColumns[6].visible = False  # 処方代理修正
                selectColumns[7].visible = False  # TDM実施
                selectColumns[8].visible = False  # カンファレンス
                selectColumns[9].visible = False  # 医師からの相談
                selectColumns[10].visible = False  # 看護師からの相談
                selectColumns[11].visible = False  # その他の職種からの相談
                selectColumns[12].visible = False  # 委員会
                selectColumns[13].visible = False  # 勉強会参加
                selectColumns[14].visible = False  # 　WG活動
                selectColumns[15].visible = False  # 1on1
                selectColumns[16].visible = False  # ICT/AST
                selectColumns[17].visible = False  # 抗菌薬相談対応
                selectColumns[18].visible = False  # 褥瘡
                selectColumns[19].visible = False  # TPN評価
                selectColumns[20].visible = False  # 手術後使用薬剤確認
                selectColumns[21].visible = False  # 手術使用薬剤準備
                selectColumns[22].visible = False  # 周術期薬剤管理関連
                selectColumns[23].visible = False  # 麻酔科周術期外来
                selectColumns[24].visible = False  # 手術使用麻薬確認・補充
                selectColumns[25].visible = False  # 術後疼痛管理チーム回診
                selectColumns[26].visible = False  # 脳卒中ホットライン対応
                selectColumns[27].visible = False  # 業務調整
                selectColumns[28].visible = False  # その他
                selectColumns[29].visible = False  # 休憩
                selectColumns[30].visible = False  # 管理業務
                selectColumns[31].visible = False  # NST


                # 表示
                selectColumns[32].visible = True  # 問い合わせ応需
                selectColumns[33].visible = True  # マスター作成・変更
                selectColumns[34].visible = True  # 薬剤情報評価
                selectColumns[35].visible = True  # 後発品選定
                selectColumns[36].visible = True  # 会議資料作成
                selectColumns[37].visible = True  # 配信資料作成
                selectColumns[38].visible = True  # フォーミュラリー作成
                selectColumns[39].visible = True  # 外来処方箋修正
                selectColumns[40].visible = True  # 勉強会資料作成・開催
                selectColumns[41].visible = True  # お役立ち情報作成
                #非表示
                selectColumns[42].visible = False  # 薬剤使用期限確認
                #表示
                selectColumns[43].visible = False  # 事前準備
                selectColumns[44].visible = False  # カンファ・ラウンド
                selectColumns[45].visible = False  # 記録作成

                page.update()