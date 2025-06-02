import logging
import sys
import asyncio
import MetaTrader5 as mt5

from pyta.chart import Chart
from pyta.indicator.macd import MACDIndicator

symbol = "BTCUSD_m"
frame = mt5.TIMEFRAME_M12

logger = logging.getLogger(__name__)

async def updater():
    macd = MACDIndicator(fast=5, slow=10, signal=9)
    chart = Chart(symbol, frame)
    chart.attach_indicator(macd)

    await chart.init_chart()

    while True:
        await chart.update_chart()

        macd_line = macd.get("macd")
        signal_line = macd.get("signal")
        histogram = macd.get("histogram")

        if not (macd_line and signal_line and histogram):
            await asyncio.sleep(0.2)
            continue

        print(f"Time: {chart.last_tick_time}, Histogram: {histogram[-1]:.5f}")
        await asyncio.sleep(0.2)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(updater())
