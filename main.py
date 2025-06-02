import logging
import MetaTrader5 as mt5

from .pyta_trader.chart import Chart
from .pyta_trader.indicator.macd import MACDIndicator

symbol = "BTCUSD_m"
frame = mt5.TIMEFRAME_M12

logger = logging.getLogger(__name__)

async def main():    
    try:
        macd = MACDIndicator(fast=5, slow=10, signal=9)
        chart = Chart(symbol, frame)

        chart.attach_indicator(macd)

        while True:
            await chart.update_chart()

            prices = chart.get_chart()
            macd_line = macd.get("macd")
            signal_line = macd.get("signal")
            histogram = macd.get("histogram")

            
    except:
        logger.info("Failed to operate")