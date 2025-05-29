# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging
import MetaTrader5 as mt5
import asyncio
from typing import List, Dict

from ..indicator.base import Indicator  # Base class

logger = logging.getLogger(__name__)

class Chart:
    def __init__(self, symbol: str, time_frame) -> None:
        """
        Initializes the Chart with a given symbol and time frame.

        :param symbol: Trading symbol (e.g. 'EURUSD')
        :param time_frame: Time frame constant from MetaTrader5 (e.g. mt5.TIMEFRAME_M1)
        """
        self.symbol = symbol
        self.time_frame = time_frame
        self.prices: List[Dict] = []  # Oldest first
        self.last_tick_time = 0
        self.indicators: List[Indicator] = []

    async def run_indicators(self):
        await asyncio.gather(*[
            indicator.calculate(self.prices)
            for indicator in self.indicators
        ])

    async def init_chart(self) -> bool:
        """
        Fetches the initial 100 candles and sets up the chart.

        :return bool: True if initialization succeeded
        """
        if not mt5.initialize():
            logger.exception("Please first establish connection to MetaTrader 5")
            return False

        rates = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 100)
        if rates is None or len(rates) == 0:
            logger.warning("Failed to fetch initial candle data")
            return False

        # Store in chronological order: oldest first, newest last
        self.prices = [dict(zip(r.dtype.names, r)) for r in rates]

        tick = mt5.symbol_info_tick(self.symbol)
        if tick:
            self.last_tick_time = tick.time

        await self.run_indicators()

        return True

    async def check_and_update_chart(self) -> bool:
        """
        Checks for new ticks and updates the chart. Notifies all attached indicators.

        :return bool: True if updated, False otherwise
        """
        tick = mt5.symbol_info_tick(self.symbol)
        if tick is None:
            logger.warning("Failed to retrieve tick")
            return False

        if tick.time != self.last_tick_time:
            self.last_tick_time = tick.time

            latest_candle = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 1)
            if latest_candle is None or len(latest_candle) == 0:
                logger.warning("Failed to fetch latest candle")
                return False

            new_price = dict(zip(latest_candle[0].dtype.names, latest_candle[0]))

            if not self.prices:
                self.prices = [new_price]
            elif new_price["time"] != self.prices[-1]["time"]:
                self.append_and_trim(new_price)
            else:
                self.prices[-1] = new_price  # Update current candle

            await self.run_indicators()

            return True

        return False

    def append_and_trim(self, new_price: Dict):
        """
        Appends new_price at the end of the list and trims the oldest if needed.

        :param new_price: New candle data as a dictionary
        """
        self.prices.append(new_price)

        if len(self.prices) > 100:
            self.prices.pop(0)

    def attach_indicator(self, indicator: Indicator):
        """
        Adds an indicator and updates it immediately.

        :param indicator: Any object subclassing Indicator
        """
        if indicator in self.indicators:
            logger.warning("Indicator already attached.")
            return

        self.indicators.append(indicator)
        indicator.update(self.prices)  # Initialize with current data

    def detach_indicator(self, indicator: Indicator):
        """
        Removes an indicator from the chart.

        :param indicator: An instance of an attached indicator
        """
        if indicator not in self.indicators:
            logger.warning("Indicator not found.")
            return

        self.indicators.remove(indicator)

    def get_chart(self) -> List[Dict]:
        """
        Returns current price list (oldest first).

        :return: List of candle dictionaries
        """
        return self.prices

__all__ = ("Chart",)
