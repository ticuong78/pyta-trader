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
from src import Chart

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

    df = pd.DataFrame(prices)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["mpl_time"] = df["time"].map(mdates.date2num)

    ohlc = df[["mpl_time", "open", "high", "low", "close"]]

    ax.clear()

    if len(df) >= 2:
        spacing = abs(df["mpl_time"].iloc[0] - df["mpl_time"].iloc[1])
        width = spacing * 0.8
    else:
        width = 0.0005

    candlestick_ohlc(ax, ohlc.values, width=width, colorup='g', colordown='r')

    ax.set_title(f"{SYMBOL} - Live Candlestick Chart")
    ax.set_ylabel("Price")
    ax.set_xlabel("Time")
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.set_xlim(ohlc["mpl_time"].min(), ohlc["mpl_time"].max())
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=1, cache_frame_data=False)
plt.show()
