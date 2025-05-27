def calculate_ema(prices, period):
    alpha = 2 / (period + 1)
    ema = []
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)
        else:
            ema.append(alpha * price + (1 - alpha) * ema[-1])
    return ema


def calculate_macd(prices, fast=5, slow=10, signal=9):
    fast_ema = calculate_ema(prices, fast)
    slow_ema = calculate_ema(prices, slow)
    macd = [f - s for f, s in zip(fast_ema, slow_ema)]
    signal_line = calculate_ema(macd, signal)
    histogram = [m - s for m, s in zip(macd, signal_line)]
    return macd, signal_line, histogram



__all__ = (
    "calculate_ema",
    "calculate_macd"
)