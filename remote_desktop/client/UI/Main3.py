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
from PyQt5.QtCore import Qt
import time
from PIL import Image


class input_password(QDialog):
    def __init__(self, parent=None):
        super(input_password, self).__init__(parent)
        self.setWindowTitle("Password")
        self.resize(320,100)
        layout = QVBoxLayout(self)

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit(self)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.ok)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.add_button)
    
    def get_password(self):
        return self.password_edit.text()

    def ok(self):
        self.accept()


class Add_Server_Dialog(QDialog):
    def __init__(self, parent=None):
        super(Add_Server_Dialog, self).__init__(parent)
        self.setWindowTitle("Add Server")
        self.resize(320,100)
        layout = QVBoxLayout(self)

        self.ip_label = QLabel("IP:")
        self.ip_edit = QLineEdit(self)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.get_server)

        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_edit)
        layout.addWidget(self.add_button)

    def add_ip(self,ip):
        check_add=Client(ip)
        if check_add is None:
            QMessageBox.warning(self, 'Incorrect IP', 'Please enter the correct IP.')
            return None
        check_add.run_screen()
        if check_add.have_pass:
            while True:
                dialog=input_password(self)
                result = dialog.exec_()
                if result == QDialog.Accepted:
                    check_add.send_pass(dialog.get_password())
                    sleep(1)
                    if check_add.accepted:
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
        global_x,global_y,global_w,global_h =self.get_actual_image_position_and_size()
        self.x,self.y=global_x,global_y
        self.server.x,self.server.y=self.x,self.y
        self.w,self.h=global_w,global_h
        self.server.width,self.server.height=self.w,self.h
        self.last_frame_time = None
        
    #setup ui
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        pic = io.BytesIO(self.server.capture)
        pic = Image.open(pic)
        MainWindow.resize(pic.size[0]//2, pic.size[1]//2)
        MainWindow.setWindowTitle("Image")
        self.image_label = QLabel(MainWindow)
        # self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.image_label.setStyleSheet("background-color: black;")
        self.image_label.setAlignment(Qt.AlignCenter)

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
        self.timer.start(10)
        
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_x_y)
        self.timer2.start(5000)
        
        self.timer3 = QTimer(self)
        self.timer3.timeout.connect(self.isactive)
        self.timer3.start(1000)
        
    
    def isactive(self):
        if self.isActiveWindow():
            # print('active')
            self.server.have_focus=True
        else:
            # print('not active')
            self.server.have_focus=False
    
    def load_image(self):
        # print('load image')
        if self.server.capture is None:
            return

        # Chuyển đổi sang QPixmap và hiển thị trong QLabel
        pixmap = QPixmap()
        success = pixmap.loadFromData(self.server.capture, "JPEG") 

        # Kiểm tra xem việc tải dữ liệu có thành công không
        if success:
            # Chỉnh sửa kích thước ảnh nếu tải thành công
            # print('load image')
            # pixmap = pixmap.scaledToWidth(800)
            scaledPixmap = pixmap.scaled(self.width()-20, self.height()-20, Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaledPixmap)
            # Bây giờ bạn có thể sử dụng pixmap để hiển thị trong QLabel hoặc widget khác
            # Ví dụ: self.image_label.setPixmap(pixmap)
        else:
            print("Failed to load image data.")
        current_time = time.time()

        if self.last_frame_time is not None:
            time_diff = current_time - self.last_frame_time
            fps = 1 / time_diff if time_diff > 0 else 0
            # print(f"FPS: {fps}")

        self.last_frame_time = current_time            
        
        # self.image_label.update()
        
    def update_x_y(self):
        global_x,global_y,global_w,global_h =self.get_actual_image_position_and_size()
        if self.x != global_x or self.y != global_y:
            self.x,self.y=global_x,global_y
            self.server.x,self.server.y=self.x,self.y
        if self.w!=global_w or self.h!=global_h:
            self.w,self.h=global_w,global_h
            self.server.width,self.server.height=self.w,self.h
            
    def get_actual_image_position_and_size(self):
        label_global_pos = self.image_label.mapToGlobal(QtCore.QPoint(0, 0))
        label_size = self.image_label.size()
        pixmap = self.image_label.pixmap()

        if pixmap and not pixmap.isNull():
            # Kích thước của ảnh sau khi được điều chỉnh kích thước
            image_size = pixmap.size().scaled(label_size, Qt.KeepAspectRatio)

            # Tính padding
            padding_x = (label_size.width() - image_size.width()) // 2
            padding_y = (label_size.height() - image_size.height()) // 2

            # Vị trí thực tế của ảnh bên trong image_label
            actual_x = label_global_pos.x() + padding_x
            actual_y = label_global_pos.y() + padding_y

            # Trả về vị trí và kích thước thực tế của ảnh
            return actual_x, actual_y, image_size.width(), image_size.height()
        else:
            # Nếu không có pixmap, trả về vị trí của image_label và kích thước 0
            return label_global_pos.x(), label_global_pos.y(), 0, 0
        
    def close_window(self):
        self.close()
        self.deleteLater()
        


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
        # self.timer = QTimer()
        # # Connect the timer's timeout signal to the update_image function
        # self.timer.timeout.connect(self.populate_server_list)
        # # Start the timer to call update_image every 100ms
        # self.timer.start(1000)
        self.populate_server_list()

        self.ui.ConnectButton.clicked.connect(self.show_add_server_dialog)
        #self.verticalLayout.addWidget(self.ui.ConnectButton)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.populate_server_list)
        self.timer.start(5000)
        self.ui.DisconnectButton.clicked.connect(self.disconnect_selected_server)
        #self.verticalLayout.addWidget(self.ui.ConnectButton)
    def disconnect_selected_server(self):
        # Get the selected row
        selected_row = self.ui.scrollArea.widget().layout().itemAt(0).widget().currentRow()

        if selected_row >= 0:
            # Remove the selected server from the list
            self.server_list[selected_row]['server'].disconnect()
            del self.server_list[selected_row]

            # Clear the existing table
            self.clear_table()

            # Repopulate the table with the updated server list
            self.populate_server_list()
            # Show a success message
            QMessageBox.information(self, 'Success', 'Server disconnected successfully.')
        else:
            # Show a warning message if no row is selected
            QMessageBox.warning(self, 'No Server Selected', 'Please select a server to disconnect.')

    def populate_server_list(self): 
        # Create a new widget to hold the layout
        widget = QWidget(self)
        self.ui.scrollArea.setWidget(widget)
        # Create a new QVBoxLayout for the widget
        layout = QVBoxLayout(widget)

        # Create a new QTableWidget for the layout
        table_widget = QTableWidget()
        table_widget.setColumnCount(2)  # Number of columns (IP, Image)

        ip_column_width = 200
        table_widget.setColumnWidth(0, ip_column_width)
        
        # Set headers
        headers = ["IP", "Screen"]
        table_widget.setHorizontalHeaderLabels(headers)

        # Add rows to the table for each student
        for server in self.server_list:
            if server['server'].server_socket is None:
                self.server_list.remove(server)
                continue
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)

            # Populate each cell in the row
            
            ip = QTableWidgetItem(server["ip"])
            ip.setTextAlignment(Qt.AlignCenter)
            table_widget.setItem(row_position, 0, ip)
            # Add image to the row
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter)
            #check none
            while server['server'].capture is None:
                # print('none')
                sleep(1)

            # Chuyển đổi sang QPixmap và hiển thị trong QLabel
            pixmap = QPixmap()
            success = pixmap.loadFromData(server['server'].capture, "JPEG")

            if not success:
                print("Failed to load image data.")
                return
            
            original_width = pixmap.width()
            original_height = pixmap.height()
            scaled_width = 500  # Adjust the width as needed
            scaled_height = int((scaled_width / original_width) * original_height)

            # Set a maximum height for the images
            ip_column_width = 200
            table_widget.setColumnWidth(0, ip_column_width)
            max_height = 200  # Adjust the height as needed
            if scaled_height > max_height:
                scaled_height = max_height
                scaled_width = int((scaled_height / original_height) * original_width)

            pixmap = pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)

            # Set a fixed width for the IP column
            ip_column_width = scaled_width // 2
            ip_column_width = 200
            table_widget.setColumnWidth(0, ip_column_width)

            # Set a fixed width for the image column
            table_widget.setColumnWidth(1, scaled_width)

            # Set size policy for the image label
            image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Set a fixed height for the row
            table_widget.setRowHeight(row_position, scaled_height)

            table_widget.setCellWidget(row_position, 1, image_label)

        table_widget.cellClicked.connect(self.cell_clicked)
        
        # Set the size policy for the table widget
        table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the size policy for the widget containing the table
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the last section of the horizontal header to stretch
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

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
            # print(new_server)
            if new_server['server'] is None:
                return
            # new_server['server'].run_screen()
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
        # print(f"Đây là ô ({row}, {column})")
        server_screen = self.server_list[row]
        self.show_window(server_screen)
        
    def show_window(self, server):
        # self.image_window = QtWidgets.QMainWindow()
        self.ui_image = ImageWindow(server['server'])
        server['server'].run_listener()
        server['server'].start_sync()
        # ui_image.setupUi(self.image_window)
        # self.image_window.show()
        self.ui_image.show()
        if not self.status_window or not self.status_window.isVisible():  
            self.status_window = QtWidgets.QMainWindow()
            ui_status = UI_Status(self.status_window,server['server'],self.ui_image)
            ui_status.setupUi(self.status_window)
            self.status_window.show()
            # Connect the destroyed signal to set status_window to None
            self.status_window.destroyed.connect(lambda: setattr(self, 'status_window', None))
    
    # def show_status_window(self):
    #     if not self.status_window:  # Check if the status window is not already open
    #         self.status_window = QtWidgets.QMainWindow()
    #         ui_status = UI_Status()
    #         ui_status.setupUi(self.status_window)
    #         self.status_window.show()
   
    # def show_status_window(self):
    #     if not self.status_window or not self.status_window.isVisible():  
    #         self.status_window = QtWidgets.QMainWindow()
    #         ui_status = UI_Status(self.status_window)
    #         ui_status.setupUi(self.status_window)
    #         self.status_window.show()
    #         # Connect the destroyed signal to set status_window to None
    #         self.status_window.destroyed.connect(lambda: setattr(self, 'status_window', None))


