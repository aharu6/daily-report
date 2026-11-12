"""
カウンターハンドラーのテスト
キーボード入力時にcount_dictが正しく更新されるかテスト
"""

import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# プロジェクトのsrcをパスに追加
sys.path.insert(0, str(Path(__file__).parent / "src"))

from handlers.timeline.counter_handlers import CounterHandlers


class TestCounterHandlers(unittest.TestCase):
    """カウンターハンドラーのテストクラス"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.count_dict = {}
        self.time = "09:00"
        # テスト用の初期データ
        self.count_dict[self.time] = {"count": 0}
    
    def test_counter_plus(self):
        """プラスボタンのテスト"""
        # モックオブジェクトの作成
        count_field = Mock()
        count_field.value = "0"
        count_field.update = Mock()
        
        event = Mock()
        
        # メソッド実行
        CounterHandlers.counterPlus(event, count_field, self.count_dict, self.time)
        
        # アサーション
        self.assertEqual(count_field.value, 1)
        self.assertEqual(self.count_dict[self.time]["count"], 1)
        count_field.update.assert_called_once()
    
    def test_counter_minus(self):
        """マイナスボタンのテスト"""
        # カウント値を5に設定
        self.count_dict[self.time]["count"] = 5
        
        count_field = Mock()
        count_field.value = "5"
        count_field.update = Mock()
        
        event = Mock()
        event.control = Mock()
        
        # メソッド実行
        CounterHandlers.counterMinus(event, count_field, self.count_dict, self.time)
        
        # アサーション
        self.assertEqual(count_field.value, 4)
        self.assertEqual(self.count_dict[self.time]["count"], 4)
        count_field.update.assert_called_once()
    
    def test_counter_minus_at_zero(self):
        """マイナスボタンで0未満にならないテスト"""
        self.count_dict[self.time]["count"] = 0
        
        count_field = Mock()
        count_field.value = "0"
        count_field.update = Mock()
        
        event = Mock()
        event.control = Mock()
        
        # メソッド実行
        CounterHandlers.counterMinus(event, count_field, self.count_dict, self.time)
        
        # アサーション - 0未満にならない
        self.assertEqual(count_field.value, 0)
        self.assertEqual(self.count_dict[self.time]["count"], 0)
    
    def test_counter_change_with_valid_input(self):
        """キーボード直接入力のテスト - 有効な入力値"""
        # キーボード入力をシミュレート
        event = Mock()
        event.control = Mock()
        event.control.value = "42"  # 直接入力
        
        # メソッド実行
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        
        # アサーション - count_dictが更新されているか確認
        self.assertEqual(
            self.count_dict[self.time]["count"], 
            42,
            "キーボード入力でcount_dictが更新されていません"
        )
    
    def test_counter_change_with_invalid_input(self):
        """キーボード直接入力のテスト - 無効な入力値"""
        event = Mock()
        event.control = Mock()
        event.control.value = "abc"  # 整数に変換できない
        
        # メソッド実行
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        
        # アサーション - 元の値が保持されているか確認
        self.assertEqual(self.count_dict[self.time]["count"], 0)
    
    def test_counter_change_with_negative_input(self):
        """キーボード直接入力のテスト - 負の値入力"""
        event = Mock()
        event.control = Mock()
        event.control.value = "-5"  # 負の値
        
        # メソッド実行
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        
        # アサーション - 0に設定されるか確認
        self.assertEqual(
            self.count_dict[self.time]["count"], 
            0,
            "負の値が入力されたときに0に設定されていません"
        )
    
    def test_counter_change_updates_dict_multiple_times(self):
        """複数回のキーボード入力テスト"""
        event = Mock()
        event.control = Mock()
        
        # 複数の値を入力
        test_values = ["10", "25", "30", "5"]
        
        for value in test_values:
            event.control.value = value
            CounterHandlers.counter_Change(event, self.count_dict, self.time)
            self.assertEqual(
                self.count_dict[self.time]["count"],
                int(value),
                f"値 {value} が正しく反映されていません"
            )
    
    def test_counter_change_with_multiple_times(self):
        """複数の時間帯でのカウンター入力テスト"""
        times = ["09:00", "10:00", "11:00"]
        
        # 各時間帯のデータを初期化
        for time in times:
            self.count_dict[time] = {"count": 0}
        
        event = Mock()
        event.control = Mock()
        
        # 各時間帯に異なる値を入力
        for i, time in enumerate(times):
            event.control.value = str(i + 5)
            CounterHandlers.counter_Change(event, self.count_dict, time)
        
        # アサーション
        self.assertEqual(self.count_dict["09:00"]["count"], 5)
        self.assertEqual(self.count_dict["10:00"]["count"], 6)
        self.assertEqual(self.count_dict["11:00"]["count"], 7)
    
    def test_counter_change_with_empty_input(self):
        """キーボード直接入力のテスト - 空文字列"""
        event = Mock()
        event.control = Mock()
        event.control.value = ""  # 空文字列
        
        # メソッド実行
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        
        # アサーション - 元の値が保持されているか確認
        self.assertEqual(self.count_dict[self.time]["count"], 0)
    
    def test_counter_change_with_zero_input(self):
        """キーボード直接入力のテスト - ゼロ入力"""
        # 初期値を10に設定
        self.count_dict[self.time]["count"] = 10
        
        event = Mock()
        event.control = Mock()
        event.control.value = "0"  # ゼロ
        
        # メソッド実行
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        
        # アサーション
        self.assertEqual(self.count_dict[self.time]["count"], 0)
    
    def test_counter_change_with_large_number(self):
        """キーボード直接入力のテスト - 大きな数値"""
        event = Mock()
        event.control = Mock()
        event.control.value = "9999"  # 大きな数値
        
        # メソッド実行
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        
        # アサーション
        self.assertEqual(self.count_dict[self.time]["count"], 9999)
    
    def test_counter_flow_keyboard_then_button(self):
        """キーボード入力後にボタンをクリックするフロー"""
        count_field = Mock()
        count_field.update = Mock()
        
        event = Mock()
        event.control = Mock()
        
        # ステップ1: キーボードで値を入力
        event.control.value = "15"
        CounterHandlers.counter_Change(event, self.count_dict, self.time)
        self.assertEqual(self.count_dict[self.time]["count"], 15)
        
        # ステップ2: プラスボタンをクリック
        count_field.value = "15"
        CounterHandlers.counterPlus(event, count_field, self.count_dict, self.time)
        
        # アサーション
        self.assertEqual(self.count_dict[self.time]["count"], 16)
        self.assertEqual(count_field.value, 16)


class TestCounterHandlersIntegration(unittest.TestCase):
    """統合テスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.count_dict = {}
        self.times = ["09:00", "10:00", "11:00", "13:00", "14:00"]
        
        for time in self.times:
            self.count_dict[time] = {"count": 0}
    
    def test_realistic_workflow(self):
        """実際の使用フローをシミュレートするテスト"""
        # シナリオ: ユーザーが複数の時間帯でカウンターを使用する
        
        event = Mock()
        event.control = Mock()
        
        # 時間09:00でキーボード直接入力: 3
        event.control.value = "3"
        CounterHandlers.counter_Change(event, self.count_dict, "09:00")
        
        # 時間10:00でキーボード直接入力: 5
        event.control.value = "5"
        CounterHandlers.counter_Change(event, self.count_dict, "10:00")
        
        # 時間11:00でボタンクリック
        count_field = Mock()
        count_field.value = "0"
        count_field.update = Mock()
        CounterHandlers.counterPlus(event, count_field, self.count_dict, "11:00")
        
        # 時間13:00でキーボード直接入力: 7
        event.control.value = "7"
        CounterHandlers.counter_Change(event, self.count_dict, "13:00")
        
        # 時間14:00でキーボード直接入力後にボタンクリック
        event.control.value = "2"
        CounterHandlers.counter_Change(event, self.count_dict, "14:00")
        count_field.value = "2"
        CounterHandlers.counterPlus(event, count_field, self.count_dict, "14:00")
        
        # アサーション
        self.assertEqual(self.count_dict["09:00"]["count"], 3)
        self.assertEqual(self.count_dict["10:00"]["count"], 5)
        self.assertEqual(self.count_dict["11:00"]["count"], 1)
        self.assertEqual(self.count_dict["13:00"]["count"], 7)
        self.assertEqual(self.count_dict["14:00"]["count"], 3)
    
    def test_count_dict_persistence(self):
        """count_dictのデータ永続性テスト"""
        # 複数の操作後にデータが保持されているか確認
        
        event = Mock()
        event.control = Mock()
        
        # 複数の値を入力
        inputs = [
            ("09:00", "10"),
            ("10:00", "20"),
            ("11:00", "30"),
        ]
        
        for time, value in inputs:
            event.control.value = value
            CounterHandlers.counter_Change(event, self.count_dict, time)
        
        # 別の時間で新しい値を入力
        event.control.value = "5"
        CounterHandlers.counter_Change(event, self.count_dict, "13:00")
        
        # 最初の値がまだ保持されているか確認
        self.assertEqual(self.count_dict["09:00"]["count"], 10)
        self.assertEqual(self.count_dict["10:00"]["count"], 20)
        self.assertEqual(self.count_dict["11:00"]["count"], 30)
        self.assertEqual(self.count_dict["13:00"]["count"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
