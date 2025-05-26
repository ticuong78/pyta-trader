# pyright: reportAttributeAccessIssue=false

import logging

import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

def init_mt5(
        path: str, login: int, 
        passw: str, server: str
    ):
    if not mt5.initialize(
        path, login,
        passw, server
    ):
        logger.exception("Cannot connect to MetaTrader 5 platform. Check your information")
        return

    print("Successfully established connection with Meta Trader 5 platform, ready to trade!")

def shut_mt5():
    mt5.shutdown()

__all__ = (
    "init_mt5",
    "shut_mt5",
)