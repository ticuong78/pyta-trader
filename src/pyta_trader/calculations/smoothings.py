def calculate_sma(prices, period):
    sma = 0
    for i in range(period):
        sma += prices[i]

    return sma / period


def calculate_ema(prices, period):
    ema = []

    sma = calculate_sma(prices, period)
    ema.append(sma)
    
    if len(prices) < period:
        return []
    
    alpha = 2 / period + 1

    for i in range(period, len(prices)):
        ema.append(alpha * prices[i] + (1 - alpha) * ema[-1])
        
    return ema

__all__ = (
    "calculate_sma",
    "calculate_ema",
)