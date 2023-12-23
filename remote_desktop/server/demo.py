import socket
from PIL import ImageGrab
import io
import struct
from threading import Thread
from time import sleep, time
import pickle
import os
from pynput import keyboard,mouse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def capture_screen():
        # Chụp ảnh màn hình
        screen = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screen.save(img_byte_arr, format='JPEG', quality=0)
        return img_byte_arr.getvalue()
        # screen = ImageGrab.grab()
        # # screen = screen.resize(self.screen_size)
        # return screen

def _send(mes):        
        message = pickle.dumps(mes)
        packet = struct.pack('Q',len(message))+message

def stream_screen():
    last_frame_time = None
    while True:
        image = capture_screen()
        mes={
            'type':'screen',
            'image':image
        }
        _send(mes)
        current_time = time()

        if last_frame_time is not None:
            time_diff = current_time - last_frame_time
            fps = 1 / time_diff if time_diff > 0 else 0
            print(f"FPS: {fps}")

        last_frame_time = current_time
        
stream_screen()