# pyright: reportIndexIssue=false, reportArgumentType=false, reportAttributeAccessIssue=false

"""
This is an example of how to establish connection to Meta Trader 5
"""

import logging
import MetaTrader5 as mt5

from src.pyta_trader.config import get_config 
from src.pyta_trader.infras import init_mt5, shut_mt5
from src.pyta_trader.indicator.macd import MACDIndicator
from src.pyta_trader.chart import Chart

logger = logging.getLogger(__name__)

symbols = {
    "XAUUSD_m": [], 
    "BTCUSD_m": []
}

try:
    config = get_config()

    # print(config.mt5_path)

    init_mt5(
        config.mt5_path,
        config.mt5_login,
        config.mt5_passw,
        config.mt5_server,
    )

    chart = Chart("BTCUSD_m", mt5.TIMEFRAME_M12)
    macd = MACDIndicator()
    chart.attach_indicator(macd)

except Exception as e:
    logging.exception(e)
finally:
    shut_mt5()