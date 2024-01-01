import ctypes

# Ẩn con trỏ chuột
ctypes.windll.user32.ShowCursor(False)

# Đoạn mã để giữ cho ứng dụng chạy
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Hiện con trỏ chuột trở lại trước khi thoát
    ctypes.windll.user32.ShowCursor(True)