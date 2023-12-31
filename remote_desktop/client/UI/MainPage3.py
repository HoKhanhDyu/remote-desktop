from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(475, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 461, 61))
        self.frame.setStyleSheet("background-color:rgb(255, 255, 127);\n"
"border-radius: 10px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.DisconnectButton = QtWidgets.QPushButton(self.frame)
        self.DisconnectButton.setGeometry(QtCore.QRect(280, 10, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DisconnectButton.setFont(font)
        self.DisconnectButton.setStyleSheet("QPushButton {\n"
"  background-color: white;\n"
"  color: black;\n"
"  border:none;\n"
"}")
        self.DisconnectButton.setObjectName("DisconnectButton")
        self.DisconnectButton.enterEvent = self.on_disconnect_button_enter
        self.DisconnectButton.leaveEvent = self.on_disconnect_button_leave

        self.ConnectButton = QtWidgets.QPushButton(self.frame)
        self.ConnectButton.setGeometry(QtCore.QRect(30, 10, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ConnectButton.setFont(font)
        self.ConnectButton.setStyleSheet("QPushButton {\n"
"  background-color: rgb(255, 255, 255);\n"
"  color: back;\n"
"  border:none;\n"
"}")
        self.ConnectButton.setObjectName("ConnectButton")
        self.ConnectButton.enterEvent = self.on_connect_button_enter
        self.ConnectButton.leaveEvent = self.on_connect_button_leave

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 451, 281))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 449, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 475, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def on_connect_button_enter(self, event):
        self.ConnectButton.setStyleSheet("QPushButton {\n"
            "  background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(85, 255, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "  color: black;\n"
            "  border:none;\n"
            "}\n"
            )

    def on_connect_button_leave(self, event):
        self.ConnectButton.setStyleSheet("QPushButton {\n"
            "  background-color: white; \n"
            "  color: back;\n"
            "  border:none;\n"
            "}\n"
            )
    
    def on_disconnect_button_enter(self, event):
        self.DisconnectButton.setStyleSheet("QPushButton {\n"
            "  background-color: qlineargradient(spread:pad, x1:0.511364, y1:0.591, x2:1, y2:1, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "  color: white;\n"
            "  border:none;\n"
            "}\n"
            )
    def on_disconnect_button_leave(self, event):
        self.DisconnectButton.setStyleSheet("QPushButton {\n"
            "  background-color: white; \n"
            "  color: back;\n"
            "  border:none;\n"
            "}\n"
            )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DisconnectButton.setText(_translate("MainWindow", "Disconnect"))
        self.ConnectButton.setText(_translate("MainWindow", "Connect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
