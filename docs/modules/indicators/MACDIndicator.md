# Giới thiệu

`MACDIndicator` là một lớp kế thừa từ `Indicator`, được sử dụng để tính toán ba đường chỉ báo kỹ thuật phổ biến trong phân tích kỹ thuật:

- **MACD Line**: Hiệu giữa đường EMA nhanh và EMA chậm  
- **Signal Line**: Đường EMA của MACD Line  
- **Histogram**: Hiệu giữa MACD Line và Signal Line  

Lớp này hoạt động dựa trên dữ liệu giá đã được xử lý bằng chiến lược (strategy) như Heikin Ashi hoặc giá đóng cửa gốc.

## Công dụng

- Tính toán chỉ báo MACD sử dụng các giá trị EMA  
- Hỗ trợ các chiến lược tính giá tùy biến  
- Hỗ trợ xử lý `None` để đảm bảo an toàn với dữ liệu chưa đủ  
- Có thể cập nhật dữ liệu bất đồng bộ từ `Chart`  

## Phương thức chi tiết

### `__init__(self, prices=[], strategy=HaCloseStrategy(), fast=5, slow=10, signal=9)`

**Mô tả**:  
Khởi tạo một đối tượng `MACDIndicator` mới với dữ liệu giá và các tham số chu kỳ EMA tùy chỉnh.

**Tham số**:

- `prices` (`List[Price]`): Danh sách dữ liệu giá đầu vào.  
- `strategy` (`PriceStrategy`): Chiến lược sử dụng để trích xuất giá (mặc định: Heikin Ashi).  
- `fast` (`int`): Số chu kỳ EMA nhanh (mặc định: 5).  
- `slow` (`int`): Số chu kỳ EMA chậm (mặc định: 10).  
- `signal` (`int`): Số chu kỳ EMA của đường MACD (mặc định: 9).  

**Ví dụ**:

```python
macd = MACDIndicator(prices=[], strategy=HaCloseStrategy(), fast=12, slow=26, signal=9)
```

---

### `async def update(self, prices: List[Price]) -> bool`

**Mô tả**:  
Cập nhật danh sách giá mới và tính toán lại các chỉ báo MACD, Signal và Histogram.

**Tham số**:

- `prices` (`List[Price]`): Danh sách dữ liệu giá cập nhật mới.

**Trả về**:  
`True` nếu tính toán thành công, `False` nếu dữ liệu không đủ.

**Ví dụ**:

```python
await macd.update(new_prices)
```

---

### `def get(self, attName: str) -> List[float]`

**Mô tả**:  
Truy xuất giá trị của một trong ba đường chỉ báo: `"macd"`, `"signal"`, hoặc `"histogram"`.

**Tham số**:

- `attName` (`str`): Tên của đường cần lấy (không phân biệt hoa thường).

**Trả về**:  
Danh sách các giá trị `float` (có thể chứa `None` nếu giá trị chưa sẵn sàng).

**Ví dụ**:

```python
macd_line = macd.get("macd")
signal_line = macd.get("signal")
hist = macd.get("histogram")
```

**Lưu ý**:  
Nếu `attName` không hợp lệ, hàm sẽ ném lỗi `LineNotSupportedError`.

---

## Các thuộc tính nội bộ

- `macd_line` (`List[float]`)  
- `signal_line` (`List[float]`)  
- `histogram` (`List[float]`)  
- `strategy` (`PriceStrategy`)  

---

## Phụ thuộc

- `calculate_ema` từ `smoothings`  
- `Price`  
- `Indicator`  
- `HaCloseStrategy`  
