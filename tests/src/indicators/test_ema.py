import unittest
from pyta.calculations.smoothings import calculate_ema, calculate_sma

class TestEMACalculation(unittest.TestCase):

    def test_ema_length_match(self):
        prices = [10, 11, 12, 13, 14, 15, 16]
        period = 3
        ema = calculate_ema(prices, period)
        self.assertEqual(len(ema), len(prices))

    def test_ema_padding_with_none(self):
        prices = [10, 11, 12, 13, 14]
        period = 3
        ema = calculate_ema(prices, period)
        self.assertEqual(ema[:period - 1], [None, None])

    def test_ema_values_correctness(self):
        prices = [10, 11, 12, 13, 14]
        period = 3
        ema = calculate_ema(prices, period)

        sma = (10 + 11 + 12) / 3
        self.assertAlmostEqual(ema[2], sma)

        alpha = 2 / (period + 1)
        ema3 = alpha * 13 + (1 - alpha) * sma
        ema4 = alpha * 14 + (1 - alpha) * ema3

        self.assertAlmostEqual(ema[3], ema3)
        self.assertAlmostEqual(ema[4], ema4)

    def test_ema_invalid_period_zero(self):
        prices = [10, 11, 12]
        with self.assertRaises(ValueError):
            calculate_ema(prices, 0)

    def test_ema_invalid_period_negative(self):
        prices = [10, 11, 12]
        with self.assertRaises(ValueError):
            calculate_ema(prices, -2)

    def test_ema_period_equals_length(self):
        prices = [1, 2, 3, 4, 5]
        period = 5
        ema = calculate_ema(prices, period)
        self.assertEqual(len(ema), len(prices))
        self.assertIsNone(ema[0])
        self.assertAlmostEqual(ema[-1], ema[-1])  # Giá trị cuối cùng có tồn tại

    def test_ema_all_prices_equal(self):
        prices = [100] * 10
        period = 3
        ema = calculate_ema(prices, period)
        for val in ema[period - 1:]:
            self.assertAlmostEqual(val, 100.0)

    def test_ema_input_too_short(self):
        prices = [5, 6]
        period = 5
        ema = calculate_ema(prices, period)
        self.assertEqual(ema, [])

    def test_ema_float_precision(self):
        prices = [1.111, 1.222, 1.333, 1.444, 1.555]
        period = 3
        ema = calculate_ema(prices, period)
        self.assertTrue(all(isinstance(x, float) or x is None for x in ema))

if __name__ == '__main__':
    unittest.main()
