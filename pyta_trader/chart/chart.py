# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging
import MetaTrader5 as mt5
import asyncio
from typing import List, Dict

from ..indicator.base import Indicator
from ..models.price import Price

logger = logging.getLogger(__name__)


def shift_append(arr: List[Dict], item: Dict, max_len: int):
    """
    Append a new item to the list. If the list exceeds max_len, remove the oldest (index 0).
    """
    arr.append(item)
    if len(arr) > max_len:
        arr.pop(0)

class Chart:
    def __init__(self, symbol: str, time_frame) -> None:
        self.symbol = symbol
        self.time_frame = time_frame
        self.prices: List[Price] = []
        self.last_tick_time = 0
        self.indicators: List[Indicator] = []

    async def run_indicators(self):
        await asyncio.gather(*[indicator.update(self.prices) for indicator in self.indicators])

    async def init_chart(self) -> bool:
        if not mt5.initialize():
            logger.exception("Please first establish connection to MetaTrader 5")
            return False

        rates = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 100)
        if rates is None or len(rates) == 0:
            logger.warning("Failed to fetch initial candle data")
            return False

        self.prices = [dict(zip(rate.dtype.names, rate)) for rate in rates]

        tick = mt5.symbol_info_tick(self.symbol)
        if tick:
            self.last_tick_time = tick.time

        await self.run_indicators()
        return True

    async def update_chart(self) -> bool:
        tick = mt5.symbol_info_tick(self.symbol)
        if not tick:
            logger.warning("Failed to retrieve tick")
            return False

        if tick.time != self.last_tick_time:
            self.last_tick_time = tick.time

            latest = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 1)
            if not latest:
                logger.warning("Failed to fetch latest candle")
                return False

            new_price = dict(zip(latest[0].dtype.names, latest[0]))

            if not self.prices:
                self.prices.append(new_price)
            elif self.prices[-1]["time"] != new_price["time"]:
                shift_append(self.prices, new_price, 100)
            else:
                self.prices[-1] = new_price

            await self.run_indicators()
            return True

        return False

    def attach_indicator(self, indicator: Indicator):
        if indicator in self.indicators:
            logger.warning("Indicator already attached.")
            return
        self.indicators.append(indicator)

    def detach_indicator(self, indicator: Indicator):
        if indicator not in self.indicators:
            logger.warning("Indicator not found.")
            return
        self.indicators.remove(indicator)

    def get_chart(self) -> List[Price]:
        return self.prices

__all__ = ("Chart",)
