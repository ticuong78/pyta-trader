# pyright: reportArgumentType=false

"""
A live candlestick chart using mplfinance and your Chart class
"""

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.chart import Chart  # adjust if your Chart is in src/chart/chart.py

# ───── Configuration ─────
SYMBOL = "BTCUSD_m"
TIMEFRAME = 12  # mt5.TIMEFRAME_M12
NUM_CANDLES = 50

chart = Chart(symbol=SYMBOL, time_frame=TIMEFRAME)
if not chart.init_chart():
    raise RuntimeError("Failed to initialize chart")

fig, ax = plt.subplots(figsize=(10, 5))

def animate(frame):
    chart.check_and_update_chart()
    prices = chart.get_chart()[:NUM_CANDLES]

    if not prices:
        return

    # Convert to DataFrame
    df = pd.DataFrame(prices)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["mpl_time"] = df["time"].map(mdates.date2num)

    ohlc = df[["mpl_time", "open", "high", "low", "close"]]

    ax.clear()
    candlestick_ohlc(ax, ohlc.values, width=0.02, colorup='g', colordown='r')
    ax.xaxis_date()
    ax.set_title(f"{SYMBOL} - Live Candlestick Chart")
    ax.set_ylabel("Price")
    ax.set_xlabel("Time")
    ax.grid(True)
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()
