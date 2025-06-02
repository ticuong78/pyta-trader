# Giới thiệu

Module `smoothings` cung cấp các hàm tính toán trung bình trượt thường (SMA) và trung bình trượt hàm mũ (EMA), được sử dụng làm lõi cho các indicator như MACD, RSI, v.v.

## Công dụng

- Cung cấp thuật toán tính SMA và EMA từ danh sách giá
- Đảm bảo kết quả căn chỉnh đúng chiều dài dữ liệu gốc
- Có thể tái sử dụng cho bất kỳ indicator nào trong hệ thống `pyta-trader`

---

## Hàm chi tiết

### `def calculate_sma(prices, period) -> float`

**Mô tả**:  
Tính trung bình cộng đơn giản (SMA) cho `period` đầu tiên trong danh sách giá.

**Tham số**:

- `prices` (`List[float]`): Danh sách giá (giá đóng cửa, Heikin Ashi, v.v.)
- `period` (`int`): Số chu kỳ cần tính trung bình

**Trả về**:  
`float` — Giá trị trung bình của `period` phần tử đầu tiên

**Ví dụ**:

```python
sma = calculate_sma([1, 2, 3, 4, 5], 3)  # Kết quả: 2.0
```

---

### `def calculate_ema(prices, period) -> List[float]`

**Mô tả**:  
Tính trung bình hàm mũ (EMA) cho danh sách giá, với độ trễ đầu vào là giá trị SMA đầu tiên.

**Tham số**:

- `prices` (`List[float]`): Danh sách giá đầu vào
- `period` (`int`): Chu kỳ EMA cần tính

**Trả về**:  
`List[float]` — Danh sách giá trị EMA, được padding bằng `None` ở đầu để khớp độ dài với đầu vào

**Thuật toán**:

- Khởi tạo bằng SMA đầu tiên
- Sử dụng công thức:
  
```python
EMA[i] = α * price[i] + (1 - α) * EMA[i - 1]
α = 2 / (period + 1)
```

**Ví dụ**:

```python
ema = calculate_ema([1, 2, 3, 4, 5], 3)
# Kết quả: [None, None, 2.0, 3.0, 4.0]
```

---

## Lưu ý

- Hàm `calculate_ema` sẽ trả về danh sách có độ dài bằng đầu vào, nhưng các phần tử đầu sẽ là `None` do chưa đủ dữ liệu để khởi tạo EMA.
- Nếu `len(prices) < period`, hàm sẽ trả về danh sách rỗng.

---

## Kết xuất

```python
__all__ = (
    "calculate_sma",
    "calculate_ema",
)
```

Các hàm này có thể được import trực tiếp từ:

```python
from pyta_trader.calculations.smoothings import calculate_sma, calculate_ema
```
