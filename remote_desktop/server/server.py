import socket
from PIL import ImageGrab
import io
import struct
from threading import Thread
from time import sleep
import pickle
from pynput import keyboard,mouse

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
        print(request)
        if request['type']=='pass':
            self.handle_pass(request['password'])
        elif request['type']=='disconnect':
            self.disconnect()
        # if request['devide']==2:
        #     self.handle_pass(request['password'])
        # elif request['device']==0:
        #     self.handle_keyboard(request['type'],request['key'])
        # elif request['device']==1:
        #     self.handle_mouse(request['type'],request['key'])
        # elif request['device']==3:
        #     self.disconnect()
        
    
    def capture_screen(self):
        # Chụp ảnh màn hình
        screen = ImageGrab.grab()
        img_byte_arr = io.BytesIO()
        screen.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def stream_screen(self):
        while True:
            if self.connected and self.live:
                image = self.capture_screen()
                mes={
                    'type':'screen',
                    'image':image
                }
                self._send(mes)
                sleep(1/60)
    
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
            controller.position = (key[0],key[1])
        elif type==1:
            controller.press(key)
        elif type==2:
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
    
                 
    def run(self):
        Thread(target=self.connect).start()
        Thread(target=self.stream_screen).start()
        Thread(target=self.get_request).start()
    
server = Server('127.0.0.1', 8888)
server.run()