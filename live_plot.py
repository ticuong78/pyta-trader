# pyright: reportArgumentType=false

"""
This is an exmaple of how to integrate this tool to your matplotlib projects
"""

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import MetaTrader5 as mt5
from datetime import datetime

# Make sure src/ is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src import Chart

SYMBOL = "BTCUSD_m"
TIMEFRAME = 12  # mt5.TIMEFRAME_M12
NUM_CANDLES = 25

chart = Chart(symbol=SYMBOL, time_frame=TIMEFRAME)

if not chart.init_chart():
    raise RuntimeError("Failed to initialize chart")

fig, ax = plt.subplots(figsize=(10, 5))

def animate(frame):
    chart.check_and_update_chart()
    prices = chart.get_chart()[:NUM_CANDLES]

    if len(prices) == 0:
        return

    times = [datetime.fromtimestamp(p['time']) for p in prices]
    closes = [p['close'] for p in prices]

    ax.clear()
    ax.plot(times, closes, label=f"{SYMBOL} Close Price")
    ax.set_title(f"{SYMBOL} - Live Chart ({NUM_CANDLES} candles)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
