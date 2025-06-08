from typing import List, Optional
from ..models.price import Price
from ..strategy.price.base import PriceStrategy
from ..strategy.price.close import HaCloseStrategy
from .base import Indicator
from pyta.excep.indicators.line_not_supported import LineNotSupportedError
from ..calculations.smoothings import calculate_sma

def calculate_rsi(prices, period):
    if len(prices) <= period:
        return [None] * len(prices)

    rsi = [None] * len(prices)

    # Tính delta
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [max(delta, 0) for delta in deltas]
    losses = [abs(min(delta, 0)) for delta in deltas]

    # Trung bình ban đầu (SMA)
    avg_gain = calculate_sma(gains, period)
    avg_loss = calculate_sma(losses, period)

    rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
    rsi[period] = 100 - (100 / (1 + rs))

    # Wilder’s smoothing cho các ngày tiếp theo
    for i in range(period, len(deltas)):
        gain = gains[i]
        loss = losses[i]

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            rsi_value = 100
        elif avg_gain == 0:
            rsi_value = 0
        else:
            rs = avg_gain / avg_loss
            rsi_value = 100 - (100 / (1 + rs))

        rsi[i + 1] = rsi_value  # dịch chỉ số để đúng với prices

    return rsi

class RSIIndicator(Indicator):
    def __init__(
        self,
        prices: List[Price] = [],
        strategy: PriceStrategy = HaCloseStrategy(),
        period: int = 14
    ):
        
        """
        RSI Indicator (Wilder)
        """
        
        super().__init__(prices)
        self.strategy = strategy
        self.period = period
    
        self.rsi_line: List[float] = []
    
    async def _calculate(self) -> bool:
        if self.prices is None or len(self.prices) < self.slow + self.signal:
            return False
        
        closes_prices = [self.strategy.calculate(p) for p in self.prices]
        self.rsi_line = calculate_rsi(closes_prices, self.period)
        
        return True

    async def update(self, prices: List[Price]) -> bool:
        self.prices = prices
        
        return await self._calculate()

    def get(self, attName: str):
        if attName.lower() == "rsi".lower():
            return self.rsi
        raise LineNotSupportedError(f"Line {attName} is not supported")

__all__ = ("RSIIndicator",)