# pyta-trader

`pyta-trader` là một framework giao dịch được viết bằng Python nhằm hỗ trợ xây dựng các chiến lược giao dịch tự động thông qua việc tích hợp với MetaTrader 5 (MT5). Dự án cung cấp các công cụ để lấy dữ liệu thị trường, phân tích biến động giá và thực hiện lệnh giao dịch hoàn toàn tự động.

---

## ⚙️ Tính năng chính

- **Tích hợp MT5:** Kết nối trực tiếp với MetaTrader 5 để nhận dữ liệu thời gian thực và đặt lệnh.
- **Quản lý biểu đồ:** Cập nhật và lấy dữ liệu nến một cách hiệu quả.
- **Thiết kế mô-đun:** Cấu trúc rõ ràng, dễ bảo trì và mở rộng.

---

## 🚀 Bắt đầu sử dụng

### Yêu cầu

- Python 3.13 trở lên
- Đã cài đặt phần mềm MetaTrader 5 và đăng nhập tài khoản

### Cấu hình

Đổi tên file `.sample.env` thành `.env` và điền đầy đủ các thông tin cấu hình như:
```dotenv
MT5_LOGIN=...
MT5_PASSWORD=...
MT5_SERVER=...
```

---

## 📘 Tài liệu hỗ trợ lập trình viên

Nếu bạn mới bắt đầu lập trình giao dịch hoặc cần hiểu rõ các khái niệm trong hệ thống như `symbol`, `lot`, `spread`, `SL/TP`, `magic number`, v.v... hãy xem tài liệu sau:

📎 [📚 Từ điển Thuật Ngữ Giao Dịch (Trading Terms)](docs/trading_terms.md)

Tài liệu này sẽ giúp bạn hiểu ý nghĩa từng thuật ngữ và cách sử dụng chúng một cách hiệu quả khi làm việc với API MetaTrader5 trong Python.

---

## 🧪 Chạy test

```bash
python -m unittest discover -s test
```

---

## 📄 Giấy phép

Dự án này được cấp phép theo [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh!  
Hãy fork repository và tạo pull request nếu bạn có bất kỳ cải tiến hoặc sửa lỗi nào.
