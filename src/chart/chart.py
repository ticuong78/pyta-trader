# pyright: reportIndexIssue=false, reportAttributeAccessIssue=false

import logging

import MetaTrader5 as mt5

from config import get_config
from infras import init_mt5, shut_mt5

logger = logging.getLogger(__name__)

def get_chart(symbol, timeframe):
    if not mt5.initialize():
        logger.exception("Establish connection to Meta Trader first!")
        return

