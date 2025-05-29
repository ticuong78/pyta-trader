# pyright: reportArgumentType=false

"""
A live candlestick chart using mplfinance and your Chart class (async version)
"""

import sys
import os
import asyncio
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from src.pyta_trader.chart.chart import Chart

# ───── Configuration ─────
SYMBOL = "BTCUSD_m"
TIMEFRAME = 12  # mt5.TIMEFRAME_M12
NUM_CANDLES = 50

async def main():
    chart = Chart(symbol=SYMBOL, time_frame=TIMEFRAME)

    if not await chart.init_chart():
        raise RuntimeError("❌ Failed to initialize chart")

    print("✅ Chart initialized. Starting live candlestick plot...")

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 5))

    try:
        while True:
            updated = await chart.check_and_update_chart()

            if not updated:
                await asyncio.sleep(1)
                continue

            prices = chart.get_chart()[-NUM_CANDLES:]
            if not prices:
                print("⌛ Waiting for price data...")
                await asyncio.sleep(1)
                continue

            df = pd.DataFrame(prices)
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df["mpl_time"] = df["time"].map(mdates.date2num)

            ohlc = df[["mpl_time", "open", "high", "low", "close"]]

            ax.clear()

            # Calculate bar width
            if len(df) >= 2:
                spacing = abs(df["mpl_time"].iloc[1] - df["mpl_time"].iloc[0])
                width = spacing * 0.8
            else:
                width = 0.0005

            candlestick_ohlc(ax, ohlc.values, width=width, colorup="g", colordown="r")

            ax.set_title(f"{SYMBOL} - Live Candlestick Chart")
            ax.set_ylabel("Price")
            ax.set_xlabel("Time")
            ax.grid(True)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
            ax.set_xlim(ohlc["mpl_time"].min(), ohlc["mpl_time"].max())
            plt.setp(ax.get_xticklabels(), rotation=45)
            plt.tight_layout()

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.1)

            await asyncio.sleep(10)  # Refresh interval in seconds

    except KeyboardInterrupt:
        print("🛑 Stopped by user.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    asyncio.run(main())
