# Giới thiệu

Mô-đun này cung cấp hai hàm tiện ích dùng để kết nối và ngắt kết nối với nền tảng MetaTrader 5 thông qua API chính thức `MetaTrader5` của MetaQuotes.

## Công dụng

- Tạo kết nối đến nền tảng MetaTrader 5 bằng tài khoản cá nhân
- Được gọi một lần duy nhất khi bắt đầu chạy chương trình
- Dễ dàng đóng kết nối khi hoàn tất hoặc ngắt ứng dụng
- Ghi log khi xảy ra lỗi trong quá trình khởi tạo

---

## Hàm chi tiết

### `def init_mt5(path: str, login: int, passw: str, server: str) -> bool`

**Mô tả**:  
Khởi tạo kết nối đến nền tảng MetaTrader 5 bằng các thông tin xác thực và đường dẫn đến terminal.

**Tham số**:

- `path` (`str`): Đường dẫn tới file thực thi terminal của MetaTrader (ví dụ: `"C:/Program Files/MetaTrader 5/terminal64.exe"`)
- `login` (`int`): ID đăng nhập tài khoản MetaTrader
- `passw` (`str`): Mật khẩu đăng nhập
- `server` (`str`): Tên server của sàn giao dịch (ví dụ: `"Exness-MT5Real"`)

**Trả về**:  
`True` nếu kết nối thành công, `False` nếu thất bại (và ghi log lỗi)

**Ví dụ**:

```python
success = init_mt5(
    path="C:/Program Files/MetaTrader 5/terminal64.exe",
    login=12345678,
    passw="mysecretpassword",
    server="Exness-MT5Real"
)

if not success:
    exit(1)
```

---

### `def shut_mt5() -> None`

**Mô tả**:  
Đóng kết nối với nền tảng MetaTrader 5 khi không còn cần thiết nữa.

**Ví dụ**:

```python
shut_mt5()
```

---

## Lưu ý

- Hàm `init_mt5` nên được gọi **trước tất cả các thao tác liên quan đến giao dịch hoặc lấy dữ liệu từ MT5**.
- Đảm bảo cài đặt module `MetaTrader5` bằng `pip install MetaTrader5`
- Nếu dùng trong hệ thống bất đồng bộ hoặc real-time, bạn nên đặt phần kết nối tại `startup` và đóng kết nối tại `shutdown`

---

## Gói liên quan

- `MetaTrader5` (PyPI): [MetaTrader5 5.0.5050](https://pypi.org/project/MetaTrader5/)
- `logging`: Ghi log lỗi trong quá trình kết nối không thành công
- **Tài liệu liên quan**: [MetaTrader module for integration with Python](https://www.mql5.com/en/docs/python_metatrader5)
