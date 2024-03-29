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
import screeninfo

sizefile = 100*1024

class MyHandler(FileSystemEventHandler):
    def __init__(self,server) -> None:
        self.server = server
    def on_modified(self, event):
        try:
            if not event.is_directory and not self.server.sending_file:
                sleep(1)
                file_path = event.src_path
                with open(file_path, 'rb') as file:
                    data = file.read()
                    print(f"File đã thay đổi: {file_path}")
                    mes = {
                        'type': 'file',
                        'event': 'modified',
                        'data': data,
                        'path': file_path
                    }
                    self.server._send(mes)
        except:
            pass

    def on_created(self, event):
        try:
            if not event.is_directory and not self.server.sending_file:
                sleep(1)
                file_path = event.src_path
                with open(file_path, 'rb') as file:
                    data = file.read()
                    print(f"{file_path} đã được tạo!")
                    mes = {
                        'type': 'file',
                        'event': 'created',
                        'data': data,
                        'path': file_path
                    }
                    self.server._send(mes)
        except:
            pass

    def on_deleted(self, event):
        try:
            if not event.is_directory and not self.server.sending_file:
                sleep(1)
                print(f"{event.src_path} đã bị xóa!")
                mes = {
                    'type': 'file',
                    'event': 'deleted',
                    'path': event.src_path
                }
                self.server._send(mes)
        except:
            pass
