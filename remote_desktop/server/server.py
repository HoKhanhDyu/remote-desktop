import socket
from PIL import ImageGrab
import io
import struct
from threading import Thread
from time import sleep, time
import pickle
import os
from pynput import keyboard, mouse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import screeninfo
from pynput import mouse


packet_size = 100 * 1024


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


class Server:
    def __init__(self, host, port=8888, password=""):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.sksend_screen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sksend_screen.bind((self.host, 8889))
        self.sksend_screen.listen(5)
        self.server_socket.settimeout(5)
        self.client_socket, self.client_address = None, None
        self.connected = False
        self.live = False
        self.have_pass = False
        self.accept_pass = False
        self.password = password
        self.fps = 60
        self.file_async = False
        self.sending_file = False
        self.screen_size = (screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height)
        self.last_frame_time = None
        self.wait_connect = False
        self.event_handle = True
        self.send_screen = True
        self.turn_off_mouse = mouse.Listener(suppress=True)
        self.turn_off_keyboard = keyboard.Listener(suppress=True)
        self.path = "./async"
    def connect(self):
        while True:
            if not self.connected and self.wait_connect:
                try:
                    print('Wait connect!')
                    self.client_socket, self.client_address = self.server_socket.accept()
                    print('Connected!')
                    sleep(1)
                    self.client_socket.sendall(bytes([self.have_pass]))
                    self.connected = True
                    if not self.have_pass:
                        self.live = True
                        self.accept_pass = True
                except:
                    pass
            else:
                if not self.wait_connect:
                    return
                sleep(1)

    def _send(self, mes):
        try:
            if not self.connected:
                return
            message = pickle.dumps(mes)
            packet = struct.pack('Q', len(message)) + message
            self.client_socket.sendall(packet)
            current_time = time()

            if self.last_frame_time is not None:
                time_diff = current_time - self.last_frame_time
                fps = 1 / time_diff if time_diff > 0 else 0
                # print(f"FPS: {fps}")

            self.last_frame_time = current_time
        except:
            self.disconnect()
            self.wait_connect=False
            sleep(5)
            self.wait_connect=True
            self.run()

    def get_request(self):
        header = struct.calcsize('Q')
        data = b''
        while True:
            try:
                if self.connected:
                    while len(data) < header:
                        data += self.client_socket.recv(packet_size)
                    image_size = struct.unpack('Q', data[:header])[0]
                    data = data[header:]
                    while len(data) < image_size:
                        data += self.client_socket.recv(packet_size)
                    request = data[:image_size]
                    data = data[image_size:]
                    self.handle(pickle.loads(request))
                else:
                    if not self.wait_connect:
                        return
                    sleep(1)
            except:
                sleep(1)
    
    def handle(self, request):
        if request['type'] == 'pass':
            self.handle_pass(request['password'])
        elif request['type'] == 'disconnect':
            self.disconnect()
        elif request['type'] == 'file':
            self.handle_file(request)
        elif request['type'] == 'mouse' and self.event_handle:
            self.handle_mouse(request)
        elif request['type'] == 'keyboard' and self.event_handle:
            self.handle_keyboard(request)
        elif request['type'] == 'off_mouse':
            self.handle_off_mouse(request)
        elif request['type'] == 'off_keyboard':
            self.handle_off_keyboard(request)
        elif request['type'] == 'screen_size':
            self.change_screen_size(request)

    def change_screen_size(self, request):
        height = int(request['width']/screeninfo.get_monitors()[0].width*screeninfo.get_monitors()[0].height)
        self.screen_size = (request['width'], height)
        
    
    def capture_screen(self):
        screen = ImageGrab.grab()
        screen = screen.resize(self.screen_size)
        img_byte_arr = io.BytesIO()
        screen.save(img_byte_arr, format='JPEG')
        return img_byte_arr.getvalue()

    def handle_off_mouse(self,request):
        if request['event'] == 'off':
            self.turn_off_mouse.start()
        elif request['event'] == 'on':
            self.turn_off_mouse.stop()
            self.turn_off_mouse = mouse.Listener(suppress=True)
            
    def handle_off_keyboard(self,request):
        if request['event'] == 'off':
            self.turn_off_keyboard.start()
        elif request['event'] == 'on':
            self.turn_off_keyboard.stop()
            self.turn_off_keyboard = keyboard.Listener(suppress=True)        
    
            
    def stream_screen(self):
        skclient_socket, client_address = None, None
        while True:
            if self.connected and self.live and self.send_screen:
                print('ok')
                try:
                    if skclient_socket is None:
                        print('ok2')
                        skclient_socket, client_address = self.sksend_screen.accept()
                    image = self.capture_screen()
                    message = pickle.dumps(image)
                    packet = struct.pack('Q', len(message)) + message
                    skclient_socket.sendall(packet)
                except:
                    sleep(1)
                    
            else:
                try:
                    if skclient_socket:
                        skclient_socket.close()
                except:
                    pass
                finally:
                    skclient_socket = None
                if not self.wait_connect:
                    return
                sleep(1)

    def handle_keyboard(self, request):
        controller = keyboard.Controller()
        if request['event'] == 'press':
            print(request['key'])
            controller.press(request['key'])
        else:
            controller.release(request['key'])

    def handle_mouse(self, request):
        controller = mouse.Controller()
        w,h = screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        if request['event'] == 'move':
            controller.position = (request['pos'][0] * w, request['pos'][1] * h)
        elif request['event'] == 'press':
            controller.position = (request['pos'][0] * w, request['pos'][1] * h)
            controller.press(request['key'])
        elif request['event'] == 'release':
            controller.position = (request['pos'][0] * w, request['pos'][1] * h)
            controller.release(request['key'])
        elif request['event'] == 'scroll':
            controller.position = (request['pos'][0] * w, request['pos'][1] * h)
            controller.scroll(dx=request['key'][0], dy=request['key'][1])

    def checkpass(self, password):
        if not self.have_pass:
            return True
        if self.password == password:
            return True
        return False

    def handle_pass(self, password):
        if self.checkpass(password):
            self.accept_pass = True
            self.live = True
            mes = {
                'type': 'pass',
                'status': True
            }
            self._send(mes)
        else:
            mes = {
                'type': 'pass',
                'status': False
            }
            self._send(mes)

    def disconnect(self):
        if self.client_socket is None:
            return
        try:
            mes = {
                'type': 'disconnect'
            }
            self._send(mes)
            self.connected = False
            self.live = False
            self.accept_pass = False
            sleep(1)
            self.client_socket.close()
        except:
            self.connected = False
            self.live = False
            self.accept_pass = False
        finally:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None

    def async_file(self):
        path = "./async"
        if not os.path.exists(path):
            os.makedirs(path)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
        event_handler = MyHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()

        try:
            while self.file_async:
                sleep(1)
            observer.stop()
        except KeyboardInterrupt:
            observer.stop()

    def handle_file(self, mes):
        self.sending_file = True
        # if not os.path.exists(mes['path']):
        #     os.makedirs(mes['path'])
        if mes['event'] == 'created':
            with open(mes['path'], 'wb') as file:
                file.write(mes['data'])
        elif mes['event'] == 'modified':
            with open(mes['path'], 'wb') as file:
                file.write(mes['data'])
        elif mes['event'] == 'deleted':
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


# server = Server('127.0.0.1', 8888)
# server.run()
# server.start_sync()
