# pyright: reportIncompatibleMethodOverride=false

from typing import List
from .base import Indicator
from ..calculations.smoothings import calculate_ema
from ..strategy.price.ha_close import HaCloseStrategy

class MACDIndicator(Indicator): 
    def __init__(self, prices=None, strategy=HaCloseStrategy(), fast=5, slow=10, signal=9):
        super().__init__(prices or [])
        self.slow = slow
        self.fast = fast
        self.signal = signal
        self._histogram: List[float] = []
        self.strategy = strategy

    async def calculate(self) -> bool:
        if not self.prices or len(self.prices) < self.slow + self.signal:
            return False

        # Heikin Ashi-style close
        haclose = [
            self.strategy.calculate(p)
            for p in self.prices
        ]

        fast_ema = calculate_ema(haclose, self.fast)
        slow_ema = calculate_ema(haclose, self.slow)

        macd_line = [
            f - s if f is not None and s is not None else None
            for f, s in zip(fast_ema, slow_ema)
        ]

        signal_line = calculate_ema([m for m in macd_line if m is not None], self.signal)
        signal_line_full = [None] * (len(macd_line) - len(signal_line)) + signal_line

        self._histogram = [
            m - s if m is not None and s is not None else None
            for m, s in zip(macd_line, signal_line_full)
        ]

        return True

    async def update(self, prices: List[dict]):
        self.prices = prices
        return await self.calculate()

    def latest(self):
        return next((v for v in reversed(self._histogram) if v is not None), None)

    @property
    def histogram(self) -> List[float]:
        return [v for v in self._histogram if v is not None]

__all__ = ("MACDIndicator",)
