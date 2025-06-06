from typing import List, Optional
from ..models.price import Price
from ..strategy.price.base import PriceStrategy
from ..strategy.price.close import HaCloseStrategy
from .base import Indicator
from ..calculations.smoothings import calculate_rsi
from pyta.excep.indicators.line_not_supported import LineNotSupportedError


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
    
        self.rsi_line: list[float] = []
        
    # pass
    
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