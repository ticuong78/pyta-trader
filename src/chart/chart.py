# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

# price object:
#           time: seconds from 1970
#           open: open price
#           high: highest price
#           low: lowest price
#           close: close price
#           tick_volume: no care
#           spread: no care
#           real_volume: no care

import logging

import numpy as np
import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

class Chart:
    def __init__(self, symbol: str, time_frame) -> None:
        """
        :param symbol: Symbol to get
        :param time_frame: time frame to get
        """
        self.prices = []
        self.last_time = 0
        self.symbol = symbol
        self.time_frame = time_frame

    def get_chart(self):
        """
        Give prices of symbol and timeframe if they are found

        :return array: arrays of mt5's price objects
        """
        if not mt5.initialize():
            logger.exception("Please first establish connection to Meta Trader")
            return

        rates = mt5.copy_rates_from_pos(
            self.symbol, self.time_frame,
            0, 100
        )

        self.prices = rates

        if len(rates) == 0:
            print("Something has gone wrong...")
            return None

        self.last_time = rates[-1][0]

        return rates
    
    def renew_chart(self):
        """
        Renew chart only when a new tick comes in
        """
        if not mt5.initialize():
            logger.exception("Please first establish connection to Meta Trader")
            return

        last_tick = mt5.symbol_info_tick(self.symbol)

        if last_tick.time != self.last_time:
            rates = mt5.copy_rates_from_pos(
                self.symbol, self.time_frame,
                0, 1 
            )
            if rates is not None and len(rates) > 0:
                self.last_time = rates[-1][0]
                self.shift_down_and_append(rates[0])

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



__all__ = (
    "Chart",
)