def calculate_sma(prices, period):
    if len(prices) < period or period <= 0:
        return None
    return round(sum(prices[:period]) / period, 3)

def calculate_ema(prices, period, pad: bool = True):
    if len(prices) < period:
        return []  # Không đủ dữ liệu để tính

    sma = calculate_sma(prices, period)
    ema = [sma]

    alpha = 2 / (period + 1)

    for i in range(period, len(prices)):

        next_ema = (alpha * prices[i] + (1 - alpha) * ema[- 1])
        ema.append(round(next_ema, 3))

    return [sma] * (period - 1) + ema if pad else ema

__all__ = (
    "calculate_sma",
    "calculate_ema",
)