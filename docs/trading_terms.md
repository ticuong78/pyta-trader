# 📚 Từ Điển Thuật Ngữ Giao Dịch Cho Lập Trình MetaTrader5 Trong Python

Tài liệu này tập hợp và giải thích các thuật ngữ cốt lõi trong giao dịch tài chính, kèm theo ví dụ sử dụng thực tế trong code Python với thư viện `MetaTrader5`.

---

## ✅ Symbol

- **Định nghĩa:** Tên của sản phẩm tài chính. Có thể là cặp tiền tệ (`EURUSD`), vàng (`XAUUSD`), hay cổ phiếu CFD.

- **Trong MT5:** Bắt buộc phải truyền `symbol` vào hầu hết các hàm như lấy dữ liệu giá, đặt lệnh, xem thông tin tài khoản...

- **Ví dụ:**
```python
info = mt5.symbol_info("EURUSD")
print(info.name, info.trade_contract_size)
```

- **Thực hành tốt:**
  - Luôn kiểm tra `symbol_info` có trả về `None` hay không → symbol có thể chưa được bật trong MT5.

---

## ✅ Tick

- **Định nghĩa:** Một thay đổi giá duy nhất (bao gồm giá Bid, Ask, Last, Volume...).

- **Ứng dụng:** Dùng để xác định giá hiện tại để đặt lệnh thị trường.

- **Ví dụ:**
```python
tick = mt5.symbol_info_tick("XAUUSD")
if tick:
    print("Ask =", tick.ask, "Bid =", tick.bid)
```

- **Cảnh báo:** Tick có thể không thay đổi nếu thị trường tạm ngừng (thứ 7, chủ nhật, ngày lễ...).

---

## ✅ Timeframe

- **Định nghĩa:** Khung thời gian của nến: M1, M5, H1, D1, W1...

- **Sử dụng:** Dùng trong các hàm `copy_rates_*` để xác định mức chi tiết của dữ liệu.

- **Ví dụ:**
```python
from datetime import datetime
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, datetime.now(), 100)
```

- **Gợi ý:** Luôn thống nhất `timeframe` với chiến lược (scalping dùng M1/M5, swing dùng H1/H4).

---

## ✅ Volume (Lot)

- **Định nghĩa:** Khối lượng giao dịch. Trong Forex, 1 lot = 100.000 đơn vị.

- **Trong lệnh:** Truyền qua tham số `volume` trong `order_send`.

- **Ví dụ:**
```python
"volume": 0.1  # = 10.000 đơn vị với Forex
```

- **Lưu ý:** Volume tối thiểu phụ thuộc từng symbol (xem `symbol_info().volume_min`).

---

## ✅ Ask / Bid

- **Định nghĩa:**
  - **Ask:** Giá bạn sẽ mua (sàn bán cho bạn).
  - **Bid:** Giá bạn sẽ bán (sàn mua từ bạn).

- **Ứng dụng:** Đặt lệnh BUY tại giá Ask, SELL tại giá Bid.

- **Ví dụ:**
```python
ask = mt5.symbol_info_tick("BTCUSD").ask
bid = mt5.symbol_info_tick("BTCUSD").bid
```

---

## ✅ Spread

- **Định nghĩa:** Chênh lệch giữa Ask và Bid.

- **Vai trò:** Là chi phí âm bạn chịu khi vừa mở lệnh.

- **Ví dụ:**
```python
tick = mt5.symbol_info_tick("EURUSD")
spread = tick.ask - tick.bid
if spread > 0.0005:
    print("Spread quá cao, tránh giao dịch!")
```

- **Kỹ thuật:** Spread thay đổi theo thời gian, đặc biệt trước tin tức. Cần kiểm tra trước khi đặt lệnh.

---

## ✅ Point

- **Định nghĩa:** Bước nhảy giá nhỏ nhất.

- **Ứng dụng:** Tính toán SL, TP, khoảng trượt...

- **Ví dụ:**
```python
point = mt5.symbol_info("XAUUSD").point
sl = price - 50 * point
tp = price + 100 * point
```

---

## ✅ SL (Stop Loss) / TP (Take Profit)

- **Định nghĩa:**
  - **SL:** Ngưỡng cắt lỗ tự động
  - **TP:** Ngưỡng chốt lời tự động

- **Ứng dụng:** Cần thiết trong chiến lược giao dịch tự động để kiểm soát rủi ro.

- **Ví dụ:**
```python
request = {
  ...
  "sl": price - 200 * point,
  "tp": price + 300 * point,
}
```

---

## ✅ Magic Number

- **Định nghĩa:** Mã định danh duy nhất cho mỗi chiến lược.

- **Lợi ích:** Giúp tách biệt các EA khi khớp nhiều lệnh song song.

- **Ví dụ:**
```python
"magic": 888888  # EA1
"magic": 999999  # EA2
```

- **Lưu ý:** Khi đọc `positions_get()`, bạn có thể lọc theo magic number.

---

## ✅ Order Filling Mode

- **Loại:**
  - `ORDER_FILLING_IOC`: Khớp càng nhiều càng tốt, phần còn lại hủy.
  - `ORDER_FILLING_FOK`: Khớp toàn bộ hoặc không khớp gì cả.

- **Gợi ý:** Dùng `IOC` để tránh bị từ chối khi khối lượng thanh khoản không đủ.

---

## ✅ GTC - Good Till Cancelled

- **Định nghĩa:** Lệnh chờ được giữ đến khi bị hủy hoặc khớp.

- **Trong MT5:** Thường áp dụng cho các lệnh chờ như BUY LIMIT, SELL STOP...

---

## ✅ Position

- **Định nghĩa:** Một lệnh đang được giữ/mở.

- **Truy xuất:** Qua `mt5.positions_get()`.

- **Ví dụ:**
```python
for p in mt5.positions_get(symbol="BTCUSD"):
    print(p.volume, p.price_open)
```

---

## ✅ Deal

- **Định nghĩa:** Giao dịch đã khớp xong (dù lệnh còn hay đã đóng).

- **Truy xuất:** Qua `history_deals_get()`.

- **Ứng dụng:** Thống kê giao dịch, tạo báo cáo, tính lợi nhuận ròng.

---

## 📌 Tổng Kết

| Thuật ngữ        | Tác dụng trong code |
|------------------|----------------------|
| `symbol`         | Xác định tài sản giao dịch |
| `tick`           | Lấy giá mới nhất |
| `timeframe`      | Dữ liệu nến khung nào |
| `volume`         | Số lượng lệnh cần khớp |
| `ask/bid`        | Giá thực thi |
| `point`          | Bước giá nhỏ nhất |
| `spread`         | Tránh lệnh khi chi phí cao |
| `sl/tp`          | Kiểm soát rủi ro, chốt lời |
| `magic`          | Gắn nhãn cho chiến lược |
| `position`       | Quản lý lệnh đang chạy |
| `deal`           | Thống kê lịch sử giao dịch |

---