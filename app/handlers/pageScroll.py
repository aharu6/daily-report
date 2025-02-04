class Scroll:
    @staticmethod
    def scroll_forward(pageContents,e,page):
        pass
        
        
    @staticmethod
    def scroll_back(pageContents,target_position):
        #target_positionにて目的の位置のカラムまで移動する
        pageContents.scroll_to(target_position)
        
