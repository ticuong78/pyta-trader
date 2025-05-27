# pyright: reportIncompatibleMethodOverride=false

from typing import List
from .base import Indicator
from ..calculations import calculate_ema  # Your own EMA implementation

class MACDIndicator(Indicator): 
    def __init__(self, prices=None):
        super().__init__(prices or [])
        self.macd = []
        self.signal = []
        self.histogram = []

    def calculate(self, fast=5, slow=10, signal=9) -> List[float]:
        if not self.prices or len(self.prices) < slow + signal:
            return []

        # Use Heikin Ashi-style close: (open + high + low + close) / 4
        haclose = [(p["open"] + p["high"] + p["low"] + p["close"]) / 4 for p in self.prices]

        fast_ema = calculate_ema(haclose, fast)
        slow_ema = calculate_ema(haclose, slow)
        self.macd = [f - s for f, s in zip(fast_ema, slow_ema)]

        self.signal = calculate_ema(self.macd, signal)
        self.histogram = [m - s for m, s in zip(self.macd, self.signal)]

        return self.histogram

    def update(self, prices: List[dict]):
        self.prices = prices
        self.calculate()

    def latest(self):
        if not self.histogram:
            return None
        return {
            "macd": self.macd[-1],
            "signal": self.signal[-1],
            "histogram": self.histogram[-1],
        }

__all__ = ("MACDIndicator",)
