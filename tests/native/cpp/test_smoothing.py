import unittest
import math
from native.cpp.smoothing_cpp import calculate_ema, calculate_sma

class TestSmoothingCpp(unittest.TestCase):
    def test_calculate_sma_normal(self):
        prices: list[float] = [1, 2, 3, 4, 5]
        period = 3
        expected = sum(prices[:period]) / period
        result = calculate_sma(prices, period)
        self.assertTrue(math.isclose(result, expected, rel_tol=1e-9))

    def test_calculate_sma_period_larger_than_data(self):
        prices: list[float] = [1, 2]
        period = 3
        result = calculate_sma(prices, period)
        self.assertEqual(result, 0.0, "Expected 0.0 when period > len(prices)")

    def test_calculate_sma_invalid_period(self):
        prices: list[float] = [1, 2, 3]
        result = calculate_sma(prices, 0)
        self.assertEqual(result, 0.0, "Expected 0.0 when period <= 0")

    def test_calculate_ema_normal(self):
        prices: list[float] = [1, 2, 3, 4, 5]
        period = 3
        ema = calculate_ema(prices, period)

        self.assertEqual(len(ema), len(prices))
        for i in range(period - 1):
            self.assertTrue(math.isnan(ema[i]))
        self.assertTrue(math.isclose(ema[period - 1], calculate_sma(prices, period), rel_tol=1e-9))

    def test_calculate_ema_insufficient_data(self):
        prices: list[float] = [1]
        period = 3
        ema = calculate_ema(prices, period)
        self.assertEqual(len(ema), len(prices))
        self.assertTrue(all(math.isnan(val) for val in ema), "EMA should be NaN when data insufficient")

    def test_calculate_ema_invalid_period(self):
        prices: list[float] = [1, 2, 3, 4]
        period = 0
        ema = calculate_ema(prices, period)
        self.assertEqual(len(ema), len(prices))
        self.assertTrue(all(math.isnan(val) for val in ema))

    def test_calculate_ema_large_values(self):
        prices: list[float] = [1e10, 1e10 + 1, 1e10 + 2, 1e10 + 3]
        period = 2
        ema = calculate_ema(prices, period)
        self.assertEqual(len(ema), len(prices))
        self.assertTrue(math.isnan(ema[0]))
        self.assertTrue(math.isclose(ema[1], calculate_sma(prices[:2], 2), rel_tol=1e-9))

if __name__ == "__main__":
    unittest.main()
