def calculate_ema(prices, period):
    alpha = 2 / (period + 1)
    ema = []
    for i, price in enumerate(prices):
        if i == 0:
            ema.append(price)
        else:
            ema.append(alpha * price + (1 - alpha) * ema[-1])
    return ema

__all__ = (
    "calculate_ema",
)