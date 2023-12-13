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

class Client:
    def __init__(self,host,port) -> None:
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((host,port))
        self.capture = None
        
    def _send(self,device, type, key):
        mes = {
            'device' : device,
            'type' : type,
            'key' : key
        }
        
        message = pickle.dumps(mes)
        packet = struct.pack('Q',len(message))+mehellohjhjjhjkjkjkhkjhhjkjhjkjhdsfefdsefdsesffdsef
        self.client_socket.sendall(packet)
    
    def update_capture(self, data_image):
        image = io.BytesIO(data_image)
        self.capture = Image.open(image)
        
    def stream_screen(self):
        header = struct.calcsize('Q')
        data = b''
        while True:
            while len(data)<header:
                data += self.client_socket.recv(4*1024)
            image_size = struct.unpack('Q',data[:header])[0]
            data = data[header:]
            while len(data) < image_size:
                data += self.client_socket.recv(4*1024)
            image = data[:image_size]
            data = data[image_size:]
            self.update_capture(image)
            
    def run(self):
        Thread(target=self.stream_screen).start()
        Thread(target=self.mouse_listener).start()
        Thread(target=self.keyboard_listener).start()
                
    def on_press(self,key):
        self._send(0,0,key)

    def on_release(self,key):
        self._send(0,1,key)
        
    def on_move(self,x, y):
        self._send(1,0,(x,y))

    def on_click(self,x, y, button, pressed):
        if pressed:
            self._send(1,1,(button))
        else:
            self._send(1,2,(button))

    def on_scroll(self,x, y, dx, dy):
        self._send(1,3,(dx, dy))
    
    def keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def mouse_listener(self):
        with mouse.Listener(on_click=self.on_click,on_move=self.on_move, on_scroll=self.on_scroll) as listener:
            listener.join()

            
            
client = Client('192.168.132.174', 8888)
client.run()