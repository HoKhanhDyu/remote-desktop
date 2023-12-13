import socket
from PIL import ImageGrab
import io
import struct
from threading import Thread
from time import sleep
import pickle
from pynput import keyboard,mouse

class Server:
    def __init__(self,host,port) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print("Waiting for a connection...")
        self.client_socket, self.client_address = self.server_socket.accept()
        print("Accepted connection from {}:{}".format(*self.client_address))
        self.live = True
    def capture_screen(self):
        # Chụp ảnh màn hình
        screen = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screen.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def stream_screen(self):
        while self.live:
            image = self.capture_screen()
            message = struct.pack('Q',len(image))+image
            self.client_socket.send(message)
            # sleep(1/120)
    
    def handle_keyboard(self,type,key):
        controller = keyboard.Controller()
        print(key)
        if type==0:
            print(key)
            controller.press(key)
        else:
            controller.release(key)
            
    def handle_mouse(self,type,key):
        controller = mouse.Controller()
        if type==0:
            controller.move(dx=key[0],dy=key[1])
        elif type==1:
            controller.press(key)
        elif type==2:
            controller.release(key)
        else:
            controller.scroll(dx=key[0],dy=key[1])
    
    def handle(self,request):
        print(request)
        # if request['device']==0:
        #     self.handle_keyboard(request['type'],request['key'])
        # elif request['device']==1:
        #     self.handle_mouse(request['type'],request['key'])
    
    def get_request(self):
        header = struct.calcsize('Q')
        data = b''
        while True:
            while len(data)<header:
                data += self.client_socket.recv(4*1024)
            image_size = struct.unpack('Q',data[:header])[0]
            data = data[header:]
            while len(data) < image_size:
                data += self.client_socket.recv(4*1024)
            request = data[:image_size]
            data = data[image_size:]
            self.handle(pickle.loads(request))
           
        
        
    def run(self):
        Thread(target=self.stream_screen).start()
        Thread(target=self.get_request).start()
        
        sleep(20)
        return
    
server = Server('127.0.0.1', 8888)
server.run()