from typing import List
from abc import ABC, abstractmethod
from ..models.price import Price

class Indicator(ABC):
    def __init__(self, prices: List[Price]):
        """
        Base class for all technical indicators.
        Derived classes must manage their own computed result fields.

        :param prices: List of price dictionaries (usually OHLC or OHLCV)
        """
        self.prices: List[Price] = prices or []

    @abstractmethod
    async def _calculate(self) -> bool:
        """
        Calculate indicator values from `self.prices`.
        Each subclass defines its own output structure.

        :return Any: Depends on indicator type — could be list, dict, tuple, etc.
        """
        pass

    @abstractmethod
    async def update(self, prices: List[Price]) -> bool:
        """
        Update the internal price data and re-calculate the indicator.

        :param prices: New list of price dictionaries
        """
        pass

    @abstractmethod
    def get(self, attName: str) -> List[float]:
        pass

    def __eq__(self, other):
        """
        Equality comparison — two indicators are equal if they're of the same type.
        Can be overridden for more specific comparisons.
        """
        return isinstance(other, self.__class__)


__all__ = ("Indicator",)
