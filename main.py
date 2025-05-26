# pyright: reportIndexIssue=false, reportArgumentType=false

import logging
import MetaTrader5 as mt5

from src.config import get_config 
from src.infras import init_mt5, shut_mt5
from src.chart import get_chart

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

    for symbol in symbols.keys():
        symbols[symbol] = get_chart(symbol, mt5.TIMEFRAME_M12)
        print(symbols[symbol])

except Exception as e:
    logging.exception(e)
finally:
    shut_mt5()