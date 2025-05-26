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
        self.last_tick_time = 0
        self.symbol = symbol
        self.time_frame = time_frame

    def get_chart(self):
        """
        Get candles (most recent first)

        :return array: arrays of mt5's price objects
        """
        return self.prices

    def init_chart(self):
        """
        Call this function initially to get first 100 candles from the zero point

        :return bool: indicates whether the process is success or not
        """
        if not mt5.initialize():
            logger.exception("Please first establish connection to Meta Trader")
            return False

        rates = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 100)

        if rates is None or len(rates) == 0:
            logger.warning("Something has gone wrong...")
            return False

        # Reverse to make most recent first
        self.prices = rates[::-1]
        self.last_tick_time = mt5.symbol_info_tick(self.symbol).time if mt5.symbol_info_tick(self.symbol) else 0

        return True

    def check_and_update_chart(self):
        """
        Check for new candles or new values and update the chart

        :return bool: indicates whether the process is success or not
        """
        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            logger.warning("Failed to get tick")
            return False

        if tick.time != self.last_tick_time:
            self.last_tick_time = tick.time

            latest_candle = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 1)

            if latest_candle and len(latest_candle) > 0:
                latest = latest_candle[0]
                if latest[0] != self.prices[0][0]:
                    self.shift_down_and_append(latest)
                else:
                    self.prices[0] = latest

            return True

        return False  # No new tick

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
