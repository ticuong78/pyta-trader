# Giới thiệu

Chart là một lớp được viết ra để kết nối và lấy thông tin thời gian thực trên sàn giao dịch Meta Trader 5

## Công dụng

Lớp này đã được tích hợp một số tính năng của Meta Trader bao gồm:

- Lấy thông tin thời gian thực
- Gắn thêm indicator và cập nhật thông tin mới cho indicator mỗi khi có sự thay đổi về giá xảy ra
- Tính toán indicator bất đồng bộ

## Phương thức chi tiết

### `__init__(self, symbol: str, time_frame: int)`

**Mô tả**:  
Khởi tạo một đối tượng `Chart` mới với mã giao dịch (`symbol`) và khung thời gian (`time_frame`) tương ứng.

**Tham số**:

- `symbol` (`str`): Mã giao dịch (ví dụ: `"BTCUSD"`, `"EURUSD"`).
- `time_frame` (`int`): Khung thời gian sử dụng (ví dụ: `mt5.TIMEFRAME_M1`, `mt5.TIMEFRAME_H1`).

**Ví dụ**:

```python
chart = Chart(symbol="BTCUSD", time_frame=mt5.TIMEFRAME_M1)
```

---

### `async def run_indicators(self) -> None`

**Mô tả**:  
Chạy cập nhật tất cả các indicator đã được gắn vào biểu đồ bằng cách gọi phương thức `update` bất đồng bộ trên từng indicator.

**Trả về**:  
Không có giá trị trả về.

**Ví dụ**:

```python
await chart.run_indicators()
```

---

### `async def init_chart(self) -> bool`

**Mô tả**:  
Khởi tạo biểu đồ bằng cách kết nối với MetaTrader 5, lấy dữ liệu nến lịch sử và khởi tạo giá. Đồng thời chạy cập nhật tất cả các indicator đã gắn.

**Trả về**:  
`True` nếu thành công, `False` nếu thất bại (ví dụ: không kết nối được hoặc không lấy được dữ liệu).

**Ví dụ**:

```python
success = await chart.init_chart()
if not success:
    print("Không thể khởi tạo biểu đồ")
```

---

### `async def update_chart(self) -> bool`

**Mô tả**:  
Cập nhật biểu đồ nếu có giá mới. Thêm giá mới vào danh sách `prices` và gọi cập nhật các indicator.

**Trả về**:  
`True` nếu biểu đồ đã được cập nhật thành công với dữ liệu mới, `False` nếu không có giá mới hoặc có lỗi xảy ra.

**Ví dụ**:

```python
updated = await chart.update_chart()
if updated:
    print("Đã cập nhật giá mới")
```

---

### `def attach_indicator(self, indicator: Indicator) -> None`

**Mô tả**:  
Gắn một indicator mới vào biểu đồ nếu chưa được gắn trước đó.

**Tham số**:

- `indicator` (`Indicator`): Một indicator cần được gắn vào.

**Ví dụ**:

```python
chart.attach_indicator(MACDIndicator([]))
```

---

### `def detach_indicator(self, indicator: Indicator) -> None`

**Mô tả**:  
Gỡ một indicator ra khỏi danh sách theo dõi nếu nó đang được gắn.

**Tham số**:

- `indicator` (`Indicator`): Indicator cần được gỡ ra.

**Ví dụ**:

```python
chart.detach_indicator(macd)
```

---

### `def get_chart(self) -> List[Price]`

**Mô tả**:  
Trả về toàn bộ danh sách `Price` đã được lưu trong biểu đồ.

**Trả về**:  
Danh sách `Price`.

**Ví dụ**:

```python
prices = chart.get_chart()
for price in prices:
    print(price.time, price.close)
```

---

## Hàm tiện ích

### `def shift_append(arr: List[Any], item: Any, max_len: int) -> None`

**Mô tả**:  
Thêm một phần tử vào cuối danh sách. Nếu vượt quá giới hạn `max_len`, phần tử đầu tiên sẽ bị loại bỏ.

**Tham số**:

- `arr`: Danh sách ban đầu.
- `item`: Phần tử cần thêm.
- `max_len`: Số lượng tối đa của danh sách.

**Ví dụ**:

```python
shift_append(my_list, new_value, 100)
```
