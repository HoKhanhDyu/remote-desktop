# Main.py
import io
import sys
from time import sleep
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QWidget, QSizePolicy, QAbstractScrollArea, QPushButton, QDialog, QLabel, 
    QLineEdit, QFileDialog, QMessageBox, QHeaderView  # Add this line
)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from UI.MainPage3 import Ui_MainWindow
from UI.Status import UI_Status
from client import Client
from PyQt5.QtCore import QTimer


class input_password(QDialog):
    def __init__(self, parent=None):
        super(input_password, self).__init__(parent)
        self.setWindowTitle("Password")
        self.resize(320,100)
        layout = QVBoxLayout(self)

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit(self)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.check_password)

    
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.add_button)
    
    def get_password(self):
        return self.password_edit.text()

class Add_Server_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Add_Server_Dialog, self).__init__(parent)
        self.setWindowTitle("Add Server")
        self.resize(320,100)
        layout = QVBoxLayout(self)

        self.ip_label = QLabel("IP:")
        self.ip_edit = QLineEdit(self)

        # self.image_label = QLabel("Image:")
        # self.image_edit = QLineEdit(self)
        # self.browse_button = QPushButton("Browse", self)
        # self.browse_button.clicked.connect(self.browse_image)

        # self.password_label = QLabel("Password:")
        # self.password_edit = QLineEdit(self)
        # self.password_edit.setEchoMode(QLineEdit.Password)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.get_server)

    
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_edit)
        # layout.addWidget(self.password_label)
        # layout.addWidget(self.password_edit)
        # layout.addWidget(self.image_label)
        # layout.addWidget(self.image_edit)
        # layout.addWidget(self.browse_button)
        layout.addWidget(self.add_button)

    # def check_password(self):
    #     password = self.password_edit.text()
    #     if password == '123':
    #         self.accept()
    #     else:
    #         QMessageBox.warning(self, 'Incorrect Password', 'Please enter the correct password.')

    def add_ip(self,ip):
        check_add=Client(ip)
        if check_add is None:
            QMessageBox.warning(self, 'Incorrect IP', 'Please enter the correct IP.')
        elif check_add.have_pass:
            while True:
                dialog=input_password(self)
                result = dialog.exec_()
                if result == QDialog.Accepted:
                    check_add.send_pass(dialog.get_password())
                    if check_add.accepted():
                        return check_add
                else:
                    return None
        else:
            return check_add
    
    def get_server(self):
        self.server = self.add_ip(self.ip_edit.text())
        self.accept()
    
    def browse_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp *.gif)")
        if image_path:
            self.image_edit.setText(image_path)


