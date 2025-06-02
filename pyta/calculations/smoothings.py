def calculate_sma(prices, period):
    return sum(prices[:period]) / period

def calculate_ema(prices, period):
    if len(prices) < period:
        return []

    ema = []
    sma = calculate_sma(prices, period)
    ema.append(sma)

    alpha = 2 / (period + 1)  
    
    for i in range(period, len(prices)):
        ema.append(alpha * prices[i] + (1 - alpha) * ema[-1])

    # Padding to align output length with input length
    return [None] * (period - 1) + ema

__all__ = (
    "calculate_sma",
    "calculate_ema",
)