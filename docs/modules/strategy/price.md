# Giới thiệu

Các lớp trong module `strategy.price` đại diện cho các chiến lược trích xuất giá từ một cây nến (`Price`) để phục vụ cho tính toán chỉ báo kỹ thuật như MACD, RSI, v.v.

## Công dụng

- Cho phép indicator linh hoạt sử dụng các cách tính giá khác nhau  
- Dễ dàng mở rộng thêm các chiến lược khác (ví dụ: giá trung bình, weighted close, v.v.)  
- Tách biệt logic xử lý giá ra khỏi chỉ báo — tuân theo nguyên lý SOLID (Open/Closed)

---

## Lớp cơ sở

### `class PriceStrategy`

**Mô tả**:  
Lớp nền tảng (base class) cho tất cả các chiến lược xử lý giá. Các lớp con phải override phương thức `calculate`.

### `def calculate(self, candle: Price) -> float`

**Mô tả**:  
Trích xuất giá trị đại diện từ một cây nến (candle). Lớp con phải định nghĩa logic cụ thể.

**Tham số**:

- `candle` (`Price`): Một đối tượng biểu diễn giá nến (OHLC)

**Trả về**:  
`float` — giá trị đại diện cho cây nến để dùng trong tính toán indicator

**Ví dụ**:

```python
strategy = MyCustomStrategy()
value = strategy.calculate(price)
```

---

## Lớp triển khai cụ thể

### `class HaCloseStrategy(PriceStrategy)`

**Mô tả**:  
Chiến lược sử dụng giá đóng cửa Heikin Ashi (trung bình của Open, High, Low, Close)

**Công thức**:

```python
Heikin Ashi Close = (Open + High + Low + Close) / 4
```

**Ví dụ**:

```python
strategy = HaCloseStrategy()
ha_close = strategy.calculate(price)
```

---

### `class CloseStrategy(PriceStrategy)`

**Mô tả**:  
Chiến lược đơn giản sử dụng giá đóng cửa (`close`) của cây nến làm giá đại diện.

**Ví dụ**:

```python
strategy = CloseStrategy()
close_price = strategy.calculate(price)
```

---

## Lưu ý mở rộng

- Bạn có thể dễ dàng thêm một lớp mới kế thừa `PriceStrategy` để dùng chiến lược riêng của bạn:
  
```python
class WeightedCloseStrategy(PriceStrategy):
    def calculate(self, candle):
        return (candle.high + candle.low + 2 * candle.close) / 4
```

- `Indicator` như `MACDIndicator` có thể nhận tham số `strategy` trong constructor để áp dụng chiến lược phù hợp.

---

## Các lớp hiện có

| Tên lớp         | Ý nghĩa                                              |
|------------------|------------------------------------------------------|
| `PriceStrategy`  | Lớp cơ sở (trừu tượng) cho tất cả chiến lược giá     |
| `HaCloseStrategy`| Giá đóng Heikin Ashi: (Open + High + Low + Close)/4 |
| `CloseStrategy`  | Giá đóng cửa truyền thống (`candle.close`)          |
