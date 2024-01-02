# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from UI.st import Ui_Form
from UI.ip1 import Ui_Dialog
from server import Server
from time import sleep

class Ui_MainWindow(object):
    def __init__(self):
        self.server = None
        self.ip, self.port = None, None
        self.ui2 = Ui_Form()
        self.ui3 = Ui_Dialog()
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(582, 320)
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
        self.label.setGeometry(QtCore.QRect(270, 75, 261, 191))
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
    
    def openWindow2(self):
        self.window2 = QtWidgets.QDialog()
        self.ui2.setupUi(self.window2)
        self.window2.exec_()
        self.server.password = self.ui2.password
        self.server.send_screen = not self.ui2.share_screen
        self.server.event_handle = not self.ui2.control
        self.server.have_pass = self.ui2.have_password        

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
                'ip' : self.server.host,
                'port' : self.server.port,
                'password' : self.server.password if self.server.have_pass else 'Không có mật khẩu',
                'send_screen' : self.server.send_screen,
                'event_handle' : self.server.event_handle,
                'Server' : 'Đang tắt' if not self.checkBox.isChecked() else 'Đang chờ kết nối' if not self.server.connected else 'Đang chạy'
            }
            info_str = ""
            for key, value in info.items():
                info_str += f"{key}: {value}\n"
            self.label.setText(info_str)
