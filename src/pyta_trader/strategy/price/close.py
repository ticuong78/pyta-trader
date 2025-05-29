from .base import PriceStrategy

class CloseStrategy(PriceStrategy):
    def calculate(self, candle):
        return candle["close"]

__all__ = ("CloseStrategy",)