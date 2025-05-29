# pyright: reportArgumentType=false

"""
Live MACD Histogram Chart only (no Candlestick), with values and soft/hard colors for M12 (HaClose), M75 (Close), and H4 (Close)
Each chart runs independently (async). Print latest histogram value for each. Optimized to avoid full redraw. Removed excess vertical white space.
"""

import asyncio
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import MetaTrader5 as mt5

from src.pyta_trader.chart import Chart
from src.pyta_trader.indicator.macd import MACDIndicator
from src.pyta_trader.strategy.price.close import CloseStrategy
from src.pyta_trader.strategy.price.ha_close import HaCloseStrategy

SYMBOL = "BTCUSD_m"
NUM_CANDLES = 50

async def run_chart(ax, label, symbol, tf, strategy, fast, slow, signal):
    chart = Chart(symbol=symbol, time_frame=tf)
    macd = MACDIndicator(strategy=strategy, fast=fast, slow=slow, signal=signal)
    chart.attach_indicator(macd)

    if not await chart.init_chart():
        raise RuntimeError(f"❌ Failed to initialize chart for {symbol} {tf}")

    print(f"✅ {label} initialized")

    while True:
        updated = await chart.check_and_update_chart()
        if not updated:
            await asyncio.sleep(0.5)
            continue

        prices = chart.get_chart()[-NUM_CANDLES:]
        hist_vals = macd.histogram[-NUM_CANDLES:]

        if len(prices) < 10 or len(hist_vals) < 10:
            await asyncio.sleep(0.5)
            continue

        df = pd.DataFrame(prices)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df["mpl_time"] = df["time"].map(mdates.date2num)

        x_vals = df["mpl_time"][-len(hist_vals):]
        width = (x_vals.iloc[1] - x_vals.iloc[0]) * 0.8 if len(x_vals) >= 2 else 0.0005

        latest_time = df["time"].iloc[-1]
        latest_val = macd.latest()
        print(f"📊 {label} | {latest_time} → Histogram: {latest_val:.2f}")

        bar_colors = []
        for i in range(len(hist_vals)):
            is_positive = hist_vals[i] >= 0
            is_increasing = i > 0 and hist_vals[i] > hist_vals[i - 1]
            if is_positive:
                bar_colors.append("#008000" if is_increasing else "#A9DFBF")
            else:
                bar_colors.append("#F5B7B1" if is_increasing else "#FF0000")

        ax.clear()
        bars = ax.bar(x_vals, hist_vals, width=width, color=bar_colors)
        ax.axhline(0, color='gray', linewidth=1, linestyle='--')
        ax.set_title(f"{symbol} - MACD Histogram ({label})")
        ax.set_ylabel("Histogram")
        ax.grid(True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

        last_rect = bars[-1]
        last_val = hist_vals[-1]
        ax.text(
            last_rect.get_x() + last_rect.get_width() / 2,
            last_val + (10 if last_val >= 0 else -10),
            f"{last_val:.2f}",
            ha="center",
            va="bottom" if last_val >= 0 else "top",
            fontsize=10,
            color='blue',
            fontweight='bold'
        )

        # Dynamically compute tighter y-limits
        hist_min = min(hist_vals)
        hist_max = max(hist_vals)
        padding = max(abs(hist_min), abs(hist_max)) * 0.05
        if padding < 5:
            padding = 5
        ax.set_ylim(hist_min - padding, hist_max + padding)

        plt.setp(ax.get_xticklabels(), rotation=45)
        fig = ax.get_figure()
        fig.set_constrained_layout(True)
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.05)
        await asyncio.sleep(0.5)

async def main():
    plt.ion()
    fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    tasks = [
        run_chart(axs[0], "M12 - HaClose", SYMBOL, mt5.TIMEFRAME_M12, HaCloseStrategy(), 5, 10, 9),
        # run_chart(axs[1], "M75 - Close", SYMBOL, mt5.TIMEFRAME_H1, CloseStrategy(), 5, 10, 9),
        run_chart(axs[2], "H4 - Close", SYMBOL, mt5.TIMEFRAME_H4, CloseStrategy(), 5, 10, 9),
    ]

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("🛑 Live histogram chart stopped.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    asyncio.run(main())
