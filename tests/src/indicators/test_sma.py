import unittest
from pyta.calculations.smoothings import calculate_sma

class TestSMACalculation(unittest.TestCase):
    
    def test_basic_sma(self):
        self.assertEqual(calculate_sma([1, 2, 3], 3), 2.0)

    def test_longer_series(self):
        self.assertEqual(calculate_sma([10, 20, 30, 40], 3), 20.0)

    def test_exact_period(self):
        self.assertEqual(calculate_sma([5, 10, 15], 3), 10.0)

    def test_short_series(self):
        self.assertIsNone(calculate_sma([1, 2], 3))

    def test_empty_series(self):
        self.assertIsNone(calculate_sma([], 3))

    def test_zero_period(self):
        self.assertIsNone(calculate_sma([1, 2, 3], 0))

    def test_period_one(self):
        self.assertEqual(calculate_sma([42], 1), 42.0)

    def test_floats(self):
        self.assertEqual(calculate_sma([1.5, 2.5, 3.0], 3), 2.333)

if __name__ == '__main__':
    unittest.main()
