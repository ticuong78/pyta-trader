from typing import List, Dict, Any
from abc import ABC, abstractmethod


class Indicator(ABC):
    def __init__(self, prices: List[dict]):
        """
        Base class for all technical indicators.
        Derived classes must manage their own computed result fields.

        :param prices: List of price dictionaries (usually OHLC or OHLCV)
        """
        self.prices: List[Dict[str, Any]] = prices or []

    @abstractmethod
    def calculate(self) -> Any:
        """
        Calculate indicator values from `self.prices`.
        Each subclass defines its own output structure.

        :return Any: Depends on indicator type — could be list, dict, tuple, etc.
        """
        pass

    @abstractmethod
    def update(self, prices: List[Dict[str, Any]]):
        """
        Update the internal price data and re-calculate the indicator.

        :param prices: New list of price dictionaries
        """
        pass

    @abstractmethod
    def latest(self) -> Any:
        """
        Return the most recent indicator value(s).

        :return Any: Depends on indicator type — e.g., last MACD histogram value
        """
        pass

    def shift_append(self, arr: List[Any], value: Any, max_len: int = 100):
        """
        Append a value to a list and keep only the last `max_len` elements.

        :param arr: Target list
        :param value: Value to append
        :param max_len: Maximum number of elements allowed
        """
        arr.append(value)
        if len(arr) > max_len:
            arr.pop(0)

    def __eq__(self, other):
        """
        Equality comparison — two indicators are equal if they're of the same type.
        Can be overridden for more specific comparisons.
        """
        return isinstance(other, self.__class__)


__all__ = ("Indicator",)
