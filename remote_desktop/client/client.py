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
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.connect((host,port))
        self.have_pass = bool(self.server_socket.recv(1)[0])
        self.connected = True
        self.accepted = not self.have_pass
        self.capture = None

    def _send(self,mes):        
        message = pickle.dumps(mes)
        packet = struct.pack('Q',len(message))+message
        self.server_socket.sendall(packet)
        
    def get_request(self):
        header = struct.calcsize('Q')
        data = b''
        while True:
            while len(data)<header:
                data += self.server_socket.recv(4*1024)
            image_size = struct.unpack('Q',data[:header])[0]
            data = data[header:]
            while len(data) < image_size:
                data += self.server_socket.recv(4*1024)
            request = data[:image_size]
            data = data[image_size:]
            self.handle(pickle.loads(request))
    
        
    def handle(self,request):
        print(request['type'])
        if request['type']=='pass':
            self.handle_pass(request)
        # if request['type']=='screen':
        #     self.stream_screen(request)
        # elif 1:
        #     pass

    def handle_pass(self,request):
        self.accepted = request['status']

    def send_pass(self,password):
        if self.connected:
            mes = {
                'type':'pass',
                'password': password
            }
            self._send(mes)
        
    
    def update_capture(self, data_image):
        image = io.BytesIO(data_image)
        self.capture = Image.open(image)
        
    def stream_screen(self,request):
        self.update_capture(request['image'])
    
    def on_press(self,key):
        mes = {
            'type' : 'keyboard',
            'event' : 'press',
            'key' : key
        }
        
        self._send(mes)

    def on_release(self,key):
        mes = {
            'type' : 'keyboard',
            'event' : 'release',
            'key' : key
        }
        self._send(mes)
        
    def on_move(self,x, y):
        mes = {
            'type' : 'mouse',
            'event' : 'move',
            'key' : (x,y)
        }
        self._send(mes)

    def on_click(self,x, y, button, pressed):
        mes = {
            'type' : 'mouse',
            'key' : button
        }
        if pressed:
            mes['type']='press'
        else:
            mes['type']='release'
        self._send(mes)

    def on_scroll(self,x, y, dx, dy):
        mes = {
            'type' : 'mouse',
            'event' : 'move',
            'key' : (dx,dy)
        }
        self._send(mes)
    
    def keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while not self.accepted:
                pass
            listener.join()

    def mouse_listener(self):
        with mouse.Listener(on_click=self.on_click,on_move=self.on_move, on_scroll=self.on_scroll) as listener:
            while not self.accepted:
                pass
            listener.join()
            
    def run(self):
        Thread(target=self.get_request).start()
        Thread(target=self.mouse_listener).start()
        Thread(target=self.keyboard_listener).start()
                            

            
            
client = Client('127.0.0.1', 8888)
client.run()
client.send_pass('123456')