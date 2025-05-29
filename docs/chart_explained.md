# 📄 Giải thích chi tiết Chart.py – Quản lý biểu đồ và sử dụng API MetaTrader5

Lớp `Chart` chịu trách nhiệm chính trong việc lấy và cập nhật dữ liệu giá từ MetaTrader5 (MT5) để cung cấp cho các indicator và chiến lược giao dịch. Dưới đây là phân tích chi tiết cách lớp này hoạt động, từng dòng làm gì, và tại sao lại sử dụng API như vậy.

---

## 🧩 Khởi tạo lớp `Chart`

```python
class Chart:
    def __init__(self, symbol: str, time_frame):
        self.symbol = symbol
        self.time_frame = time_frame
        self.prices = []
        self.last_tick_time = 0
        self.indicators = []
```

- **symbol**: mã sản phẩm tài chính, ví dụ `"EURUSD"` hoặc `"BTCUSD_m"`.
- **time_frame**: khung thời gian nến, ví dụ `mt5.TIMEFRAME_M15`.
- **prices**: danh sách chứa dữ liệu nến.
- **last_tick_time**: thời điểm tick cuối cùng, dùng để tránh cập nhật trùng.
- **indicators**: danh sách các chỉ báo được gắn vào biểu đồ này.

---

## 📥 `init_chart()` — lấy dữ liệu nến ban đầu

```python
rates = mt5.copy_rates_from_pos(self.symbol, self.time_frame, 0, 100)
```

- **API sử dụng:** `mt5.copy_rates_from_pos`
- **Chức năng:** Lấy 100 cây nến gần nhất cho `symbol` và `timeframe` đã chọn.
- **Mục tiêu:** Cung cấp dữ liệu cho các indicator có thể tính toán ngay (EMA, MACD, v.v.).
- **Chuyển đổi:** Sử dụng `datetime.fromtimestamp(r["time"])` để đưa `time` từ MT5 về định dạng Python datetime.

---

## 🔁 `check_and_update_chart()` — cập nhật giá mới bằng tick

```python
tick = mt5.symbol_info_tick(self.symbol)
```

- **API sử dụng:** `mt5.symbol_info_tick`
- **Chức năng:** Lấy giá `ask`, `bid`, `last` và `time` mới nhất từ thị trường.
- **Cơ chế cập nhật:**
  - Nếu có tick mới (`tick.time != self.last_tick_time`), cập nhật `self.prices[-1]["close"] = tick.last`.
  - Cập nhật `time` để khớp thời gian thực.
- **Tác dụng:** Giúp biểu đồ luôn thể hiện giá mới nhất mà không cần gọi lại toàn bộ `copy_rates`.

---

## 📊 `get_chart()` — trả dữ liệu cho Indicator

```python
def get_chart(self):
    return self.prices
```

- Trả về toàn bộ danh sách nến hiện có.
- Indicator hoặc Strategy sử dụng `chart.get_chart()` để lấy dữ liệu đầu vào.

---

## ➕ `attach_indicator()` & `detach_indicator()`

```python
def attach_indicator(self, indicator):
    if indicator not in self.indicators:
        self.indicators.append(indicator)
```

- Cho phép gắn chỉ báo (đã implement từ `Indicator`) vào biểu đồ.
- Tự động tính toán dựa trên giá hiện tại mà `Chart` cung cấp.
- Tách biệt rõ logic hiển thị giá và tính toán chỉ báo.

---

## ✅ Tổng kết các API MT5 được sử dụng

| API | Vai trò |
|-----|--------|
| `mt5.copy_rates_from_pos()` | Lấy dữ liệu nến ban đầu cho biểu đồ |
| `mt5.symbol_info_tick()` | Lấy tick mới để cập nhật giá đóng của nến hiện tại |
| `datetime.fromtimestamp()` | Chuyển `time` từ UNIX về định dạng Python datetime |

---

## 🧠 Mục tiêu thiết kế lớp `Chart`

- Tách biệt hoàn toàn phần **quản lý dữ liệu giá** khỏi phần **tính toán chỉ báo**.
- Cho phép mở rộng nguồn dữ liệu dễ dàng (ví dụ: có thể tạo `BinanceChart`, `CSVChart`, v.v.).
- Hỗ trợ linh hoạt nhiều Indicator có thể dùng chung một biểu đồ mà không can thiệp vào lớp dữ liệu.

---
