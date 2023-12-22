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

class Client:
    def __init__(self,host,port) -> None:
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.connect((host,port))
        sleep(1)
        self.have_pass = bool(self.server_socket.recv(1)[0])
        self.connected = True
        self.accepted = not self.have_pass
        self.capture = None
        self.recording = False

    def _send(self,mes):        
        if not self.connected:
            return
        message = pickle.dumps(mes)
        packet = struct.pack('Q',len(message))+message
        self.server_socket.sendall(packet)
        
    def get_request(self):
        header = struct.calcsize('Q')
        data = b''
        while not self.connected:
            pass
        while self.connected:
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
        elif request['type']=='screen':
            self.stream_screen(request)
        elif request['type']=='disconnect':
            self.handle_disconnect()
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
        
    
    def update_capture(self, dimage):
        image = io.BytesIO(dimage)
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
        # with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #     while not self.accepted or not self.connected:
        #         pass
        #     listener.join()
        #     while self.connected:  
        #         pass 
        #     listener.stop()
        # print(2)
        while not self.accepted or not self.connected:
            pass
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        while self.connected:
            pass
        self.listener.stop()
        
    def mouse_listener(self):
        # with mouse.Listener(on_click=self.on_click,on_move=self.on_move, on_scroll=self.on_scroll) as listener:
        #     while not self.accepted or not self.connected:
        #         pass
        #     listener.join()
        #     while self.connected:  
        #         pass 
        #     listener.stop()
        # print(3)
        while not self.accepted or not self.connected:
            pass
        self.listener = mouse.Listener(on_click=self.on_click,on_move=self.on_move, on_scroll=self.on_scroll)
        self.listener.start()
        while self.connected:
            pass
        self.listener.stop()
            
    def screen_record(self,fps=30):
        self.recording = True
        frames = []
        while self.recording:
            if self.capture is not None:
                frame=np.array(self.capture)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(np.array(frame))

        height, width, layers = frames[0].shape
        current_time = datetime.datetime.now()
        video_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.mp4")
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        for frame in frames:
            video.write(frame)

        cv2.destroyAllWindows()
        video.release()

        
        
    def start_record(self):
        Thread(target=self.screen_record).start()
        
    def stop_record(self):
        self.recording = False
        
    def save_screen(self):
        if self.capture is not None:
            current_time = datetime.datetime.now()
            pic_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.png")
            self.capture.save(pic_name)
    
    def disconnect(self):     
        mes={'type':'disconnect'}
        self._send(mes)
        self.connected = False
        sleep(3)
        
    def handle_disconnect(self):
        self.server_socket.close()
    
    def run(self):
        Thread(target=self.get_request).start()
        Thread(target=self.mouse_listener).start()
        Thread(target=self.keyboard_listener).start()
                            

            
            
client = Client('192.168.100.10', 8888)
client.run()
client.send_pass('123456')
sleep(5)
client.disconnect()