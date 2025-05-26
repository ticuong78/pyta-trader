# pyright: reportAttributeAccessIssue=false

import logging

import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

def init_mt5(
        path: str, login: int, 
        passw: str, server: str
    ):
    """
    Create connection to Meta Trader's platform

    :param path: path to your Meta Trader's terminal execution
    :param login: your Meta Trader's account login integer
    :param passw: your Meta Trader's account password
    :param server: your Meta Trader's account server

    :return bool: indicates whether establising process is successful
    """

    if not mt5.initialize(
        path, login,
        passw, server
    ):
        logger.exception("Cannot connect to MetaTrader 5 platform. Check your information")
        return False

    print("Successfully established connection with Meta Trader 5 platform, ready to trade!")
    return True

def shut_mt5():
    mt5.shutdown()

__all__ = (
    "init_mt5",
    "shut_mt5",
)