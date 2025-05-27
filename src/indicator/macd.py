from typing import Tuple, List, number

from .base import Indicator
from ..calculations import calculate_ema

class MACDIndicator(Indicator): 
    def __init__ (self, prices):
        super().__init__(prices)
        self.macd = []
        self.signal = []
        self.histogram = []

    def calculate(self, prices, fast=5, slow=10, signal=9) -> Tuple[List[number], List[number], List[number]]:
        """
        Calculate MACD based on passed arguments

        Args:
            prices (_type_): prices array
            fast (int, optional): fast period. Defaults to 5.
            slow (int, optional): slow period. Defaults to 10.
            signal (int, optional): signalling period. Defaults to 9.

        Returns:
            Tuple[List[number], List[number], List[number]]: macd, signal, histogram
        """
        fast_ema = self.calculate_ema(prices, fast)
        slow_ema = self.calculate_ema(prices, slow)
        macd = [f - s for f, s in zip(fast_ema, slow_ema)]
        signal_line = self.calculate_ema(macd, signal)
        histogram = [m - s for m, s in zip(macd, signal_line)]
        
        return macd, signal_line, histogram
    
__all__ = (
    "MACDIndicator",
)