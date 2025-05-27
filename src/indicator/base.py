from typing import List, number

from abc import ABC, abstractmethod

class Indicator(ABC):
    @abstractmethod
    def __init__ (self, prices):
        """
        Insert prices into instance and save it for furture calculations
        
        :param prices: list of prices (numbers)
        """
        
        self.prices = prices
    
    @abstractmethod
    def calculate() -> List[number]:
        """
        Calculate the indicator, each indicator has its own calculation method and formulas
        
        :return List[number]: List of calculated values
        """
        pass
    
__all__ = (
    "Indicator",
)