# Remote Desktop

Remote Desktop là một dự án cho phép bạn điều khiển máy tính từ xa thông qua mạng internet.

## Cài đặt

Đầu tiên, hãy cài đặt các thư viện cần thiết bằng cách chạy lệnh sau:

```sh
pip install -r requirements.txt

Sử dụng
Server
Để khởi chạy server, hãy chạy hàm main trong file server.py:

Client
Để kết nối với server từ client, hãy chạy hàm main trong file client.py:

Sau khi kết nối, bạn có thể sử dụng các phương thức như send_pass để gửi mật khẩu hoặc disconnect để ngắt kết nối.

Lưu ý
Đảm bảo rằng cả client và server đều có quyền truy cập vào các tệp và thư mục cần thiết. Nếu không, bạn có thể gặp lỗi trong quá trình chạy.

```