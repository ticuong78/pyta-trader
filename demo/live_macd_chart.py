# pyright: reportArgumentType=false

"""
A live candlestick + MACD chart using mplfinance and your Chart class
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

# Ensure `src` folder is in path
sys.path.append(os.path.abspath("src"))

# ───── Custom modules ─────
from src.pyta_trader.chart import Chart
from src.pyta_trader.indicator.macd import MACDIndicator

# ───── Configuration ─────
SYMBOL = "BTCUSD_m"
TIMEFRAME = 12  # mt5.TIMEFRAME_M12
NUM_CANDLES = 50

# ───── Chart + Indicator Setup ─────
chart = Chart(symbol=SYMBOL, time_frame=TIMEFRAME)
if not chart.init_chart():
    raise RuntimeError("Failed to initialize chart")

macd = MACDIndicator()
chart.attach_indicator(macd)

# ───── Plotting Setup ─────
fig, (ax_price, ax_macd) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

def animate(frame):
    updated = chart.check_and_update_chart()
    prices = chart.get_chart()[:NUM_CANDLES]

    if not prices:
        return

    df = pd.DataFrame(prices)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["mpl_time"] = df["time"].map(mdates.date2num)

    ohlc = df[["mpl_time", "open", "high", "low", "close"]]

    # ───── Candlestick Chart ─────
    ax_price.clear()
    width = (ohlc["mpl_time"].iloc[0] - ohlc["mpl_time"].iloc[1]) * 0.8 if len(ohlc) >= 2 else 0.0005
    candlestick_ohlc(ax_price, ohlc.values, width=width, colorup='g', colordown='r')

    ax_price.set_title(f"{SYMBOL} - Live Candlestick Chart")
    ax_price.set_ylabel("Price")
    ax_price.grid(True)

    # ───── MACD Chart ─────
    ax_macd.clear()

    macd_vals = macd.macd[NUM_CANDLES:]
    signal_vals = macd.signal[NUM_CANDLES:]
    hist_vals = macd.histogram[NUM_CANDLES:]
    x_vals = df["mpl_time"].iloc[:len(macd_vals)]

    if len(macd_vals) > 1:
        ax_macd.bar(x_vals, hist_vals, width=width * 0.5, color=["green" if v >= 0 else "red" for v in hist_vals])
        ax_macd.plot(x_vals, macd_vals, label="MACD", color="blue")
        ax_macd.plot(x_vals, signal_vals, label="Signal", color="orange")
        ax_macd.legend(loc="upper left")
        ax_macd.set_ylabel("MACD")
        ax_macd.grid(True)

    # ───── Shared X-Axis Formatting ─────
    ax_macd.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax_price.set_xlim(ohlc["mpl_time"].min(), ohlc["mpl_time"].max())
    plt.setp(ax_macd.get_xticklabels(), rotation=45)
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
plt.show()
