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

        # Tính EMA nhanh và chậm, đã pad sẵn, không có None
        fast_ema = calculate_ema(haclose, self.fast, pad=True)
        slow_ema = calculate_ema(haclose, self.slow, pad=True)

        # Tính MACD
        macd_line = [round(f - s, 3) for f, s in zip(fast_ema, slow_ema)]

        # Tính Signal line (EMA của MACD line)
        signal_line = calculate_ema(macd_line, self.signal, pad=True)

        # Tính histogram
        histogram = [round(m - s, 3) for m, s in zip(macd_line, signal_line)]

        # Gán kết quả
        self.macd_line = macd_line
        self.signal_line = signal_line
        self.histogram = histogram

        return True

    async def update(self, prices: List[Price]) -> bool:
        self.prices = prices
        return await self._calculate()

    def get(self, line: str):
        line = line.lower()
        if line == "macd":
            return self.macd_line
        elif line == "signal":
            return self.signal_line
        elif line == "histogram":
            return self.histogram
        else:
            raise LineNotSupportedError(f"Line {line} is not supported")

__all__ = ("MACDIndicator",)
