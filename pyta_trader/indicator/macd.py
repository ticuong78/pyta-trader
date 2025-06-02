# pyright: reportAttributeAccessIssue=false

from ..models.price import Price

from typing import List, Optional
from .base import Indicator
from ..calculations.smoothings import calculate_ema
from ..strategy.price.close import HaCloseStrategy
from ..strategy.price.base import PriceStrategy
from ..excep.indicators.line_not_supported import LineNotSupportedError

class MACDIndicator(Indicator):
    def __init__(
        self,
        prices: List[Price] = [],
        strategy: PriceStrategy = HaCloseStrategy(),
        fast: int = 5,
        slow: int = 10,
        signal: int = 9
    ):
        """
        MACD Indicator that calculates:
        - MACD Line = EMA(fast) - EMA(slow)
        - Signal Line = EMA(MACD Line, signal period)
        - Histogram = MACD Line - Signal Line

        :param prices: Price data
        :param strategy: Strategy used to extract price (e.g. Heikin Ashi close)
        :param fast: Fast EMA period
        :param slow: Slow EMA period
        :param signal: Signal EMA period
        """
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

        fast_ema = calculate_ema(haclose, self.fast)
        slow_ema = calculate_ema(haclose, self.slow)

        self.macd_line = [
            f - s if f is not None and s is not None else None
            for f, s in (fast_ema, slow_ema)
        ]

        macd_valid = [m for m in self.macd_line if m is not None]
        signal_raw = calculate_ema(macd_valid, self.signal)
        self.signal_line = [None] * (len(self.macd_line) - len(signal_raw)) + signal_raw

        self.histogram = [
            m - s if m is not None and s is not None else None
            for m, s in (self.macd_line, self.signal_line)
        ]

        return True

    async def update(self, prices: List[Price]) -> bool:
        self.prices = prices

        return await self.calculate()
    
    def get(self, attName: str):
        if attName.lower() == "macd".lower():
            return self.macd_line
        elif attName.lower() == "signal".lower():
            return self.signal_line
        elif attName.lower() == "histogram".lower():
            return self.histogram
        else:
            raise LineNotSupportedError(f"Line {attName} is not supported")

__all__ = ("MACDIndicator",)
