from typing import List
from abc import ABC, abstractmethod

class Indicator(ABC):
    def __init__(self, prices: List[dict]):
        """
        Insert prices into instance and save it for future calculations

        :param prices: List of price dictionaries
        """
        self.prices = prices or []

    @abstractmethod
    def latest(self):
        """
        Get the latest calculated value of the indicator.

        :return any: any type of value
        """
        pass

    @abstractmethod
    def calculate(self) -> List[float]:
        """
        Calculate the indicator — each subclass defines its formula.

        :return List[float]: List of calculated values
        """
        pass

    @abstractmethod
    def update(self, prices: List[dict]):
        """
        Update prices and re-calculate the indicator values.
        Every subclass must implement this to handle incoming price updates.

        :param prices: New list of price dictionaries
        """
        pass

    def __eq__(self, other):
        return isinstance(other, Indicator)

__all__ = ("Indicator",)
