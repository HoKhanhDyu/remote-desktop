import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QVBoxLayout, QListView, QFileSystemModel, QWidget, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenu
import os
import shutil
from PyQt5.QtGui import QIcon

class FileManagerApp(QMainWindow):
    def __init__(self):
        super(FileManagerApp, self).__init__()

        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)

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

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        
        self.right_list_view = QListView()
        self.right_list_view.setModel(self.model)
        self.right_list_view.setRootIndex(self.model.index('async'))
        
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
        
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(splitter)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        
    def home_folder(self):
        self.left_list_view.setRootIndex(self.model.index(''))
        
    def back_folder(self):
        now_index = self.left_list_view.rootIndex()
        self.left_list_view.setRootIndex(now_index.parent())
            
    def double_click_event_left(self, index):
        if self.model.isDir(index):
            self.left_list_view.setRootIndex(index)
        else:
            print(self.model.filePath(index))
            
    def double_click_event_right(self, index):
        if self.model.isDir(index):
            self.right_list_view.setRootIndex(index)
        else:
            print(self.model.filePath(index))
            
    def right_click_event(self, position):
        index = self.left_list_view.indexAt(position)
        if not index.isValid() or self.model.isDir(index):  # Note the parentheses after self.model
            return

        menu = QMenu()
        menu.addAction("Add", lambda: self.copy_file(index))
        menu.exec_(self.left_list_view.viewport().mapToGlobal(position))
        
    def right_click_event2(self, position):
        index = self.right_list_view.indexAt(position)
        if not index.isValid() or self.model.isDir(index):
            return

        menu = QMenu()
        menu.addAction("Remove", lambda: self.remove_file(index))
        menu.addAction("Receive", lambda: self.receive(index))
        menu.exec_(self.right_list_view.viewport().mapToGlobal(position))
        
    def remove_file(self, index):
        self.model.remove(index)

            
    def copy_file(self,path1):
        # print(self.model.filePath(path1))
        shutil.copy(self.model.filePath(path1), 'async')
        
    def receive(self,path1):
        shutil.copy(self.model.filePath(path1), self.model.filePath(self.left_list_view.rootIndex()))
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_manager = FileManagerApp()
    file_manager.show()
    sys.exit(app.exec_())
