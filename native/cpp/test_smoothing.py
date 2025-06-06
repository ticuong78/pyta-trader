import smoothing_cpp
import math

def test_calculate_sma():
    prices = [1, 2, 3, 4, 5]
    period = 3
    expected_sma = (1 + 2 + 3) / 3  # 2.0
    result = smoothing_cpp.calculate_sma(prices, period)
    assert math.isclose(result, expected_sma, rel_tol=1e-9), f"SMA expected {expected_sma}, got {result}"
    print("✅ test_calculate_sma passed.")

def test_calculate_ema():
    prices = [1, 2, 3, 4, 5]
    period = 3
    ema = smoothing_cpp.calculate_ema(prices, period)
    
    # EMA will have length = len(prices), with first period-1 = NANs
    assert len(ema) == len(prices), f"EMA length mismatch, expected {len(prices)}, got {len(ema)}"
    
    # First period-1 values must be NaN
    for i in range(period - 1):
        assert math.isnan(ema[i]), f"Expected NaN at index {i}, got {ema[i]}"

    # Check that EMA[period-1] == SMA of first `period` prices
    sma = smoothing_cpp.calculate_sma(prices, period)
    assert math.isclose(ema[period - 1], sma, rel_tol=1e-9), f"Expected SMA at EMA[{period-1}]"

    print("✅ test_calculate_ema passed.")

if __name__ == "__main__":
    test_calculate_sma()
    test_calculate_ema()
