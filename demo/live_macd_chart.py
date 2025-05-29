# pyright: reportArgumentType=false

"""
Live MACD Histogram Chart only (no Candlestick)
"""

import asyncio
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

from src.pyta_trader.chart import Chart
from src.pyta_trader.indicator.macd import MACDIndicator

# ───── Configuration ─────
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
                await asyncio.sleep(1)
                continue

            prices = chart.get_chart()[-NUM_CANDLES:]
            if len(prices) < 10 or len(macd.histogram) < 10:
                print(len(prices), len(macd.histogram))
                print("⌛ Waiting for more price/MACD data...")
                await asyncio.sleep(1)
                continue

            # Convert to DataFrame and extract timestamps
            df = pd.DataFrame(prices)
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df["mpl_time"] = df["time"].map(mdates.date2num)

            x_vals = df["mpl_time"]
            hist_vals = macd.histogram

            # Align lengths
            n = min(len(hist_vals), len(x_vals))
            x_vals = x_vals[-n:]
            hist_vals = hist_vals[-n:]

            width = (x_vals.iloc[1] - x_vals.iloc[0]) * 0.8 if len(x_vals) >= 2 else 0.0005

            # ───── Histogram Plot ─────
            ax_macd.clear()
            ax_macd.bar(
                x_vals,
                hist_vals,
                width=width,
                color=["green" if v >= 0 else "red" for v in hist_vals]
            )
            ax_macd.axhline(0, color='gray', linewidth=1, linestyle='--')
            ax_macd.set_title(f"{SYMBOL} - MACD Histogram")
            ax_macd.set_ylabel("MACD Histogram")
            ax_macd.grid(True)
            ax_macd.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            plt.setp(ax_macd.get_xticklabels(), rotation=45)
            plt.tight_layout()

            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.1)

            await asyncio.sleep(10)

    except KeyboardInterrupt:
        print("🛑 Live histogram chart stopped.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    asyncio.run(main())
