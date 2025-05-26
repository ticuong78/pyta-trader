# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging

import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

class Chart:
    last_time = 0
    prices = []

    def __init__(self, symbol, time_frame) -> None:
        self.symbol = symbol
        self.time_frame = time_frame

    def get_chart(self):
        """
        Give prices of symbol and timeframe if they are found

        :return array: arrays of mt5's price objects
        """
        return self.prices

    def _renew_chart(self):
        """
        Renew chart with new symbol's values
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
    
    def renew_chart(self):
        """
        Renew chart when new tick comes
        """
        last_tick = mt5.symbol_info_tick(self.symbol)

        if last_tick.time != self.last_time:
            self._renew_chart()

__all__ = (
    "Chart",
)