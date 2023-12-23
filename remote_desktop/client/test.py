import socket
import struct
from PIL import Image
import io
from threading import Thread
from time import sleep
import numpy as np
from pynput import keyboard
from pynput import mouse
import pickle
import cv2
import os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


cv2.namedWindow("Server", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Server", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

frame = cv2.imread("Screenshot 2023-12-23 092811.png")

cv2.imshow("Server", frame)

# Thoát khi nhấn phím 'q' hoặc kết thúc video
cv2.waitKey(0)
# Khi xong, giải phóng và đóng tất cả
cv2.destroyAllWindows()