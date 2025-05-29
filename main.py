# pyright: reportArgumentType=false

"""
Live MACD Histogram Chart only (no Candlestick), with values and soft/hard colors
"""

import asyncio
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

from src.pyta_trader.chart import Chart
from src.pyta_trader.indicator.macd import MACDIndicator

SYMBOL = "BTCUSD_m"
TIMEFRAME = 12
NUM_CANDLES = 50

async def main():
    chart = Chart(symbol=SYMBOL, time_frame=TIMEFRAME)
    macd = MACDIndicator()
    chart.attach_indicator(macd)

    if not await chart.init_chart():
        raise RuntimeError("❌ Failed to initialize chart")

    print("✅ Chart and MACD initialized. Starting histogram plot...")

    plt.ion()
    fig, ax_macd = plt.subplots(figsize=(12, 5))

    try:
        while True:
            updated = await chart.check_and_update_chart()
            if not updated:
                await asyncio.sleep(0.1)
                continue

            prices = chart.get_chart()[-NUM_CANDLES:]
            hist_vals = macd.histogram

            if len(prices) < 10 or len(hist_vals) < 10:
                print(len(prices), len(hist_vals))
                print("⌛ Waiting for more price/MACD data...")
                await asyncio.sleep(1)
                continue

            # Convert to DataFrame and extract timestamps
            df = pd.DataFrame(prices)
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df["mpl_time"] = df["time"].map(mdates.date2num)

            x_vals = df["mpl_time"]
            n = min(len(hist_vals), len(x_vals))
            x_vals = x_vals[-n:]
            hist_vals = hist_vals[-n:]

            width = (x_vals.iloc[1] - x_vals.iloc[0]) * 0.8 if len(x_vals) >= 2 else 0.0005

            # Color logic: bold if increasing vs previous, light if not
            bar_colors = []
            for i in range(n):
                is_positive = hist_vals[i] >= 0
                is_increasing = i > 0 and hist_vals[i] > hist_vals[i - 1]
                if is_positive:
                    bar_colors.append("#008000" if is_increasing else "#A9DFBF")  # Green / Light Green
                else:
                    bar_colors.append("#F5B7B1" if is_increasing else "#FF0000")  # Light Red / Dark Red (swapped)

            ax_macd.clear()
            bars = ax_macd.bar(
                x_vals,
                hist_vals,
                width=width,
                color=bar_colors
            )
            ax_macd.axhline(0, color='gray', linewidth=1, linestyle='--')
            ax_macd.set_title(f"{SYMBOL} - MACD Histogram")
            ax_macd.set_ylabel("MACD Histogram")
            ax_macd.grid(True)
            ax_macd.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            plt.setp(ax_macd.get_xticklabels(), rotation=45)
            plt.tight_layout()

            # Plot value label above each bar
            for rect, val in zip(bars, hist_vals):
                if val is not None:
                    ax_macd.text(
                        rect.get_x() + rect.get_width() / 2,
                        val + (10 if val >= 0 else -10),
                        f"{val:.2f}",
                        ha="center",
                        va="bottom" if val >= 0 else "top",
                        fontsize=8,
                        color='black',
                    )

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.1)

            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        print("🛑 Live histogram chart stopped.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    asyncio.run(main())
