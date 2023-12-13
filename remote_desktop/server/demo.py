from pynput.keyboard import Listener

def on_press(key):
    print(key)
    try:
        print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def on_release(key):
    print(f'Key {key} released')
    # Bạn có thể thêm điều kiện để thoát vòng lặp lắng nghe ở đây
    # Ví dụ: if key == keyboard.Key.esc:dcsx    -+
    231
    #            return False

# Thiết lập Listener để lắng nghe các sự kiện bàn phím
with Listener(on_press=on_press, on_release=on_release,suppress=True) as listener:
    listener.join()
    