# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging
import numpy as np
import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

class Chart:
    def __init__(self, symbol: str, time_frame) -> None:
        """
        :param symbol: Symbol to get
        :param time_frame: Time frame to get
        """
        self.prices = np.array([], dtype=object)
        self.last_time = 0
        self.symbol = symbol
        self.time_frame = time_frame

    def get_chart(self):
        """
        Call this function initially to get first 100 candles from the zero point

        :return array: arrays of mt5's price objects
        """
        if not mt5.initialize():
            logger.exception("Please first establish connection to Meta Trader")
            return None

        rates = mt5.copy_rates_from_pos(
            self.symbol, self.time_frame,
            0, 100
        )

        if rates is None or len(rates) == 0:
            logger.warning("Something has gone wrong...")
            return None

        self.prices = rates
        self.last_time = rates[-1][0]
        return self.prices
    
    def renew_chart(self):
        """
        To renew chart and update prices. Call this function after you get 
        your required number of candles (use **get_chart**)

        :return: Updated price array if updated, else original price array
        """
        if not mt5.initialize():    
            logger.exception("Please first establish connection to Meta Trader")
            return self.prices

        last_tick = mt5.symbol_info_tick(self.symbol)

        if last_tick is None:
            logger.warning("Failed to retrieve last tick")
            return self.prices

        if last_tick.time != self.last_time:
            rates = mt5.copy_rates_from_pos(
                self.symbol, self.time_frame,
                0, 1 
            )
            if rates is not None and len(rates) > 0:
                self.last_time = rates[-1][0]
                self.shift_down_and_append(rates[0])
        return self.prices

    def shift_down_and_append(self, new_price):
        """
        Efficiently shift prices down by 1 and add new_price at the start.
        Keeps the array size constant.

        :param new_price: New price you want to add
        """
        if self.prices is None or len(self.prices) == 0:
            self.prices = np.array([new_price])
        else:
            self.prices[1:] = self.prices[:-1]  
            self.prices[0] = new_price

__all__ = ("Chart",)
