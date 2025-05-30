from ...models.price import Price

class PriceStrategy:
    def calculate(self, candle: Price) -> float:
        raise NotImplementedError()

__all__ = ("PriceStrategy", )