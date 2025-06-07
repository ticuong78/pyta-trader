# pyright: reportAttributeAccessIssue=false

from typing import List
from ..models.price import Price
from ..calculations.smoothings import calculate_ema
from ..strategy.price.close import HaCloseStrategy
from ..strategy.price.base import PriceStrategy
from ..excep.indicators.line_not_supported import LineNotSupportedError
from .base import Indicator

class MACDIndicator(Indicator):
    def __init__(
        self,
        prices: List[Price] = [],
        strategy: PriceStrategy = HaCloseStrategy(),
        fast: int = 5,
        slow: int = 10,
        signal: int = 9
    ):
        super().__init__(prices)
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.strategy = strategy

        self.macd_line: List[float] = []
        self.signal_line: List[float] = []
        self.histogram: List[float] = []

    async def _calculate(self) -> bool:
        if not self.prices or len(self.prices) < self.slow + self.signal:
            return False

        haclose = [self.strategy.calculate(p) for p in self.prices]

        fast_ema = calculate_ema(haclose, self.fast, pad=False)
        slow_ema = calculate_ema(haclose, self.slow, pad=False)

        min_len = min(len(fast_ema), len(slow_ema))
        fast_ema = fast_ema[-min_len:]
        slow_ema = slow_ema[-min_len:]

        macd_raw = [f - s for f, s in zip(fast_ema, slow_ema)]
        if not macd_raw or len(macd_raw) < self.signal:
            return False

        signal_raw = calculate_ema(macd_raw, self.signal, pad=False)
        signal_pad = [None] * (len(macd_raw) - len(signal_raw)) + signal_raw

        histogram_raw = [
            m - s if m is not None and s is not None else None
            for m, s in zip(macd_raw, signal_pad)
        ]

        total_pad = len(self.prices) - len(macd_raw)
        self.macd_line = [None] * total_pad + macd_raw
        self.signal_line = [None] * total_pad + signal_pad
        self.histogram = [None] * total_pad + histogram_raw

        return True

    async def update(self, prices: List[Price]) -> bool:
        self.prices = prices
        return await self._calculate()

    def get(self, line: str):
        if line.lower() == "macd":
            return self.macd_line
        elif line.lower() == "signal":
            return self.signal_line
        elif line.lower() == "histogram":
            return self.histogram
        else:
            raise LineNotSupportedError(f"Line {line} is not supported")

    def get_latest_valid(self, line: str):
        data = self.get(line)
        for x in reversed(data):
            if x is not None:
                return x
        return None

__all__ = ("MACDIndicator",)
