import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyta.calculations.smoothings import calculate_rsi

def test_calculate_rsi_mixed_trend():
    prices = [
        50.00, 51.00, 50.50, 49.00, 48.00,
        47.50, 48.50, 49.00, 48.50, 47.00,
        46.00, 47.00, 48.50, 49.50, 49.00,
        48.00, 47.50, 46.50, 45.00, 44.00,
        43.50, 44.00, 45.50, 46.50, 47.00,
        47.50, 48.00, 48.50, 48.00, 47.00
    ]
    period = 14
    rsi = calculate_rsi(prices, period)

    print("📊 RSI Values (Mixed Trend Dataset):")
    for i, val in enumerate(rsi):
        if val is None:
            print(f"  Day {i+1}: Not enough data")
        else:
            print(f"  Day {i+1}: RSI = {val:.2f}")

    assert len(rsi) == len(prices)
    assert rsi[period] is not None
    assert 0 <= rsi[period] <= 100

    print("\n✅ test_calculate_rsi_mixed_trend passed.")

if __name__ == "__main__":
    test_calculate_rsi_mixed_trend()
