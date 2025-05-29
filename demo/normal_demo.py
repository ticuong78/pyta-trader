# pyright: reportArgumentType=false

import sys
import os
import asyncio
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
from datetime import datetime

# Make sure src/ is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.pyta_trader.chart.chart import Chart

SYMBOL = "BTCUSD_m"
TIMEFRAME = 12  # mt5.TIMEFRAME_M12
NUM_CANDLES = 20

async def main():
    chart = Chart(symbol=SYMBOL, time_frame=TIMEFRAME)

    if not await chart.init_chart():
        raise RuntimeError("❌ Failed to initialize chart")

    print("✅ Chart initialized. Launching live plot...")

    # Setup matplotlib
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 5))

    try:
        while True:
            updated = await chart.check_and_update_chart()
            if updated:
                prices = chart.get_chart()[-NUM_CANDLES:]

                if len(prices) == 0:
                    print("⌛ Waiting for more data...")
                    await asyncio.sleep(1)
                    continue

                times = [datetime.fromtimestamp(p["time"]) for p in prices]
                closes = [p["close"] for p in prices]

                ax.clear()
                ax.plot(times, closes, label=f"{SYMBOL} Close Price", color="blue")
                ax.set_title(f"{SYMBOL} - Live Chart ({NUM_CANDLES} candles)")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.legend(loc="upper left")
                ax.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()

                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.1)

            await asyncio.sleep(10)

    except KeyboardInterrupt:
        print("🛑 Live chart stopped.")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    asyncio.run(main())
