from .base import PriceStrategy

class HaCloseStrategy(PriceStrategy):
    def calculate(self, candle):
        return (candle["open"] + candle["high"] + candle["low"] + candle["close"]) / 4

class CloseStrategy(PriceStrategy):
    def calculate(self, candle):
        return candle["close"]

__all__ = (
    "CloseStrategy",
    "HaCloseStrategy",
)