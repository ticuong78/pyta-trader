# Giới thiệu

`Indicator` là lớp trừu tượng cơ sở cho tất cả các chỉ báo kỹ thuật trong hệ thống `pyta-trader`. Các lớp con như `MACDIndicator`, `RSIIndicator`, v.v., sẽ kế thừa từ lớp này và triển khai các phương thức tính toán cụ thể.

## Công dụng

- Định nghĩa chuẩn giao tiếp cho các indicator
- Cung cấp interface bất đồng bộ để cập nhật dữ liệu
- Cho phép hệ thống cập nhật giá và truy xuất dữ liệu indicator một cách nhất quán
- Đảm bảo các lớp con có cùng cấu trúc hoạt động

## Phương thức chi tiết

### `__init__(self, prices: List[Price])`

**Mô tả**:  
Khởi tạo đối tượng indicator với danh sách giá ban đầu.

**Tham số**:

- `prices` (`List[Price]`): Danh sách dữ liệu giá đầu vào (OHLC hoặc OHLCV)

**Ví dụ**:

```python
indicator = MyCustomIndicator(prices)
```

---

### `async def _calculate(self) -> bool`

**Mô tả**:  
Phương thức trừu tượng, dùng để tính toán chỉ báo dựa trên `self.prices`. Mỗi lớp con phải định nghĩa cách tính toán riêng.

**Trả về**:  
`True` nếu tính toán thành công, `False` nếu dữ liệu không đủ hoặc có lỗi.

**Ví dụ**:

```python
success = await indicator._calculate()
```

---

### `async def update(self, prices: List[Price]) -> bool`

**Mô tả**:  
Cập nhật dữ liệu giá mới cho indicator và gọi lại `_calculate()` để tính toán lại.

**Tham số**:

- `prices` (`List[Price]`): Dữ liệu giá mới

**Trả về**:  
`True` nếu cập nhật thành công.

**Ví dụ**:

```python
await indicator.update(new_prices)
```

---

### `def get(self, attName: str) -> List[float]`

**Mô tả**:  
Truy xuất giá trị theo tên thành phần indicator (tuỳ theo lớp con cài đặt).

**Tham số**:

- `attName` (`str`): Tên thành phần cần lấy, ví dụ `"macd"` hoặc `"signal"`

**Trả về**:  
Danh sách `float` (hoặc `None` nếu chưa tính xong)

**Ví dụ**:

```python
histogram = indicator.get("histogram")
```

---

### `def __eq__(self, other) -> bool`

**Mô tả**:  
So sánh hai indicator có cùng kiểu hay không. Có thể được override ở lớp con để so sánh sâu hơn.

**Ví dụ**:

```python
if macd1 == macd2:
    print("Cùng loại indicator")
```

---

## Lưu ý khi kế thừa

- Bắt buộc triển khai 3 phương thức: `_calculate()`, `update()`, và `get()`
- Kết quả tính toán nên lưu vào các thuộc tính riêng như `macd_line`, `signal_line`, v.v.
- Đảm bảo `get()` trả về dữ liệu đúng định dạng và xử lý tên không phân biệt hoa thường
