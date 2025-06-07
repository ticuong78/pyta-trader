import unittest
import asyncio
from datetime import datetime, timedelta

from pyta.models.price import Price
from pyta.indicator.macd import MACDIndicator



class TestExtendedMACDIndicator(unittest.TestCase):
    def _generate_prices(self, values):
        """Helper để tạo danh sách Price từ danh sách giá đóng cửa"""
        base_time = datetime.now()
        return [
            Price(
                time=int((base_time + timedelta(days=i)).timestamp()),
                open=p,
                high=p + 1,
                low=p - 1,
                close=p,
            )
            for i, p in enumerate(values)
        ]

    def test_macd_with_flat_market(self):
        """MACD và Histogram gần 0 khi giá đi ngang"""
        prices = self._generate_prices([100] * 30)
        indicator = MACDIndicator()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(indicator.update(prices))

        macd = indicator.get_latest_valid("macd")
        signal = indicator.get_latest_valid("signal")
        hist = indicator.get_latest_valid("histogram")
        print("Flat Market:", macd, signal, hist)

        self.assertAlmostEqual(macd, signal, delta=0.01)
        self.assertAlmostEqual(hist, 0, delta=0.01)

    def test_macd_with_trend_shift(self):
        """Histogram chuyển từ dương sang âm thể hiện đảo chiều xu hướng"""
        prices = self._generate_prices([i for i in range(20)] + [20 - i for i in range(20)])
        indicator = MACDIndicator()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(indicator.update(prices))

        hist = indicator.histogram
        nones_removed = [x for x in hist if x is not None]
        crosses = [
            i for i in range(1, len(nones_removed))
            if nones_removed[i - 1] * nones_removed[i] < 0
        ]
        print("Crossover indices:", crosses)
        self.assertTrue(len(crosses) >= 1)

    def test_macd_with_short_data(self):
        """Không tính MACD khi dữ liệu chưa đủ"""
        prices = self._generate_prices([1, 2, 3])  # quá ngắn
        indicator = MACDIndicator()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(indicator.update(prices))
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
