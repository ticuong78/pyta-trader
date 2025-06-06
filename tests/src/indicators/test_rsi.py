import unittest
import math
import random
import time

# Thay đường dẫn import cho phù hợp project của bạn
from pyta.calculations.smoothings import calculate_rsi


class TestCalculateRSI(unittest.TestCase):
    """Test suite đầy đủ cho hàm calculate_rsi (Wilder RSI)."""

    # ----------  Nhóm ca gốc  -------------------------------------------------

    def test_too_few_prices(self):
        prices = [100, 101, 102]      # < period
        period = 14
        self.assertEqual(
            calculate_rsi(prices, period),
            [None] * len(prices)
        )

    def test_all_gains(self):
        prices = list(range(1, 30))
        period = 14
        rsi = calculate_rsi(prices, period)
        self.assertTrue(all(x is None for x in rsi[:period]))
        self.assertTrue(all(x == 100 for x in rsi[period:]))

    def test_all_losses(self):
        prices = list(range(30, 0, -1))
        period = 14
        rsi = calculate_rsi(prices, period)
        self.assertTrue(all(x is None for x in rsi[:period]))
        self.assertTrue(all(x == 0 for x in rsi[period:]))

    def test_mixed_prices_simple(self):
        prices = [
            44.34, 44.09, 44.15, 43.61, 44.33,
            44.83, 45.10, 45.42, 45.84, 46.08,
            45.89, 46.03, 45.61, 46.28, 46.28,
            46.00, 46.03, 46.41, 46.22, 45.64,
        ]
        period = 14
        expected_first_rsi = 70.46    # Wilder’s book
        rsi = calculate_rsi(prices, period)
        self.assertTrue(math.isclose(rsi[period], expected_first_rsi, rel_tol=1e-2))
        self.assertTrue(all(v is not None for v in rsi[period:]))

    def test_no_mutation(self):
        prices = list(range(1, 16))
        period = 14
        original = prices.copy()
        _ = calculate_rsi(prices, period)
        self.assertEqual(prices, original)

    # ----------  Ca kiểm thử mở rộng  ----------------------------------------

    def test_constant_prices(self):
        """Giá không đổi ⇒ gain = loss = 0 ⇒ RSI = 100 theo công thức hiện tại."""
        prices = [50.0] * 30
        period = 14
        rsi = calculate_rsi(prices, period)
        self.assertTrue(all(x is None for x in rsi[:period]))
        self.assertTrue(all(x == 100 for x in rsi[period:]))

    def test_period_equals_length(self):
        """Nếu period == len(prices) ➜ vẫn trả về toàn None (không có SMA)."""
        prices = [10, 11, 12, 13]
        period = len(prices)
        self.assertEqual(
            calculate_rsi(prices, period),
            [None] * len(prices)
        )

    def test_period_one(self):
        """
        period = 1 là biên đặc biệt: RSI = 100 khi tăng, 0 khi giảm,
        vì Wilder smoothing rút về giá trị delta hiện tại.
        """
        prices = [1, 2, 3, 2, 3, 4, 3]
        period = 1
        expected = [None, 100, 100, 0, 100, 100, 0]
        self.assertEqual(calculate_rsi(prices, period), expected)

    def test_random_prices_value_range(self):
        """Giá ngẫu nhiên ⇒ mọi RSI hợp lệ ∈ [0,100] (sau phần None)."""
        random.seed(42)
        prices = [100 + random.uniform(-5, 5) for _ in range(200)]
        period = 14
        rsi = calculate_rsi(prices, period)

        # Check chiều dài và None prefix
        self.assertEqual(len(rsi), len(prices))
        self.assertTrue(all(x is None for x in rsi[:period]))

        # Giá trị hợp lệ nằm trong 0..100
        for val in rsi[period:]:
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 100)

    def test_large_dataset_performance(self):
        """
        Bộ dữ liệu rất lớn (≥ 100k) vẫn chạy nhanh (< 0.5 s trên máy bình thường).
        Không đo chính xác hiệu năng nhưng đảm bảo không quá chậm/treo.
        """
        prices = list(range(1, 120_001))          # 120 000 điểm giá
        period = 14
        start = time.perf_counter()
        _ = calculate_rsi(prices, period)
        duration = time.perf_counter() - start
        self.assertLess(duration, 0.5, f"Chạy quá chậm: {duration:.3f}s")

    def test_rsi_monotonic_segments(self):
        """
        Tạo 3 đoạn: giảm mạnh ▸ đi ngang ▸ tăng mạnh.
        Kỳ vọng: RSI tăng dần qua từng đoạn.
        """
        prices = (
            list(range(200, 100, -1)) +   # giảm
            [100] * 20 +                  # đi ngang
            list(range(100, 201))         # tăng
        )
        period = 14
        rsi = calculate_rsi(prices, period)

        first_rsi = rsi[period]           # thuộc đoạn giảm ➜ thấp
        mid_rsi = rsi[len(prices)//2]     # đoạn đi ngang
        last_rsi = rsi[-1]                # đoạn tăng ➜ cao

        self.assertLess(first_rsi, mid_rsi)
        self.assertLess(mid_rsi, last_rsi)

    # ------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main(verbosity=2)
