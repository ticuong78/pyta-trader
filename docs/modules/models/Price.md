# Giới thiệu

`Price` là một model dữ liệu được dùng để biểu diễn một cây nến (OHLCV) trong hệ thống giao dịch. Lớp này được định nghĩa bằng `pydantic.BaseModel` để đảm bảo kiểm soát và xác thực dữ liệu đầu vào.

## Công dụng

- Đại diện cho dữ liệu một nến: thời gian, giá mở/đóng/cao/thấp, volume...
- Dùng làm dữ liệu đầu vào cho các indicator và biểu đồ
- Được sử dụng trong quá trình chuyển đổi dữ liệu từ MetaTrader 5 sang nội bộ hệ thống Python
- Ngăn chặn dữ liệu không hợp lệ thông qua cấu hình `extra="forbid"`

## Thuộc tính

- `time` (`int`): Thời gian (UNIX timestamp)  
- `open` (`float`): Giá mở cửa  
- `high` (`float`): Giá cao nhất  
- `low` (`float`): Giá thấp nhất  
- `close` (`float`): Giá đóng cửa  
- `tick_volume` (`Optional[float]`): Khối lượng theo số tick  
- `spread` (`Optional[float]`): Spread tại thời điểm đó  
- `real_volume` (`Optional[float]`): Khối lượng thực tế  

**Ví dụ**:

```python
Price(
    time=1717262734,
    open=101.5,
    high=105.0,
    low=100.1,
    close=103.2,
    tick_volume=1200,
    spread=0.3,
    real_volume=500.0
)
```

---

## Hàm tiện ích

### `convert_rate_to_price(rate: np.void) -> Price`

**Mô tả**:  
Chuyển đổi một dòng dữ liệu nến (`np.void`) từ MetaTrader 5 (ví dụ từ `mt5.copy_rates_from_pos`) sang đối tượng `Price`.

**Tham số**:

- `rate` (`np.void`): Một dòng dữ liệu giá chứa các field như `"time"`, `"open"`, `"high"`, `"low"`, `"close"`, v.v.

**Trả về**:  
Một đối tượng `Price` tương ứng.

**Ví dụ**:

```python
import MetaTrader5 as mt5
import numpy as np

rates = mt5.copy_rates_from_pos("BTCUSD", mt5.TIMEFRAME_M1, 0, 1)
price = convert_rate_to_price(rates[0])
print(price.close)
```

**Xử lý lỗi**:  
Nếu thiếu field hoặc kiểu dữ liệu không hợp lệ, hàm sẽ raise exception để dừng hệ thống.

---

## Lưu ý

- Trường hợp sử dụng phổ biến nhất là trong khởi tạo biểu đồ (`Chart.init_chart`) và cập nhật giá (`Chart.update_chart`)
- Trường `model_config = ConfigDict(extra="forbid")` đảm bảo không có field thừa được phép khởi tạo model
