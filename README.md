# Remote Desktop

Remote Desktop là một dự án cho phép bạn điều khiển máy tính từ xa thông qua mạng internet.

Đây là một dự án cho phép bạn...

## Cài đặt

```sh
git clone https://github.com/HoKhanhDyu/remote-desktop.git
cd remote-desktop
```

Đầu tiên, hãy cài đặt các thư viện cần thiết bằng cách chạy lệnh sau:

```sh
pip install -r requirements.txt
```

## Sử dụng

### Server
Để khởi chạy server, hãy chạy hàm main trong file server.py:
```sh
python remote_desktop/server/main.py
```

### Client
Để kết nối với server từ client, hãy chạy hàm main trong file client.py:
```sh
python remote_desktop/client/main.py
```
