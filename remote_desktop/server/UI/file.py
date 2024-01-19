import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QVBoxLayout, QListView, QFileSystemModel, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenu
import os
import shutil
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from time import sleep,time

class FileManagerApp(QMainWindow):
    def __init__(self, socket=None):
        super(FileManagerApp, self).__init__()

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)
        self.server = socket
        self.now_path = ''
        self.now_file = None

        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('remote_desktop/server/UI/icon/file.png'))
        
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        
        self.left_list_view = QListView()
        self.left_list_view.setModel(self.model)
        self.left_list_view.setRootIndex(self.model.index(''))

        
        self.button2 = QPushButton("")
        self.button2.setFixedWidth(25)
        self.button2.setFixedHeight(25)
        self.button2.clicked.connect(self.home_folder)
        self.button2.setIcon(QIcon('remote_desktop/server/UI/icon/001-home.png'))


        self.button = QPushButton("")
        self.button.setFixedWidth(25)
        self.button.setFixedHeight(25)
        self.button.clicked.connect(self.back_folder)
        self.button.setIcon(QIcon('remote_desktop/server/UI/icon/002-arrow.png'))
        
        self.button3 = QPushButton("")
        self.button3.setFixedWidth(25)
        self.button3.setFixedHeight(25)
        self.button3.clicked.connect(self.back_folder2)
        self.button3.setIcon(QIcon('remote_desktop/server/UI/icon/002-arrow.png'))
        
        
        self.button4 = QPushButton("")
        self.button4.setFixedWidth(25)
        self.button4.setFixedHeight(25)
        self.button4.clicked.connect(self.home_folder2)
        self.button4.setIcon(QIcon('remote_desktop/server/UI/icon/001-home.png'))

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        
        self.right_list_view = QListView()
        
        self.left_list_view.doubleClicked.connect(self.double_click_event_left)
        self.right_list_view.doubleClicked.connect(self.double_click_event_right)
        self.left_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.left_list_view.customContextMenuRequested.connect(self.right_click_event)
        self.right_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.right_list_view.customContextMenuRequested.connect(self.right_click_event2)

        splitter = QSplitter()
        splitter.addWidget(self.left_list_view)
        splitter.addWidget(self.right_list_view)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignLeft)

        button_layout.addWidget(self.button2)
        button_layout.addWidget(self.button)
        
        button_layout2 = QHBoxLayout()
        button_layout2.setAlignment(Qt.AlignRight)
        button_layout2.addWidget(self.button4)
        button_layout2.addWidget(self.button3)
        
        splitter2 = QHBoxLayout()
        splitter2.addLayout(button_layout)
        splitter2.addLayout(button_layout2)
        
        layout = QVBoxLayout()
        layout.addLayout(splitter2)
        layout.addWidget(splitter)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        
        self.load_right()
        
    def load_right(self):
        self.server.query_file(self.now_path)
        
        current_time = time()
        
        while self.server.list_file == self.now_file and time() - current_time < 2:
            sleep(0.3)
        
        self.now_file = self.server.list_file   
        
        model = QStandardItemModel(self.right_list_view)

        
        for file in self.server.list_file:  
            # print(file)
            item = QStandardItem(file['name'])
            if file['type'] == 'folder':
                item.setIcon(QIcon('remote_desktop/client/UI/icon/folder_icon.png'))
            else:
                item.setIcon(QIcon('remote_desktop/client/UI/icon/file_icon.png'))
            model.appendRow(item)
        self.right_list_view.setModel(model)
            
        
    def home_folder(self):
        self.left_list_view.setRootIndex(self.model.index(''))
        
    def back_folder(self):
        now_index = self.left_list_view.rootIndex()
        self.left_list_view.setRootIndex(now_index.parent())
        
    def home_folder2(self):
        self.now_path = ''
        self.load_right()
    
    def back_folder2(self):
        new_path = self.now_path.split('\\')
        # print(new_path)
        new_path = '\\'.join(new_path[0:-1]) if len(new_path) > 2 else new_path[0]+'\\' if len(new_path) == 2 and new_path[1]!='' else '' 
        self.now_path = new_path
        # print(self.now_path)
        self.load_right()
            
    def double_click_event_left(self, index):
        if self.model.isDir(index):
            self.left_list_view.setRootIndex(index)
        else:
            # print(self.model.filePath(index))
            pass
            
    def double_click_event_right(self, index):
        try:
            if self.server.list_file[index.row()]['type'] == 'folder':
                self.now_path = self.server.list_file[index.row()]['path']
                # print(self.now_path)
                self.load_right()
            else:
                # print(self.server.list_file[index.row()]['path'])
                pass
        except:
            pass
            
    def right_click_event(self, position):
        index = self.left_list_view.indexAt(position)
        if not index.isValid() or self.model.isDir(index):  # Note the parentheses after self.model
            return

        menu = QMenu()
        menu.addAction("Add", lambda: self.copy_file(index))
        menu.exec_(self.left_list_view.viewport().mapToGlobal(position))
        
    def right_click_event2(self, position):
        index = self.right_list_view.indexAt(position)
        if self.server.list_file[index.row()]['type'] == 'folder':
            return
        menu = QMenu()
        menu.addAction("Receive", lambda: self.receive(index.row()))
        menu.exec_(self.right_list_view.viewport().mapToGlobal(position))
            
    def copy_file(self,path1):
        path =  self.model.filePath(path1)
        # print(path)
        self.server.send_file(path, self.now_path)
        # print('ok2')
        self.load_right()
    def receive(self,index):
        path =self.model.filePath(self.left_list_view.rootIndex())
        # print(path)
        self.server.need_file(self.server.list_file[index]['path'],path)
        
        

