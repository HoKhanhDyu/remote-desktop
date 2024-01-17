# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from UI.st import Ui_Form
from UI.ip1 import Ui_Dialog
from server import Server
from time import sleep, time
from UI.file import FileManagerApp
class Ui_MainWindow(object):
    def __init__(self):
        self.server = None
        self.ip, self.port = None, None
        self.ui2 = Ui_Form()
        self.ui3 = Ui_Dialog()
        # self.setWindowIcon(QtGui.QIcon('./remote_desktop/server/UI/icon/icon_app.png'))
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(582, 320)
        MainWindow.setWindowIcon(QtGui.QIcon('./remote_desktop/server/UI/icon/icon_app.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 80, 201, 101))
        self.checkBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setStyleSheet("QCheckBox::indicator{\n"
        "width:200px;\n"
        "height:190px;\n"
        "}\n"
        "\n"
        "QCheckBox::indicator::checked{\n"
        "image:url(\"./remote_desktop/server/UI/icon/001-switch-on.png\")\n"
        "}\n"
        "\n"
        "QCheckBox::indicator::unchecked{image:url(\"./remote_desktop/server/UI/icon/002-switch-off.png\")\n"
        "}\n"
        "")
        self.checkBox.setText("")
        self.checkBox.setIconSize(QtCore.QSize(20, 20))
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.checkBox.setAutoRepeat(False)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.switch_on)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 50, 261, 191))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 20, 31, 31))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setText("")
        self.pushButton_2.clicked.connect(self.openWindow2)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./remote_desktop/server/UI/icon/001-filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 20, 31, 31))
        self.pushButton.setStyleSheet("")
        self.pushButton.setText("")
        self.pushButton.clicked.connect(self.open_async)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./remote_desktop/server/UI/icon/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.get_ip_port()
        
        self.server = Server(self.ip)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Remote Desktop(host)"))
    
    def openWindow2(self):
        self.window2 = QtWidgets.QDialog()
        self.ui2.setupUi(self.window2)
        self.window2.exec_()
        self.server.password = self.ui2.password
        self.server.send_screen = not self.ui2.share_screen
        self.server.event_handle = not self.ui2.control
        self.server.have_pass = self.ui2.have_password    
        
    def open_async(self):
        self.file_manager = FileManagerApp()
        self.file_manager.show()

    def get_ip_port(self):
        self.window3 = QtWidgets.QDialog()
        self.ui3.setupUi(self.window3)
        self.window3.exec_()
        self.ip = self.ui3.get_ip()
        
    def switch_on(self):
        if self.checkBox.isChecked():
            self.server.wait_connect = True
            self.server.run()
        else:
            self.server.disconnect()
            self.server.wait_connect = False
            
    def update_info(self):
        if self.server is not None:
            info = {
                'IP' : self.server.host,
                'Password' : self.server.password if self.server.have_pass else 'Không có mật khẩu',
                'Xem màn hình' : 'Bật' if self.server.send_screen else 'Tắt',
                'Cho phép điều khiển' : 'Bật' if self.server.event_handle else 'Tắt',
                'FPS' : int(self.server.fps) if self.checkBox.isChecked() and self.server.connected else '0',
                'Trạng thái' : 'Đang tắt' if not self.checkBox.isChecked() else 'Đang chờ kết nối' if not self.server.connected else f'Đang kết nối với {self.server.client_address[0]}',
                'Thời gian kết nối' : '{:02}:{:02}'.format(int((time() - self.server.start_time) // 60), int((time() - self.server.start_time) % 60)) if self.server.connected else None,    
            }
            info_str = ""
            for key, value in info.items():
                if value is not None:
                    info_str += f"{key}: {value}\n"
            self.label.setText(info_str)
