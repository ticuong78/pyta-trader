def calculate_ema(prices, period):
    ema = []
    if len(prices) < period:
        return []

    # Start with SMA
    sma = sum(prices[:period]) / period
    ema.append(sma)

    alpha = 2 / (period + 1)
    for price in prices[period:]:
        ema.append(alpha * price + (1 - alpha) * ema[-1])
    return ema  # pad to match TradingView's indexing

__all__ = (
    "calculate_ema",
)