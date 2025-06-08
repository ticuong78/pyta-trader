from abc import ABC, abstractmethod
from ...models.price import Price

class PriceStrategy(ABC):
    @abstractmethod
    def calculate(self, candle: Price) -> float:
        raise NotImplementedError()

__all__ = ("PriceStrategy", )