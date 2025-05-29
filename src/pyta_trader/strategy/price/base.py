class PriceStrategy:
    def calculate(self, candle: dict) -> float:
        raise NotImplementedError()

__all__ = ("PriceStrategy", )