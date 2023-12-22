import socket
from PIL import ImageGrab
import io
import struct
from threading import Thread
from time import sleep
import pickle
import os
from pynput import keyboard,mouse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and not server.sending_file:
            file_path = event.src_path
            with open(file_path, 'rb') as file:
                data = file.read()
                print(f"File đã thay đổi: {file_path}")
                mes = {
                    'type' : 'file',
                    'event' : 'modified',
                    'data' : data,
                    'path' : file_path
                }
                server._send(mes)
                # sleep(5)
        
    def on_created(self, event):
        if not event.is_directory and not server.sending_file:
            file_path = event.src_path
            with open(file_path, 'rb') as file:
                data = file.read()
                print(f"{file_path} đã được tạo!")
                mes = {
                    'type' : 'file',
                    'event' : 'created',
                    'data' : data,
                    'path' : file_path
                }
                server._send(mes)
                # sleep(5)

    def on_deleted(self, event):
        if not event.is_directory and not server.sending_file:
            print(f"{event.src_path} đã bị xóa!")
            mes = { 
                'type' : 'file',
                'event' : 'deleted',
                'path' : event.src_path
            }   
            server._send(mes)
            # sleep(5)
class Server:
    def __init__(self,host,port,password="") -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host=host
        self.port=port
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_socket, self.client_address = None,None
        self.connected = False
        self.live = False
        self.have_pass=True
        self.accept_pass=False
        self.password = '123456'
        self.fps = 60
        self.file_async = False
        self.sending_file = False
        self.screen_size = (800,600)

    def connect(self):
        while True:
            if not self.connected:
                
                print('Wait connect!')
                self.client_socket, self.client_address = self.server_socket.accept()
                print('Connected!')
                sleep(1)
                self.client_socket.sendall(bytes([self.have_pass]))
                self.connected=True
                if not self.have_pass:
                    self.live=True
                    self.accept_pass=True
        
    def _send(self,mes):
        if not self.connected:
            return
        message = pickle.dumps(mes)
        packet = struct.pack('Q',len(message))+message
        self.client_socket.sendall(packet)
    
    def get_request(self):
        header = struct.calcsize('Q')
        data = b''
        while True:
            if self.connected:
                while len(data)<header:
                    data += self.client_socket.recv(4*1024)
                image_size = struct.unpack('Q',data[:header])[0]
                data = data[header:]
                while len(data) < image_size:
                    data += self.client_socket.recv(4*1024)
                request = data[:image_size]
                data = data[image_size:]
                self.handle(pickle.loads(request))
    
        
    def handle(self,request):
        if request['type']=='file':
            print(request)
        if request['type']=='pass':
            self.handle_pass(request['password'])
        elif request['type']=='disconnect':
            self.disconnect()
        elif request['type']=='file':
            self.handle_file(request)
        elif request['type']=='mouse':
            self.handle_mouse(request['key'],request['type'])
        elif request['type']=='keyboard':    
            self.handle_keyboard(request['key'],request['type'])

        
    
    def capture_screen(self):
        # Chụp ảnh màn hình
        # screen = ImageGrab.grab()
        # img_byte_arr = io.BytesIO()
        # screen.save(img_byte_arr, format='JPEG')
        # return img_byte_arr.getvalue()
        screen = ImageGrab.grab()
        # screen = screen.resize(self.screen_size)
        return screen

    def stream_screen(self):
        while True:
            if self.connected and self.live:
                image = self.capture_screen()
                mes={
                    'type':'screen',
                    'image':image
                }
                self._send(mes)
                sleep(1/self.fps)
    
    def handle_keyboard(self,type,key):
        controller = keyboard.Controller()
        print(key)
        if type=='press':
            print(key)
            controller.press(key)
        else:
            controller.release(key)
            
    def handle_mouse(self,type,key):
        controller = mouse.Controller()
        if type=='move':
            controller.position = (key[0],key[1])
        elif type=='press':
            controller.press(key)
        elif type=='release':
            controller.release(key)
        else:
            controller.scroll(dx=key[0],dy=key[1])
            
    def checkpass(self,password):
        if not self.have_pass:
            return True
        if self.password==password:
            return True
        return False
    
    def handle_pass(self,password):
        if self.checkpass(password):
            self.accept_pass=True
            self.live=True
            mes={
                'type':'pass',
                'status':True
            }
            self._send(mes)
        else:
            mes={
                'type':'pass',
                'status':False
            }
            self._send(mes)
                
    def disconnect(self):
        mes={
            'type':'disconnect'
        }
        self._send(mes)
        self.connected=False
        self.live=False
        self.accept_pass=False
        sleep(5)
        self.client_socket.close()
        # self.server_socket.close()
    
    def async_file(self):
        path = "./async"
        if not os.path.exists(path):
            os.makedirs(path)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()

        try:
            while self.file_async:
                sleep(1)
            observer.stop()
        except KeyboardInterrupt:
            observer.stop()
                
    def handle_file(self,mes):
        # if not os.path.exists(mes['path']) and mes['path'] != '':
        #     os.makedirs(mes['path'])
        self.sending_file = True
        if mes['event']=='created':
            with open(mes['path'], 'wb') as file:
                file.write(mes['data'])
        elif mes['event']=='modified':
            with open(mes['path'], 'wb') as file:
                file.write(mes['data'])
        elif mes['event']=='deleted':
            os.remove(mes['path'])
        sleep(3)
        self.sending_file = False
    
    def start_sync(self):
        self.file_async = True
        Thread(target=self.async_file).start()
    
    def stop_sync(self):
        self.file_async = False
    
    def run(self):
        Thread(target=self.connect).start()
        Thread(target=self.stream_screen).start()
        Thread(target=self.get_request).start()
    
server = Server('127.0.0.1', 8888)
server.run()
server.start_sync()
sleep(50)
server.stop_sync()