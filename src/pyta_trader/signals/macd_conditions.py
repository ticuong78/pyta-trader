# pyright: reportArgumentType=false

from typing import List
from ..chart import Chart
from ..indicator.macd import MACDIndicator

def classify_histogram_numeric(value: float, threshold: float = 0.01) -> int:
    """
    Phân loại giá trị MACD Histogram thành mã số tín hiệu:
    -2 = ĐỎ ĐẬM (giảm mạnh)
    -1 = ĐỎ LỢT (giảm nhẹ)
     1 = XANH LỢT (tăng nhẹ)
     2 = XANH ĐẬM (tăng mạnh)
    """
    if value < -threshold:
        return -2  # ĐỎ ĐẬM
    elif value < 0:
        return -1  # ĐỎ LỢT
    elif value <= threshold:
        return 1   # XANH LỢT
    else:
        return 2   # XANH ĐẬM

def macd_m12_signal_numeric(histogram: list[float], threshold: float = 0.01) -> int:
    """
    Tín hiệu MUA/BÁN dựa vào sự chuyển đổi giữa 2 histogram gần nhất:
    - return 1: nếu chuyển từ lợt → đậm tăng (BUY)
    - return 0: nếu chuyển từ lợt → đậm giảm (SELL)
    - return -1: không có tín hiệu
    """
    if len(histogram) < 2:
        return -1  # Không đủ dữ liệu

    prev = classify_histogram_numeric(histogram[-2], threshold)
    curr = classify_histogram_numeric(histogram[-1], threshold)

    if (prev == 1 and curr == 2) or (prev == -1 and curr == 2):
        return 1  # BUY
    if (prev == 1 and curr == -2) or (prev == -1 and curr == -2):
        return 0  # SELL

    return -1  # Không có tín hiệu

def macd_m75_or_h4_filter_numeric(histogram_latest: float, is_buy: bool, threshold: float = 0.01) -> bool:
    """
    Bộ lọc tín hiệu dựa trên Histogram của khung lớn (M75/H4):
    - Nếu đang MUA mà histogram là ĐỎ ĐẬM (giảm mạnh) → lọc bỏ (return True)
    - Nếu đang BÁN mà histogram là XANH ĐẬM (tăng mạnh) → lọc bỏ (return True)
    """
    color = classify_histogram_numeric(histogram_latest, threshold)
    if is_buy and color == -2:
        return True
    if not is_buy and color == 2:
        return True
    return False

def detect_macd_signal_from_chart(chart: Chart) -> int:
    """
    Sinh tín hiệu BUY/SELL từ dữ liệu trong Chart

    Returns:
        int: 1 = BUY, 0 = SELL, -1 = NO SIGNAL
    """
    prices = chart.get_chart()
    closes = [p["close"] for p in prices]

    if len(closes) < 10:
        return -1

    macd = MACDIndicator(closes)
    _, _, histogram = macd.calculate(closes)

    return macd_m12_signal_numeric(histogram)

if __name__ == "__main__":
    import MetaTrader5 as mt5
    from ..chart import Chart

    SYMBOL = "BTCUSD_m"
    TIMEFRAME = mt5.TIMEFRAME_M15

    chart = Chart(SYMBOL, TIMEFRAME)

    if not chart.init_chart():
        print("❌ Không thể khởi tạo biểu đồ")
    else:
        signal = detect_macd_signal_from_chart(chart)

        if signal == 1:
            print("📈 MACD BUY Signal")
        elif signal == 0:
            print("📉 MACD SELL Signal")
        else:
            print("❓ No signal (MACD không đủ điều kiện)")