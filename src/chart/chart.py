# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging
import MetaTrader5 as mt5

from typing import List

from src.indicator.base import Indicator

logger = logging.getLogger(__name__)

class Chart:
    def __init__(self, symbol: str, time_frame) -> None:
        """
        Initializes the Chart with a given symbol and time frame.

        :param symbol: Trading symbol (e.g. 'EURUSD')
        :param time_frame: Time frame constant from MetaTrader5 (e.g. mt5.TIMEFRAME_M1)
        """
        self.prices: List[float] = []
        self.indicators: List[Indicator] = []
        self.last_tick_time = 0
        self.symbol = symbol
        self.time_frame = time_frame

    def get_chart(self):
        """
        Get current cached candles, most recent first.

        :return list: List of candle dictionaries
        """
        return self.prices

    def init_chart(self):
        """
        Fetches the initial 100 candles and sets up the chart.

        :return bool: Indicates whether initialization succeeded
        """
        if not mt5.initialize():
            logger.exception("Please first establish connection to MetaTrader 5")
            return False

        rates = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 100)
        if rates is None or len(rates) == 0:
            logger.warning("Failed to fetch initial candle data")
            return False

        self.prices = [dict(zip(r.dtype.names, r)) for r in reversed(rates)]
        tick = mt5.symbol_info_tick(self.symbol)
        if tick:
            self.last_tick_time = tick.time

        return True

    def check_and_update_chart(self):
        """
        Checks for new ticks and updates the latest candle data accordingly.

        :return bool: True if an update occurred, otherwise False
        """
        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            logger.warning("Failed to retrieve tick")
            return False

        if tick.time != self.last_tick_time:
            self.last_tick_time = tick.time

            latest_candle = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 1)
            if latest_candle and len(latest_candle) > 0:
                latest = dict(zip(latest_candle[0].dtype.names, latest_candle[0]))

                if not self.prices:
                    self.prices = [latest]
                    return True

                if latest["time"] != self.prices[0]["time"]:
                    self.shift_down_and_append(latest)
                else:
                    self.prices[0] = latest

            return True

        return False

    def shift_down_and_append(self, new_price):
        """
        Shifts the existing prices down and adds new_price at the top.

        :param new_price: A dictionary representing the latest candle
        """
        if not self.prices:
            self.prices = [new_price]
        else:
            self.prices = [new_price] + self.prices[:-1]
    
    def attach_indicator(self, indicator: Indicator):
        if indicator in self.indicators or Indicator is None:
            logger.warning("Indicator already attached or None. Please check!")
            return

        self.indicators.append(indicator)
        
    def detach_indicator(self, indicator: Indicator):
        if indicator not in self.indicators:
            logger.warning("Indicator not attached. Please check!")
            return

        self.indicators.remove(indicator)
    
__all__ = ("Chart",)