class ImageWindow(QMainWindow):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.setupUi(self)
        self.x,self.y,self.w,self.h=0,0,0,0
    #setup ui
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Image")
        self.image_label = QLabel(MainWindow)
        self.image_label.setScaledContents(True)

        # Create a QVBoxLayout and add the QLabel to it
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        # Create a QWidget, set its layout to the QVBoxLayout
        widget = QWidget(MainWindow)
        widget.setLayout(layout)

        # Set the QWidget as the central widget of the QMainWindow
        MainWindow.setCentralWidget(widget)

        # Initialize and start the QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_image)
        self.timer.start(50)
        
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_x_y)
        self.timer2.start(1000)
        
        
    def load_image(self):
        # print('load image')
        buffer = io.BytesIO()
        if self.server['server'].capture is None:
            return
        self.server['server'].capture.save(buffer, format="PNG")

        # Chuyển đổi sang QPixmap và hiển thị trong QLabel
        pixmap = QPixmap()
        success = pixmap.loadFromData(buffer.getvalue(), "PNG") 

        # Kiểm tra xem việc tải dữ liệu có thành công không
        if success:
            # Chỉnh sửa kích thước ảnh nếu tải thành công
            # print('load image')
            # pixmap = pixmap.scaledToWidth(1000)
            self.image_label.setPixmap(pixmap)
            # Bây giờ bạn có thể sử dụng pixmap để hiển thị trong QLabel hoặc widget khác
            # Ví dụ: self.image_label.setPixmap(pixmap)
        else:
            print("Failed to load image data.")
        
        # self.image_label.update()
        
    def update_x_y(self):
        if self.x != self.pos().x() or self.y != self.pos().y():
            self.x,self.y=self.pos().x(),self.pos().y()
            self.server.x,self.server.y=self.x,self.y
        if self.w != self.width() or self.h != self.height():
            self.w,self.h=self.width(),self.height()
            self.server.width,self.server.height=self.w,self.h
        
        


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MainPage")
        self.status_window = None
        # Initialize an empty server list
        self.server_list = []

        # Populate the scroll area with server information
        self.timer = QTimer()
        # Connect the timer's timeout signal to the update_image function
        self.timer.timeout.connect(self.populate_server_list)
        # Start the timer to call update_image every 100ms
        self.timer.start(1000)
        

        self.ui.ConnectButton.clicked.connect(self.show_add_server_dialog)
        #self.verticalLayout.addWidget(self.ui.ConnectButton)

    def populate_server_list(self): 
        # Create a new widget to hold the layouthj
        widget = QWidget(self)
        self.ui.scrollArea.setWidget(widget)
        # Create a new QVBoxLayout for the widget
        layout = QVBoxLayout(widget)

        # Create a new QTableWidget for the layout
        table_widget = QTableWidget()
        table_widget.setColumnCount(2)  # Number of columns (IP, Image)

        # Set headers
        headers = ["IP", "Image"]
        table_widget.setHorizontalHeaderLabels(headers)

        # Add rows to the table for each student
        for server in self.server_list:
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)

            # Populate each cell in the row
            table_widget.setItem(row_position, 0, QTableWidgetItem(server["ip"]))

            # Add image to the row
            image_label = QLabel()
            buffer = io.BytesIO()
            #check none
            while server['server'].capture is None:
                print('none')
                sleep(1)
            server['server'].capture.save(buffer, format="PNG")

            # Chuyển đổi sang QPixmap và hiển thị trong QLabel
            pixmap = QPixmap()
            success = pixmap.loadFromData(buffer.getvalue(), "PNG")

            # Kiểm tra xem việc tải dữ liệu có thành công không
            if success:
                # Chỉnh sửa kích thước ảnh nếu tải thành công
                pixmap = pixmap.scaledToWidth(100)

                # Bây giờ bạn có thể sử dụng pixmap để hiển thị trong QLabel hoặc widget khác
                # Ví dụ: self.image_label.setPixmap(pixmap)
            else:
                print("Failed to load image data.")# Adjust the width as needed
            image_label.setPixmap(pixmap)
            table_widget.setCellWidget(row_position, 1, image_label)

        table_widget.cellClicked.connect(self.cell_clicked)
        
        # Set the size policy for the table widget
        table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the size policy for the widget containing the table
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the last section of the horizontal header to stretch
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Add the table widget to the layout
        layout.addWidget(table_widget)

        # Set the size policy for the scroll area
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Ensure the layout is updated
        self.ui.scrollArea.updateGeometry()
        widget.adjustSize()

    def show_add_server_dialog(self):
        dialog = Add_Server_Dialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            new_server = {
                "ip": dialog.ip_edit.text(),
                # "image": dialog.image_edit.text()
                'server':dialog.server
            }
            print(new_server)
            if new_server['server'] is None:
                return
            new_server['server'].run_screen()
            self.server_list.append(new_server)

            # Clear the existing table
            self.clear_table()

            # Repopulate the table with the updated server list
            self.populate_server_list()

    def clear_table(self):
        # Clear the existing table
        widget = self.ui.scrollArea.widget()
        for i in reversed(range(widget.layout().count())):
            widget.layout().itemAt(i).widget().setParent(None)

    def cell_clicked(self, row, column):
        print(f"Đây là ô ({row}, {column})")
        server_screen = self.server_list[row]
        self.show_image_window(server_screen)
        self.show_status_window()
        
    def show_image_window(self, server):
        # self.image_window = QtWidgets.QMainWindow()
        self.ui_image = ImageWindow(server)
        server['server'].run_listen()
        # ui_image.setupUi(self.image_window)
        # self.image_window.show()
        self.ui_image.show()

    
    # def show_status_window(self):
    #     if not self.status_window:  # Check if the status window is not already open
    #         self.status_window = QtWidgets.QMainWindow()
    #         ui_status = UI_Status()
    #         ui_status.setupUi(self.status_window)
    #         self.status_window.show()
   
    def show_status_window(self):
        if not self.status_window or not self.status_window.isVisible():  
            self.status_window = QtWidgets.QMainWindow()
            ui_status = UI_Status(self.status_window)
            ui_status.setupUi(self.status_window)
            self.status_window.show()
            # Connect the destroyed signal to set status_window to None
            self.status_window.destroyed.connect(lambda: setattr(self, 'status_window', None))


