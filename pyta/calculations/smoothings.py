# def calculate_sma(prices, period):
#     return sum(prices[:period]) / period

# def calculate_sma(prices, period):
#     sma = []
#     total = 0
#     for i in range(period):
#         total += prices[i] / period
#         sma.append(round(total, 3))  # làm tròn cho đẹp

#     return sma

def calculate_sma(prices, period):
    if len(prices) < period:
        return []
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



def calculate_rsi(prices, period):
    if len(prices) <= period:
        return [None] * len(prices)

    rsi = [None] * len(prices)

    # Tính delta
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [max(delta, 0) for delta in deltas]
    losses = [abs(min(delta, 0)) for delta in deltas]

    # Trung bình ban đầu (SMA)
    avg_gain = calculate_sma(gains, period)
    avg_loss = calculate_sma(losses, period)

    rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
    rsi[period] = 100 - (100 / (1 + rs))

    # Wilder’s smoothing cho các ngày tiếp theo
    for i in range(period, len(deltas)):
        gain = gains[i]
        loss = losses[i]

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            rsi_value = 100
        elif avg_gain == 0:
            rsi_value = 0
        else:
            rs = avg_gain / avg_loss
            rsi_value = 100 - (100 / (1 + rs))

        rsi[i + 1] = rsi_value  # dịch chỉ số để đúng với prices

    return rsi

__all__ = (
    "calculate_sma",
    "calculate_ema",
    "calculate_rsi",
)