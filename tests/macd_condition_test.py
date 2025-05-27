# tests/macd_condition_test.py

import unittest
from src.signals.macd_conditions import (
    classify_histogram_numeric,
    macd_m12_signal_numeric,
    macd_m75_or_h4_filter_numeric
)

class TestMACDConditions(unittest.TestCase):

    def test_classify_histogram_numeric(self):
        test_cases = [
            (-0.05, -2),     # ĐỎ ĐẬM
            (-0.009, -1),    # ĐỎ LỢT
            (0.0005, 1),     # XANH LỢT
            (0.02, 2),       # XANH ĐẬM
        ]
        for value, expected in test_cases:
            with self.subTest(value=value):
                result = classify_histogram_numeric(value)
                self.assertEqual(result, expected, f"Histogram {value} phân loại sai: {result} != {expected}")

    def test_macd_m12_signal_numeric(self):
        test_cases = [
            ([-0.005, 0.03], 1),      # MUA
            ([0.005, -0.03], 0),      # BÁN
            ([0.03, 0.02], -1),       # KHÔNG
            ([0.005, 0.007], -1),     # KHÔNG
            ([0.01], -1),             # KHÔNG
        ]
        for histogram, expected in test_cases:
            with self.subTest(histogram=histogram):
                result = macd_m12_signal_numeric(histogram)
                self.assertEqual(result, expected, f"Tín hiệu sai với histogram {histogram}: {result} != {expected}")

    def test_macd_m75_or_h4_filter_numeric(self):
        test_cases = [
            (-0.05, True, True),
            (0.05, False, True),
            (0.005, True, False),
            (-0.005, False, False),
        ]
        for value, is_buy, expected in test_cases:
            with self.subTest(value=value, is_buy=is_buy):
                result = macd_m75_or_h4_filter_numeric(value, is_buy)
                self.assertEqual(result, expected, f"Filter sai với value={value}, is_buy={is_buy}: {result} != {expected}")


if __name__ == '__main__':
    unittest.main()