class Client:
    def __init__(self,host,port=8888) -> None:
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.have_pass = None
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
        temp = Image.new('RGB', (screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height),'black')
        ioo = io.BytesIO()
        temp.save(ioo, format='JPEG')
        self.capture = ioo.getvalue()
        self.recording = False
        self.file_async = False 
        self.fps = 30
        self.controling = False
        self.sending_file = False
        self.running = False
        self.last_frame_time = time()
        self.x, self.y, self.height, self.width = 0, 0, 0, 0
        self.lasttime = time()
        self.press = False
        self.listener_key = None
        self.listener_mouse = None
        self.path = './async'
        self.start_time = time()
        self.count = 0
        self.have_focus = True
        self.list_file = None

    def _send(self,mes): 
        try:   
            if not self.connected:
                return
            # print(mes['type'])
            message = pickle.dumps(mes)
            packet = struct.pack('Q',len(message))+message
            self.server_socket.sendall(packet)
        except:
            # print(3)
            self.connected = False
            self.disconnect()
        
    def get_request(self):
        global sizefile
        header = struct.calcsize('Q')
        data = b''
        while not self.connected:
            sleep(1)
        while self.connected:
            try:
                while len(data)<header:
                    data += self.server_socket.recv(sizefile)
                image_size = struct.unpack('Q',data[:header])[0]
                data = data[header:]
                while len(data) < image_size:
                    data += self.server_socket.recv(sizefile)
                request = data[:image_size]
                data = data[image_size:]
                self.handle(pickle.loads(request))
            except Exception as e:
                # print(2)
                # self.connected = False
                # self.disconnect()
                pass
            
    def change_size_screen(self,size):
        width = int(size.split(' ')[0])
        mes = {
            'type' : 'screen_size',
            'width' : width
        }
        self._send(mes)

    def handle(self,request):
        # print(request)
        # if request['type']=='file':
        #     print(request)
        if request['type']=='pass':
            self.handle_pass(request)
        elif request['type']=='disconnect':
            self.handle_disconnect()
        elif request['type']=='file':
            self.handle_file(request)
        elif request['type']=='keylog':
            self.handle_keylog(request)
        elif request['type']=='query_file':
            self.handle_query_file(request)
        elif request['type']=='update_file':
            self.file_update(request)
        elif request['type']=='send_file':
            self.receive_file(request)
        elif request['type']=='need_file':
            self.handle_need_file(request)
        # elif 1:
        #     pass
        
    def need_file(self,path1,path2):
        mes = {
            'type' : 'need_file',
            'path1' : path1,
            'path2' : path2
        }
        self._send(mes)
        
    def handle_need_file(self,mes):
        self.send_file(mes['path1'],mes['path2'])

    def send_file(self,path1,path2):
        file_name = os.path.basename(path1)
        path2 = os.path.join(path2,file_name)
        with open(path1,'rb') as file:
            data = file.read()
            mes = {
                'type' : 'send_file',
                'data' : data,
                'path' : path2
            }
            # print(mes)
            self._send(mes)
            
    def receive_file(self,message):
        with open(message['path'],'wb') as file:
            file.write(message['data'])
        
    
    def query_file(self,path):
        mes = {
            'type' : 'query_file',
            'path' : path
        }
        self._send(mes)
    
    def file_update(self,mes):
        self.list_file  = mes['files']
    
    def handle_pass(self,request):
        # print(request['status'])
        self.accepted = request['status']

    def on_mouse(self):
        mes = {
            'type' : 'off_mouse',
            'event' : 'on'
        }
        self._send(mes)
    
    def off_mouse(self):
        mes = {
            'type' : 'off_mouse',
            'event' : 'off'
        }
        self._send(mes)
        
    def on_keyboard(self):
        mes = {
            'type' : 'off_keyboard',
            'event' : 'on'
        }
        self._send(mes)
    
    def handle_query_file(self,mes):
        self.update_file(mes['path'])
    
    def update_file(self,path):
        if path == '':
            import ctypes
            import string

            # Lấy bitmask của các ổ đĩa
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()

            # Tạo danh sách các ổ đĩa
            drives = list()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(letter + ":\\")
                bitmask >>= 1
                
            list_file = []
            for drive in drives:
                mes = {
                    'path' : drive,
                    'type' : 'folder',
                    'name' : drive[0]+':'
                }
                list_file.append(mes)
            mes = {
                'type' : 'update_file',
                'files' : list_file
            }
            self._send(mes)
            return
        
        list_file = []
        try:
            entries = os.listdir(path)
            for entry in entries:
                full_path = os.path.join(path, entry)
                file = {
                    'name' : entry,
                    'path' : full_path,
                }
                if os.path.isfile(full_path):
                    file['type'] = 'file'
                elif os.path.isdir(full_path):
                    file['type'] = 'folder'
                list_file.append(file)
        except:
            pass
        finally:
            mes = {
                'type' : 'update_file',
                'files' : list_file
            }
            self._send(mes)
        
    def off_keyboard(self):
        mes = {
            'type' : 'off_keyboard',
            'event' : 'off'
        }
        self._send(mes)
    
    def send_pass(self,password):
        if self.connected:
            mes = {
                'type':'pass',
                'password': password
            }
            self._send(mes) 
        

    def update_capture(self, dimage):
        # image = io.BytesIO(dimage)
        # self.capture = Image.open(image)
        self.capture = dimage
    
    def recive_screen(self):
        global sizefile
        header = struct.calcsize('Q')
        data = b''
        while not self.connected or not self.accepted:
            sleep(1)
        skserver_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        skserver_socket.connect((self.host, 8889))
        while self.connected:
            try:
                while len(data)<header:
                    data += skserver_socket.recv(sizefile)
                image_size = struct.unpack('Q',data[:header])[0]
                data = data[header:]
                while len(data) < image_size:
                    data += skserver_socket.recv(sizefile)
                request = data[:image_size]
                data = data[image_size:]
                self.stream_screen(pickle.loads(request))
            except:
                # print(1)
                # self.connected = False
                # self.disconnect()
                pass
        
    
    def stream_screen(self,image):
        self.update_capture(image)
        self.count += 1
        current_time = time()

        if current_time - self.start_time >= 1:
            self.fps = self.count/(current_time - self.last_frame_time)
            self.count = 0
            self.last_frame_time = current_time
            # print(f"FPS: {fps}")
    
    def on_press(self,key):
        if not self.have_focus:
            return
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
        if not self.have_focus:
            return
        if x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height:
            return
        current_time = time()
        if current_time - self.lasttime > 0.08:
            # Gửi cập nhật
            self.lasttime = current_time
            x=(x-self.x)/self.width
            y=(y-self.y)/self.height
            mes = {
                'type' : 'mouse',
                'event' : 'move',
                'key' : (x,y),
                'pos' : (x,y)
            }
            self._send(mes)

    def on_click(self,x, y, button, pressed):
        if not self.have_focus:
            return
        if x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height:
            return
        x=(x-self.x)/self.width
        y=(y-self.y)/self.height
        # print(f'{button} click at {x} {y} of screen')
        mes = {
            'type' : 'mouse',
            'key' : button,
            'pos' : (x,y)
        }
        if pressed:
            mes['event']='press'
            self.press = True
        else:
            mes['event']='release'
            self.press = False
        self._send(mes)

    def on_scroll(self,x, y, dx, dy):
        if not self.have_focus:
            return
        if x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height:
            return
        x=(x-self.x)/self.width
        y=(y-self.y)/self.height
        # print(f'scroll {dx},{dy} at {x} {y} of screen')
        mes = {
            'type' : 'mouse',
            'event' : 'scroll',
            'key' : (dx,dy),
            'pos' : (x,y)
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
        while not self.accepted or not self.connected:
            sleep(1)
        self.listener_key = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener_key.start()
        
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
            
    def screen_record(self,fps=30):
        self.recording = True
        frames = []
        while self.recording:
            if self.capture is not None:
                image_array = np.frombuffer(self.capture, np.uint8)
                # Đọc mảng numpy với OpenCV để tạo ảnh
                frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(np.array(frame))
                sleep(1/fps)

        height, width, layers = frames[0].shape
        current_time = datetime.datetime.now()
        video_name = "./video_image/"+current_time.strftime("%Y-%m-%d_%H-%M-%S.mp4")
        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (width, height))

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
            pic_name = "./video_image/"+ current_time.strftime("%Y-%m-%d_%H-%M-%S.png")
            file = io.BytesIO(self.capture)
            image = Image.open(file)
            image.save(pic_name)
            
    def handle_keylog(self,mes):
        print(mes['event'])
    
    def disconnect(self):    
        # print('disconnect') 
        mes={'type':'disconnect'}
        self._send(mes)
        if not self.connected:
            try:
                self.server_socket.close()
            except:
                pass
            finally:
                self.server_socket = None
    def handle_disconnect(self):
        self.connected = False
        sleep(3)
        try:
            self.server_socket.close()
        except:
            pass
        finally:
            self.server_socket = None

    def async_file(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for item in os.listdir(self.path):
            item_path = os.path.join(self.path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
        event_handler = MyHandler(self)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=False)
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
        sleep(3)
        self.sending_file = False
            
    def start_sync(self):
        self.file_async = True
        Thread(target=self.async_file).start()
    
    def stop_sync(self):
        self.file_async = False

    
    def run_screen(self):
        self.running = True
        Thread(target=self.get_request).start()
        Thread(target=self.recive_screen).start()
    
    def run_listener(self):
        Thread(target=self.keyboard_listener).start()
        Thread(target=self.mouse_listener).start()
        
    def stop_run(self):
        # self.running = False
        if self.listener_key is not None:
            self.listener_key.stop()
        if self.listener_mouse is not None:
            self.listener_mouse.stop()
  
# client = Client('127.0.0.1', 8888)
# client.run_screen()
# client.start_sync()
# # client.disconnect()
