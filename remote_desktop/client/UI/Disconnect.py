from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(659, 191)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 10, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.Yes_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Yes_Button.setGeometry(QtCore.QRect(200, 70, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.Yes_Button.setFont(font)
        self.Yes_Button.setStyleSheet("border-radius: 10px;\n"
"background-color: rgb(255, 255, 255);")
        self.Yes_Button.setObjectName("Yes_Button")
        # Set up de nut thay doi mau khi con chuot cham vao
        self.Yes_Button.enterEvent = self.on_Yes_Button_enter
        self.Yes_Button.leaveEvent = self.on_Yes_Button_leave

        # No Button
        self.No_Button = QtWidgets.QPushButton(self.centralwidget)
        self.No_Button.setGeometry(QtCore.QRect(340, 70, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.No_Button.setFont(font)
        self.No_Button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 10px;")
        self.No_Button.setObjectName("No_Button")
        # Set up de nut thay doi mau khi con chuot cham vao
        self.No_Button.enterEvent = self.on_No_Button_enter
        self.No_Button.leaveEvent = self.on_No_Button_leave

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 659, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Xác Nhận Ngắt Kết Nối"))
        self.Yes_Button.setText(_translate("MainWindow", "Có"))
        self.No_Button.setText(_translate("MainWindow", "Không"))

    # Ham thay doi mau sac nut Yes_Button khi con chuot cham
    #a. Khi con chuot cham vao
    def on_Yes_Button_enter(self, event):
        self.Yes_Button.setStyleSheet("background-color: lightgreen; \n"
                                      "border-radius: 10px;\n")
    #b. Khi con chuot dang cham vao thi roi di
    def on_Yes_Button_leave(self, event):
        self.Yes_Button.setStyleSheet("background-color: white; \n"\
                                      "border-radius: 10px;\n")

    # Ham thay doi mau sac nut No_Button khi con chuot cham
    #a. Khi con chuot cham vao
    def on_No_Button_enter(self, event):
        self.No_Button.setStyleSheet("background-color: rgb(255, 69, 72); \n"
                                      "border-radius: 10px;\n"
                                      "color: white")
    #b. Khi con chuot dang cham vao thi roi di
    def on_No_Button_leave(self, event):
        self.No_Button.setStyleSheet("background-color: white; \n"\
                                      "border-radius: 10px;\n"
                                      "color: black")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
