import unittest
import datetime
import asyncio
from datetime import timezone
from pyta.indicator.macd import MACDIndicator
from pyta.models.price import Price

class TestMACDExtended(unittest.TestCase):
    def setUp(self):
        
        prices_data = [
            100.00, 99.31, 98.62, 97.93, 97.24, 96.55, 95.86, 95.17, 94.48, 93.79,  # Giảm mạnh
            107.59, 108.97, 110.34, 111.72, 113.10, 114.48, 115.86, 117.24, 118.62, 120.00,   # Tăng mạnh → tạo bullish
            
        ]
        now = int(datetime.datetime.now(timezone.utc).timestamp())
        self.prices = [
            Price(time=now + i, open=p, high=p + 0.5, low=p - 0.5, close=p)
            for i, p in enumerate(prices_data)
        ]


        self.macd = MACDIndicator(prices=self.prices, fast=5, slow=10, signal=9)
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.macd.update(self.prices))
        print("MACD:", self.macd.macd_line[-10:])
        print("Signal:", self.macd.signal_line[-10:])
        print("Histogram:", self.macd.histogram[-10:])


    def test_output_lengths_match(self):
        self.assertEqual(len(self.macd.macd_line), len(self.prices))
        self.assertEqual(len(self.macd.signal_line), len(self.prices))
        self.assertEqual(len(self.macd.histogram), len(self.prices))

    def test_no_nan_values(self):
        self.assertTrue(all(x is None or isinstance(x, float) for x in self.macd.macd_line))
        self.assertTrue(all(x is None or isinstance(x, float) for x in self.macd.signal_line))
        self.assertTrue(all(x is None or isinstance(x, float) for x in self.macd.histogram))

    def test_latest_values_are_not_none(self):
        self.assertIsNotNone(self.macd.macd_line[-1])
        self.assertIsNotNone(self.macd.signal_line[-1])
        self.assertIsNotNone(self.macd.histogram[-1])

    def test_insufficient_data(self):
        short_prices = self.prices[:5]
        macd_short = MACDIndicator(prices=short_prices, fast=5, slow=10, signal=9)
        self.loop.run_until_complete(macd_short.update(short_prices))
        self.assertTrue(all(x is None for x in macd_short.macd_line))

    def test_macd_histogram_alignment(self):
        for macd, signal, hist in zip(self.macd.macd_line, self.macd.signal_line, self.macd.histogram):
            if macd is not None and signal is not None and hist is not None:
                self.assertAlmostEqual(hist, macd - signal, places=4)

    def test_histogram_cross_up(self):
        found = False
        for i in range(1, len(self.macd.histogram)):
            prev = self.macd.histogram[i - 1]
            curr = self.macd.histogram[i]
            if prev is not None and curr is not None:
                if prev < 0 < curr:
                    found = True
                    break
        self.assertTrue(found, "Không phát hiện giao cắt dương (bullish crossover)")

    def test_histogram_cross_down(self):
        found = False
        for i in range(1, len(self.macd.histogram)):
            prev = self.macd.histogram[i - 1]
            curr = self.macd.histogram[i]
            if prev is not None and curr is not None:
                if prev > 0 > curr:
                    found = True
                    break
        self.assertTrue(found, "Không phát hiện giao cắt âm (bearish crossover)")

    def test_macd_cross_signal_up(self):
        found = False
        for i in range(1, len(self.macd.macd_line)):
            m_prev = self.macd.macd_line[i - 1]
            s_prev = self.macd.signal_line[i - 1]
            m_curr = self.macd.macd_line[i]
            s_curr = self.macd.signal_line[i]
            if None not in (m_prev, s_prev, m_curr, s_curr):
                if m_prev < s_prev and m_curr > s_curr:
                    found = True
                    break
        self.assertTrue(found, "Không phát hiện MACD cắt lên Signal Line (bullish signal)")

    def test_macd_cross_signal_down(self):
        found = False
        for i in range(1, len(self.macd.macd_line)):
            m_prev = self.macd.macd_line[i - 1]
            s_prev = self.macd.signal_line[i - 1]
            m_curr = self.macd.macd_line[i]
            s_curr = self.macd.signal_line[i]
            if None not in (m_prev, s_prev, m_curr, s_curr):
                if m_prev > s_prev and m_curr < s_curr:
                    found = True
                    break
        self.assertTrue(found, "Không phát hiện MACD cắt xuống Signal Line (bearish signal)")
