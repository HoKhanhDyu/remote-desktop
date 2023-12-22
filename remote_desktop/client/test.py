from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            print(f"File đã thay đổi: {file_path}")
        
    def on_created(self, event):
        if not event.is_directory:
            print(f"{event.src_path} đã được tạo!")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"{event.src_path} đã bị xóa!")


path = "./async"
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=False)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()