import socket
import struct
from PIL import Image
import io
from threading import Thread
from time import sleep, time
import numpy as np
from pynput import keyboard
from pynput import mouse
import pickle
import cv2
import os
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sizefile = 100*1024

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and not client.sending_file:
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
                client._send(mes)
                # sleep(5)
        
    def on_created(self, event):
        if not event.is_directory and not client.sending_file:
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
                client._send(mes)
                # sleep(5)

    def on_deleted(self, event):
        if not event.is_directory and not client.sending_file:
            print(f"{event.src_path} đã bị xóa!")
            mes = { 
                'type' : 'file',
                'event' : 'deleted',
                'path' : event.src_path
            }   
            client._send(mes)
            # sleep(5)r
class Client:
    def __init__(self,host,port=8888) -> None:
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.server_socket.connect((host, port))
            sleep(1)
            self.have_pass = bool(self.server_socket.recv(1)[0])
            self.connected = True
        except socket.error:
            self.server_socket = None
            self.connected = False
            return None
        self.accepted = not self.have_pass
        self.capture = None
        self.recording = False
        self.file_async = False 
        self.fps = 60
        self.controling = False
        self.sending_file = False
        self.running = False
        self.last_frame_time = None
        self.x, self.y, self.height, self.width = 0, 0, 0, 0

    def _send(self,mes):        
        if not self.connected:
            return
        print(mes['type'])
        message = pickle.dumps(mes)
        packet = struct.pack('Q',len(message))+message
        self.server_socket.sendall(packet)
        
    def get_request(self):
        global sizefile
        header = struct.calcsize('Q')
        data = b''
        while not self.connected:
            pass
        while self.connected:
            while len(data)<header:
                data += self.server_socket.recv(sizefile)
            image_size = struct.unpack('Q',data[:header])[0]
            data = data[header:]
            while len(data) < image_size:
                data += self.server_socket.recv(sizefile)
            request = data[:image_size]
            data = data[image_size:]
            self.handle(pickle.loads(request))

    def handle(self,request):
        # print(request['type'])
        if request['type']=='file':
            print(request)
        if request['type']=='pass':
            self.handle_pass(request)
        elif request['type']=='screen':
            self.stream_screen(request)
        elif request['type']=='disconnect':
            self.handle_disconnect()
        elif request['type']=='file':
            self.handle_file(request)
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
        # self.capture = image
        
    def stream_screen(self,request):
        self.update_capture(request['image'])
        current_time = time()

        if self.last_frame_time is not None:
            time_diff = current_time - self.last_frame_time
            fps = 1 / time_diff if time_diff > 0 else 0
            # print(f"FPS: {fps}")

        self.last_frame_time = current_time
    
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
        if x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height:
            return
        x=x-self.x/self.width*1920
        y=y-self.y/self.height*1080
        mes = {
            'type' : 'mouse',
            'event' : 'move',
            'key' : (x,y)
        }
        self._send(mes)

    def on_click(self,x, y, button, pressed):
        if x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height:
            return
        x=x-self.x/self.width*1920
        y=y-self.y/self.height*1080
        mes = {
            'type' : 'mouse',
            'key' : button
        }
        if pressed:
            mes['event']='press'
        else:
            mes['event']='release'
        self._send(mes)

    def on_scroll(self,x, y, dx, dy):
        if x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height:
            return
        x=x-self.x/self.width*1920
        y=y-self.y/self.height*1080
        mes = {
            'type' : 'mouse',
            'event' : 'scroll',
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
            sleep(1)
        self.listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener_key.start()
        while self.connected and self.accepted and self.running:
            sleep(1)
        self.listener_key.stop()
        
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
            sleep(1)
        self.listener_mouse = mouse.Listener(on_click=self.on_click,on_move=self.on_move, on_scroll=self.on_scroll)
        self.listener_mouse.start()
        while self.connected and self.accepted and self.running:
            sleep(1)
        self.listener_mouse.stop()
            
    def screen_record(self,fps=60):
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
        print('disconnect') 
        mes={'type':'disconnect'}
        self._send(mes)
        
    def handle_disconnect(self):
        self.connected = False
        sleep(3)
        self.server_socket.close()

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
        if mes['event']=='modified':
            with open(mes['path'],'wb') as file:
                file.write(mes['data'])
        elif mes['event']=='created':
            with open(mes['path'],'wb') as file:
                file.write(mes['data'])
        elif mes['event']=='deleted':
            os.remove(mes['path'])
        sleep(5)
        self.sending_file = False
            
    def start_sync(self):
        self.file_async = True
        Thread(target=self.async_file).start()
    
    def stop_sync(self):
        self.file_async = False
        
    def show_fullscreen_video(self):
        # Tạo cửa sổ với thuộc tính toàn màn hình
        cv2.namedWindow("Server", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Server", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            frame=np.array(self.capture)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # self.capture.show()
            cv2.imshow("Server", frame)
            # Thoát khi nhấn phím 'q' hoặc kết thúc video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Khi xong, giải phóng và đóng tất cả
        cv2.destroyAllWindows()

    
    def run_screen(self):
        self.running = True
        Thread(target=self.get_request).start()
    
    def run_listener(self):
        Thread(target=self.keyboard_listener).start()
        Thread(target=self.mouse_listener).start()
        
    def stop_run(self):
        self.running = False
        if self.listener_key is not None:
            self.listener_key.stop()
        if self.listener_mouse is not None:
            self.listener_mouse.stop()
        
        
                            

            
            
# client = Client('127.0.0.1', 8888)
# client.run()
# client.send_pass('zx')    
# sleep(3)
# client.send_pass('zxc')
# sleep(5)
# client.disconnect()
