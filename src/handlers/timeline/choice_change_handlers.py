class ChoiceChangeHandlers:
    @staticmethod
    def change_choice_button(e, selectColumns, page):
        # visible falseで重くなるようであればclearの使用を検討する
        # selectColumns[0].controls.clear()
        match int(e.data):
            case 0:  # 病棟担当
                selectColumns[0].visible = True  # 初回・中間指導情報収集
                selectColumns[1].visible = True  # 退院指導情報収集
                selectColumns[2].visible = True  # 注射台車監査
                selectColumns[3].visible = True  # 服薬指導
                selectColumns[4].visible = True  # 指導記録作成
                selectColumns[5].visible = True  # 無菌調製(調製者)
                selectColumns[6].visible = True  # 無菌調製補助業（準備、監査）
                selectColumns[7].visible = True  # 薬剤セット
                selectColumns[8].visible = True  # 薬剤セット確認
                selectColumns[9].visible = True  # 持参薬を確認
                selectColumns[10].visible = True  # 薬剤服用歴等について保険薬局へ照会
                selectColumns[11].visible = True  # 薬剤サマリー作成
                selectColumns[12].visible = True  # 処方代理修正・代行入力
                selectColumns[13].visible = True  # TDM実施
                selectColumns[14].visible = True  # カンファレンス
                selectColumns[15].visible = True  # 問い合わせ業務

                # 非表示
                selectColumns[16].visible = False  # 委員会
                selectColumns[17].visible = False  # 勉強会参加
                selectColumns[18].visible = False  # WG活動
                selectColumns[19].visible = False  # 1on1
                selectColumns[20].visible = False  # ICT
                selectColumns[21].visible = False  # AST
                selectColumns[22].visible = False  # 抗菌薬相談対応
                selectColumns[23].visible = False  # 褥瘡
                selectColumns[24].visible = False  # TPN評価
                selectColumns[25].visible = False  # 手術後使用薬剤確認
                selectColumns[26].visible = False  # 手術使用薬剤確認
                selectColumns[27].visible = False  # 周術期薬剤管理記録作成
                selectColumns[28].visible = False  # 周術期薬剤管理準備
                selectColumns[29].visible = False  # 麻酔科周術期外来予約確認
                selectColumns[30].visible = False  # 麻酔科周術期外来情報収集
                selectColumns[31].visible = False  # 麻酔科周術期外来
                selectColumns[32].visible = False  # 麻酔科主従周術期外来記録
                selectColumns[33].visible = False  # 手術使用麻薬確認・補充
                selectColumns[34].visible = False  # APSチーム回診情報収集
                selectColumns[35].visible = False  # APSチーム回診
                selectColumns[36].visible = False  # APS関連記録作成
                selectColumns[37].visible = False  # 脳卒中ホットライン対応
                selectColumns[38].visible = False  # 手術使用薬剤確認・補充
                selectColumns[39].visible = False  # 注射薬調製
                selectColumns[40].visible = False  # 金庫管理定数確認
                selectColumns[41].visible = False  # 業務調製
                selectColumns[42].visible = False  # 休憩
                selectColumns[43].visible = False  # その他
                selectColumns[44].visible = False  # 管理業務
                selectColumns[45].visible = False  # 　NST
                selectColumns[46].visible = False  # マスター作成・変更
                selectColumns[47].visible = False  # 薬剤情報評価
                selectColumns[48].visible = False  # 後発品選定
                selectColumns[49].visible = False  # 会議資料作成
                selectColumns[50].visible = False  # 配信資料作成
                selectColumns[51].visible = False  # フォーミュラリー作成
                selectColumns[52].visible = False  # 外来処方箋修正
                selectColumns[53].visible = False  # 勉強会資料作成・開催
                selectColumns[54].visible = False  # お役立ち情報作成
                selectColumns[55].visible = False  # 薬剤使用期限確認
                selectColumns[56].visible = False  # 緩和回診
                selectColumns[57].visible = False  # 心不全回診
                selectColumns[58].visible = False  # 緩和回診記録作成
                selectColumns[59].visible = False  # 手術室サテライト薬剤定数確認
                selectColumns[60].visible = False  # ICTリンクスタッフ活動
                selectColumns[61].visible = False  # 医療安全対策WG活動
                selectColumns[62].visible = False  # 実習生対応
                selectColumns[63].visible = False  # 薬剤部連絡会

                page.update()
            case 1:  # 12階
                # 非表示
                selectColumns[0].visible = False  # 初回・中間指導情報収集
                selectColumns[1].visible = False  # 退院指導情報収集
                selectColumns[2].visible = False  # 注射台車監査
                selectColumns[3].visible = False  # 服薬指導
                selectColumns[4].visible = False  # 指導記録作成
                selectColumns[5].visible = False  # 無菌調製(調製者)
                selectColumns[6].visible = False  # 無菌調製補助業務（準備、監査）
                selectColumns[7].visible = False  # 薬剤セット
                selectColumns[8].visible = False  # 薬剤セット確認
                selectColumns[9].visible = False  # 持参薬を確認
                selectColumns[10].visible = False  # 薬剤服用歴等について保険薬局へ照会
                selectColumns[11].visible = False  # 薬剤サマリー作成
                selectColumns[12].visible = False  # 処方代理修正・代行入力
                selectColumns[13].visible = False  # TDM実施
                selectColumns[14].visible = False  # カンファレンス
                selectColumns[15].visible = False  # 問い合わせ業務
                selectColumns[16].visible = False  # 委員会
                selectColumns[17].visible = False  # 勉強会参加
                selectColumns[18].visible = False  # WG活動
                selectColumns[19].visible = False  # 1on1
                selectColumns[20].visible = False  # ICT 
                selectColumns[21].visible = False  # AST
                selectColumns[22].visible = False  # 抗菌薬相談対応
                selectColumns[23].visible = False  # 褥瘡
                selectColumns[24].visible = False  # TPN評価
                
                #表示
                selectColumns[25].visible = True  # 手術後使用薬剤確認
                selectColumns[26].visible = True  # 手術使用薬剤準備
                selectColumns[27].visible = True  # 周術期薬剤管理記録作成
                selectColumns[28].visible = True  # 周術期薬剤管理準備
                selectColumns[29].visible = True  # 麻酔科周術期外来予約確認
                selectColumns[30].visible = True  # 麻酔科周術期外来情報収集
                selectColumns[31].visible = True  # 麻酔科周術期外来
                selectColumns[32].visible = True  # 麻酔科周術期外来記録 
                selectColumns[33].visible = True  # 手術使用麻薬確認・補充
                selectColumns[34].visible = True  # APSチーム回診情報収集
                selectColumns[35].visible = True  # APSチーム回診
                selectColumns[36].visible = True  # APS関連記録作成
                selectColumns[37].visible = True  # 脳卒中ホットライン対応
                selectColumns[38].visible = True  # 手術使用薬剤確認・補充
                selectColumns[39].visible = True  # 注射薬調製
                selectColumns[40].visible = True  # 金庫管理定数確認
                
                #非表示
                selectColumns[41].visible = False  # 業務調整
                selectColumns[42].visible = False  # 休憩
                selectColumns[43].visible = False  # その他
                selectColumns[44].visible = False  # 管理業務
                selectColumns[45].visible = False  # NST
                selectColumns[46].visible = False  # マスター作成・変更
                selectColumns[47].visible = False  # 薬剤情報評価
                selectColumns[48].visible = False  # 後発品選定
                selectColumns[49].visible = False  # 会議資料作成
                selectColumns[50].visible = False  # 配信資料作成
                selectColumns[51].visible = False  # フォーミュラリー作成
                selectColumns[52].visible = False  # 外来処方箋修正
                selectColumns[53].visible = False  # 勉強会資料作成・開催
                selectColumns[54].visible = False  # お役立ち情報作成
                selectColumns[55].visible = False  # 薬剤使用期限確認
                selectColumns[56].visible = False  # 緩和回診
                selectColumns[57].visible = False  # 心不全回診
                selectColumns[58].visible = False  # 緩和回診記録作成
                #表示
                selectColumns[59].visible = True  # 手術室サテライト薬剤定数確認
                #非表示
                selectColumns[60].visible = False  # ICTリンクスタッフ活動
                selectColumns[61].visible = False  # 医療安全対策WG活動
                selectColumns[62].visible = False  # 実習生対応
                selectColumns[63].visible = False  # 薬剤部連絡会

                page.update()

            case 2:  # 役職者
                # 非表示
                selectColumns[0].visible = False  # 初回・中間指導情報収集
                selectColumns[1].visible = False  # 退院指導情報収集
                selectColumns[2].visible = False  # 注射台車監査
                selectColumns[3].visible = False  # 服薬指導
                selectColumns[4].visible = False  # 指導記録作成
                selectColumns[5].visible = False  # 無菌調製(調製者)
                selectColumns[6].visible = False  # 無菌調製補助業務（準備、監査）
                selectColumns[7].visible = False  # 薬剤セット
                selectColumns[8].visible = False  # 薬剤セット確認
                selectColumns[9].visible = False  # 持参薬を確認
                selectColumns[10].visible = False  # 薬剤服用歴等について保険薬局へ照会
                selectColumns[11].visible = False  # 薬剤サマリー作成
                selectColumns[12].visible = False  # 処方代理修正・代行入力
                selectColumns[13].visible = False  # TDM実施
                selectColumns[14].visible = False  # カンファレンス
                selectColumns[15].visible = False  # 問い合わせ業務
                selectColumns[16].visible = False  # 委員会
                selectColumns[17].visible = False  # 勉強会参加
                selectColumns[18].visible = False  # WG活動
                selectColumns[19].visible = False  # 1on1
                selectColumns[20].visible = False  # ICT
                selectColumns[21].visible = False  # AST
                selectColumns[22].visible = False  # 抗菌薬相談対応
                selectColumns[23].visible = False  # 褥瘡
                selectColumns[24].visible = False  # TPN評価
                selectColumns[25].visible = False  # 手術後使用薬剤確認
                selectColumns[26].visible = False  # 手術使用薬剤準備
                selectColumns[27].visible = False  # 周術期薬剤管理記録作成
                selectColumns[28].visible = False  # 周術期薬剤管理準備
                selectColumns[29].visible = False  # 麻酔科周術期外来予約確認
                selectColumns[30].visible = False  # 麻酔科周術期外来情報収集
                selectColumns[31].visible = False  # 麻酔科周術期外来
                selectColumns[32].visible = False  # 麻酔科周術期外来記録
                selectColumns[33].visible = False  # 手術使用麻薬確認・補充
                selectColumns[34].visible = False  # APSチーム回診情報収集
                selectColumns[35].visible = False  # APSチーム回診
                selectColumns[36].visible = False  # APS関連記録作成
                selectColumns[37].visible = False  # 脳卒中ホットライン対応
                selectColumns[38].visible = False  # 手術使用薬剤確認・補充
                selectColumns[39].visible = False  # 注射薬調製
                selectColumns[40].visible = False  # 金庫管理定数確認
                selectColumns[41].visible = False  # 業務調整
                selectColumns[42].visible = False  # 休憩
                selectColumns[43].visible = False  # その他
                
                # 表示
                selectColumns[44].visible = True  # 管理業務
                # 非表示
                selectColumns[45].visible = False  # NST
                selectColumns[46].visible = False  # 
                selectColumns[47].visible = False  # 
                selectColumns[48].visible = False  # 
                selectColumns[49].visible = False  # 
                selectColumns[50].visible = False  # 
                selectColumns[51].visible = False  # 
                selectColumns[52].visible = False  # 
                selectColumns[53].visible = False  # 
                selectColumns[54].visible = False  # 
                selectColumns[55].visible = False  # 
                selectColumns[56].visible = False  # 
                selectColumns[57].visible = False  # 
                selectColumns[58].visible = False  # 
                selectColumns[59].visible = False  # 
                selectColumns[60].visible = False  # 
                selectColumns[61].visible = False  #   
                selectColumns[62].visible = False  # 
                selectColumns[63].visible = False  # 
                
                page.update()

            case 3:  # その他
                selectColumns[0].visible = False  # 初回・中間指導情報収集
                selectColumns[1].visible = False  # 退院時時指導情報収集
                selectColumns[2].visible = False  # 注射台車監査
                selectColumns[3].visible = False  # 服薬指導
                selectColumns[4].visible = False  # 指導記録作成
                selectColumns[5].visible = False  # 無菌調製(調製者)
                selectColumns[6].visible = False  # 無菌調製補助業務（準備、監査）
                selectColumns[7].visible = False  # 薬剤セット
                selectColumns[8].visible = False  # 薬剤セット確認
                selectColumns[9].visible = False  # 持参薬を確認
                selectColumns[10].visible = False  # 薬剤服用歴等について保険薬局へ照会
                selectColumns[11].visible = False  # 薬剤サマリー作成
                selectColumns[12].visible = False  # 処方代理修正・代行入力
                selectColumns[13].visible = False  # TDM実施
                selectColumns[14].visible = False  # カンファレンス
                selectColumns[15].visible = False  # 問い合わせ業務
                
                # 表示
                selectColumns[16].visible = True  # 委員会
                selectColumns[17].visible = True  # 勉強会参加
                selectColumns[18].visible = True  # WG活動
                selectColumns[19].visible = True  # 1on1
                
                # 非表示
                selectColumns[20].visible = False  # ICT
                selectColumns[21].visible = False  # AST
                selectColumns[22].visible = False  # 抗菌薬相談対応
                selectColumns[23].visible = False  # 褥瘡
                selectColumns[24].visible = False  # TPN評価
                selectColumns[25].visible = False  # 手術後使用薬剤確認
                selectColumns[26].visible = False  # 手術使用薬剤準備
                selectColumns[27].visible = False  # 周術期薬剤管理記録作成
                selectColumns[28].visible = False  # 周術期薬剤管理準備
                selectColumns[29].visible = False  # 麻酔科周術期外来予約確認
                selectColumns[30].visible = False  # 麻酔科周術期外来情報収集
                selectColumns[31].visible = False  # 麻酔科周術期外来
                selectColumns[32].visible = False  # 麻酔科周術期外来記録
                selectColumns[33].visible = False  # 手術使用麻薬確認・補充
                selectColumns[34].visible = False  # APSチーム回診情報収集
                selectColumns[35].visible = False  # APSチーム回診
                selectColumns[36].visible = False  # APS関連記録作成
                selectColumns[37].visible = False  # 脳卒中ホットライン対応
                selectColumns[38].visible = False  # 手術使用薬剤確認・補充
                selectColumns[38].visible = False  # 手術使用薬剤確認・補充
                selectColumns[39].visible = False  # 注射薬調製
                selectColumns[40].visible = False  # 金庫管理定数確認
                
                #　表示
                selectColumns[41].visible = True  # 業務調整
                selectColumns[42].visible = True  # 休憩
                selectColumns[43].visible = True  # その他
                # 非表示
                selectColumns[44].visible = False  # 管理業務
                selectColumns[45].visible = False  # NST
                selectColumns[46].visible = False  # 
                selectColumns[47].visible = False  # 
                selectColumns[48].visible = False  # 
                selectColumns[49].visible = False  # 
                selectColumns[50].visible = False  # 
                selectColumns[51].visible = False  # 
                selectColumns[52].visible = False  # 
                selectColumns[53].visible = False  # 
                selectColumns[54].visible = False  # 
                selectColumns[55].visible = False  # 
                selectColumns[56].visible = False  # 
                selectColumns[57].visible = False  # 
                selectColumns[58].visible = False  # 
                selectColumns[59].visible = False  # 
                #表示
                selectColumns[60].visible = True  # ICTリンクスタッフ活動
                selectColumns[61].visible = True  # 医療安全対策WG活動
                selectColumns[62].visible = True  # 実習生対応
                selectColumns[63].visible = True  # 薬剤部連絡会
                
                page.update()
            case 4:  # ICT/AST/NST/緩和・回診    
                # 非表示
                selectColumns[0].visible = False  # 初回・中間指導情報収集
                selectColumns[1].visible = False  # 退院指導情報収集
                selectColumns[2].visible = False  # 注射台車監査
                selectColumns[3].visible = False  # 服薬指導
                selectColumns[4].visible = False  # 指導記録作成
                selectColumns[5].visible = False  # 無菌調製(調製者)
                selectColumns[6].visible = False  # 無菌調製補助業務（準備、監査）
                selectColumns[7].visible = False  # 薬剤セット
                selectColumns[8].visible = False  # 薬剤セット確認
                selectColumns[9].visible = False  # 持参薬を確認
                selectColumns[10].visible = False  # 薬剤服用歴等について保険薬局へ照会
                selectColumns[11].visible = False  # 薬剤サマリー作成
                selectColumns[12].visible = False  # 処方代理修正・代行入力
                selectColumns[13].visible = False  # TDM実施
                selectColumns[14].visible = False  # カンファレンス
                selectColumns[15].visible = False  # 問い合わせ業務
                selectColumns[16].visible = False  # 委員会
                selectColumns[17].visible = False  # 勉強会参加
                selectColumns[18].visible = False  # WG活動
                selectColumns[19].visible = False  # 1on1
                #表示
                selectColumns[20].visible = True  # ICT
                selectColumns[21].visible = True  # AST
                selectColumns[22].visible = True  # 抗菌薬相談対応
                selectColumns[23].visible = True  # 褥瘡
                selectColumns[24].visible = True  # TPN評価
                #非表示
                selectColumns[25].visible = False  # 手術後使用薬剤確認
                selectColumns[26].visible = False  # 手術使用薬剤準備
                selectColumns[27].visible = False  # 周術期薬剤管理記録作成
                selectColumns[28].visible = False  # 周術期薬剤管理準備
                selectColumns[29].visible = False  # その科周術期外来予約確認
                selectColumns[30].visible = False  # 麻酔科周術期外来情報収集
                selectColumns[31].visible = False  # 麻酔科周術期外来
                selectColumns[32].visible = False  # 麻酔科周術期外来記録
                selectColumns[33].visible = False  # 手術使用麻薬確認・補充
                selectColumns[34].visible = False  # APSチーム回診情報収集
                selectColumns[35].visible = False  # APSチーム回診
                selectColumns[36].visible = False  # APS関連記録作成
                selectColumns[37].visible = False  # 脳卒中ホットライン対応
                selectColumns[38].visible = False  # 手術使用薬剤確認・補充
                selectColumns[39].visible = False  # 注射薬調製
                selectColumns[40].visible = False  # 金庫管理定数確認
                selectColumns[41].visible = False  # 業務調整
                selectColumns[42].visible = False  # 休憩
                selectColumns[43].visible = False  # その他
                selectColumns[44].visible = False  # 管理業務
                #表示
                selectColumns[45].visible = True  # NST
                #非表示
                selectColumns[46].visible = False  # マスター作成・変更
                selectColumns[47].visible = False  # 薬剤情報評価
                selectColumns[48].visible = False  # 後発品選定
                selectColumns[49].visible = False  # 会議資料作成
                selectColumns[50].visible = False  # 配信資料作成
                selectColumns[51].visible = False  # フォーミュラリー作
                selectColumns[52].visible = False  # 外来処方箋修正
                selectColumns[53].visible = False  # 勉強会資料作成・
                selectColumns[54].visible = False  # お役立ち情報作成
                selectColumns[55].visible = False  # 薬剤使用期限確認
                #表示
                selectColumns[56].visible = True  # 緩和回診
                selectColumns[57].visible = True  # 心不全回診
                selectColumns[58].visible = True  # 緩和回診記録作
                #非表示
                selectColumns[59].visible = False  # 手術室サテライト薬剤定数確認
                selectColumns[60].visible = False  # ICTリンクスタッフ活動
                selectColumns[61].visible = False  # 医療安全対策WG活動
                selectColumns[62].visible = False  # 実習生対応
                selectColumns[63].visible = False  # 薬剤部連絡会
                
                page.update()

            case 5:  # DI
                # 非表示
                selectColumns[0].visible = False  # 初回・中間指導情報収集
                selectColumns[1].visible = False  # 退院指導情報収集
                selectColumns[2].visible = False  # 注射台車監査
                selectColumns[3].visible = False  # 服薬指導
                selectColumns[4].visible = False  # 指導記録作成
                selectColumns[5].visible = False  # 無菌調製(調製者)
                selectColumns[6].visible = False  # 無菌調製補助業務（準備、監査）
                selectColumns[7].visible = False  # 薬剤セット
                selectColumns[8].visible = False  # 薬剤セット確認
                #表示
                selectColumns[9].visible = True  # 持参薬を確認
                #非表示
                selectColumns[10].visible = False  # 薬剤服用歴等について保険薬局へ照会
                selectColumns[11].visible = False  # 薬剤サマリー作成
                selectColumns[12].visible = False  # 処方代理修正・代行入力
                selectColumns[13].visible = False  # TDM実施
                selectColumns[14].visible = False  # カンファレンス
                #表示
                selectColumns[15].visible = True # 問い合わせ業務
                #非表示
                selectColumns[16].visible = False  # 委員会
                selectColumns[17].visible = False  # 勉強会参加
                selectColumns[18].visible = False  # WG活動
                selectColumns[19].visible = False  # 1on1
                selectColumns[20].visible = False  # ICT
                selectColumns[21].visible = False  # AST
                selectColumns[22].visible = False  # 抗菌薬相談対応
                selectColumns[23].visible = False  # 褥瘡
                selectColumns[24].visible = False  # TPN評価
                selectColumns[25].visible = False  # 手術後使用薬剤確認
                selectColumns[26].visible = False  # 
                selectColumns[27].visible = False  # 
                selectColumns[28].visible = False  # 
                selectColumns[29].visible = False  # 
                selectColumns[30].visible = False  # 
                selectColumns[31].visible = False  #
                selectColumns[32].visible = False  # 麻酔科周術期外来記録
                selectColumns[33].visible = False  # 
                selectColumns[34].visible = False  # 
                selectColumns[34].visible = False  # APSチーム回診情報収集
                selectColumns[35].visible = False  # APSチーム回診
                selectColumns[36].visible = False  # APS関連記録作成
                selectColumns[37].visible = False  # 脳卒中ホットライン対応
                selectColumns[38].visible = False  # 手術使用薬剤確認・補充
                selectColumns[39].visible = False  # 注射薬調製
                selectColumns[40].visible = False  # 金庫管理定数確認
                selectColumns[41].visible = False  # 業務調整
                selectColumns[42].visible = False  # 休憩
                selectColumns[43].visible = False  # その他
                selectColumns[44].visible = False  # 管理業務
                selectColumns[45].visible = False  # NST
                #表示
                selectColumns[46].visible = True  # マスター作成・変更
                selectColumns[47].visible = True  # 薬剤情報評価
                selectColumns[48].visible = True  # 後発品選定
                selectColumns[49].visible = True  # 会議資料作成
                selectColumns[50].visible = True  # 配信資料作成
                selectColumns[51].visible = True  # フォーミュラリー作
                selectColumns[52].visible = True  # 外来処方箋修正
                selectColumns[53].visible = True  # 勉強会資料作成・
                selectColumns[54].visible = True  # お役立ち情報作成
                
                #非表示
                selectColumns[55].visible = False  # 薬剤使用期限確認
                selectColumns[56].visible = False  # 緩和回診
                selectColumns[57].visible = False  # 心不全回診
                selectColumns[58].visible = False  # 緩和回診記録作
                selectColumns[59].visible = False  # 手術室サテライト薬剤
                selectColumns[60].visible = False  # ICTリンクスタッフ活動
                selectColumns[61].visible = False  # 医療安全対策WG活動
                selectColumns[62].visible = False  # 実習生対応
                selectColumns[63].visible = False  # 薬剤部連絡会                
                
                page.update()