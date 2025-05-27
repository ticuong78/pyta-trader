# Hướng dẫn sử dụng

## class Chart

class cung cấp các hàm truy xuất dữ liệu của biểu đồ thông qua nền tảng Meta Trader, để chạy cần setup Meta Trader tại máy
dùng init_chart() để lấy 100 giá đầu tiên, thêm vào prices trong Chart.
Để cập nhật thông tin giá mới, dùng check_and_update_chart()
Để lấy giá, dùng get_chart() trả về một mảng số thực
