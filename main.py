import asyncio
import time
from src.pyta_trader.chart.chart import Chart
from src.pyta_trader.indicator.macd import MACDIndicator

import MetaTrader5 as mt5

async def main():
    # Initialize chart for a specific symbol and timeframe
    chart = Chart(symbol="BTCUSD_m", time_frame=mt5.TIMEFRAME_M12)  # Adjust symbol and timeframe as needed

    # Initialize MACD indicator with default parameters
    macd_indicator = MACDIndicator()

    # Attach the MACD indicator to the chart
    chart.attach_indicator(macd_indicator)

    # Initialize the chart (fetch initial data)
    if not await chart.init_chart():
        print("Failed to initialize chart.")
        return

    print("Starting live MACD monitoring...")

    try:
        while True:
            # Check for new data and update chart
            updated = chart.check_and_update_chart()

            if updated:
                # Run indicator calculations
                await chart.run_indicators()

                # Retrieve the latest MACD values
                macd_value = macd_indicator.macd
                signal_value = macd_indicator.signal
                histogram_value = macd_indicator.histogram

                # Display the MACD values
                print(f"MACD: {macd_value:.5f}, Signal: {signal_value:.5f}, Histogram: {histogram_value:.5f}")

            # Wait for a specified interval before the next update
            await asyncio.sleep(60)  # Adjust the sleep duration as needed

    except KeyboardInterrupt:
        print("Live MACD monitoring stopped.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
