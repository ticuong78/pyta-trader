# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging

import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

def get_chart(symbol, timeframe):
    """
    Give prices of symbol and timeframe if found

    :param symbol: symbol to get
    :param timeframe: timeframe to get
    :return array: arrays of mt5's price objects
    """
    if not mt5.initialize():
        logger.exception("Please first establish connection to Meta Trader")
        return

    rates = mt5.copy_rates_from_pos(
        symbol, timeframe,
        0, 100
    )

    if len(rates) == 0:
        print("Something has gone wrong...")
        return None

    return rates

__all__ = (
    "get_chart",
)