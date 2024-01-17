import os
from PyQt5 import QtCore, QtGui, QtWidgets
from time import time
from UI.file import FileManagerApp

class UI_Status(object):
    
    def __init__(self, parent=None, server = None, screen = None):  # Add 'parent' as an argument
        self.parent = parent  # Store the parent widget reference
        self.server = server
        self.screen = screen
        self.recording = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(602, 105)
        MainWindow.setWindowIcon(QtGui.QIcon('./remote_desktop/client/UI/icon/menu.png'))
        self.mainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 591, 61))
        self.frame.setStyleSheet("background-color: rgb(158, 226, 255);\n"
"border-radius: 10px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        #power Button
        self.powerButton = QtWidgets.QPushButton(self.frame)
        self.powerButton.setGeometry(QtCore.QRect(10, 10, 41, 41))
        self.powerButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.powerButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./remote_desktop/client/UI/icon/power_Button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.powerButton.setIcon(icon)
        self.powerButton.setObjectName("powerButton")
        # Set up de nut thay doi mau khi con chuot cham vao
        self.powerButton.enterEvent = self.on_PowerButton_enter
        self.powerButton.leaveEvent = self.on_PowerButton_leave
        # Set up khi nut duoc click
        self.powerButton.clicked.connect(self.on_PowerButton_clicked)

        #Screen Shot
        self.ScreenShotButton = QtWidgets.QPushButton(self.frame)
        self.ScreenShotButton.setGeometry(QtCore.QRect(60, 10, 41, 41))
        self.ScreenShotButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ScreenShotButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./remote_desktop/client/UI/icon/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ScreenShotButton.setIcon(icon1)
        self.ScreenShotButton.setObjectName("ScreenShotButton")
        # Set up de nut thay doi mau khi con chuot cham vao
        self.ScreenShotButton.enterEvent = self.on_ScreenShotButton_enter
        self.ScreenShotButton.leaveEvent = self.on_ScreenShotButton_leave
        # Set up khi nut duoc click
        self.ScreenShotButton.clicked.connect(self.on_ScreenShotButton_clicked)

        #Recorder button
        self.RecorderButton = QtWidgets.QPushButton(self.frame)
        self.RecorderButton.setGeometry(QtCore.QRect(110, 10, 41, 41))
        self.RecorderButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RecorderButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./remote_desktop/client/UI/icon/recorder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RecorderButton.setIcon(icon2)
        self.RecorderButton.setObjectName("RecorderButton")
        # Set up de nut thay doi mau khi con chuot cham vao
        self.RecorderButton.enterEvent = self.on_RecorderButton_enter
        self.RecorderButton.leaveEvent = self.on_RecorderButton_leave
        # Set up khi nut duoc click
        self.RecorderButton.clicked.connect(self.on_RecorderButton_clicked)

        #Mouse Button
        self.MouseButton = QtWidgets.QPushButton(self.frame)
        self.MouseButton.setGeometry(QtCore.QRect(160, 10, 41, 41))
        self.MouseButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.MouseButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./remote_desktop/client/UI/icon/mouse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MouseButton.setIcon(icon3)
        self.MouseButton.setObjectName("MouseButton")
        # Set up khi nut duoc click
        self.MouseButton.clicked.connect(self.on_MouseButton_clicked)
        # Bien (TRUE/False) nay dem danh dau button da duoc nhan chua de thay doi icon phu hop
        self.mouse_icon_flag = False
        # Set up de nut thay doi mau khi con chuot cham vao
        self.MouseButton.enterEvent = self.on_MouseButton_enter
        self.MouseButton.leaveEvent = self.on_MouseButton_leave

        #Monitor Button
        self.monitorButton = QtWidgets.QPushButton(self.frame)
        self.monitorButton.setGeometry(QtCore.QRect(210, 10, 41, 41))
        self.monitorButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.monitorButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./remote_desktop/client/UI/icon/keyboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.monitorButton.setIcon(icon4)
        self.monitorButton.setObjectName("monitorButton")
        # Set up khi nut duoc click
        self.monitorButton.clicked.connect(self.on_MonitorButton_clicked)
        # Bien (TRUE/False) nay dem danh dau button da duoc nhan chua de thay doi icon phu hop
        self.monitor_icon_flag = False
        # Set up de nut thay doi mau khi con chuot cham vao
        self.monitorButton.enterEvent = self.on_Monitor_Button_enter
        self.monitorButton.leaveEvent = self.on_Monitor_Button_leave

        # Độ phân giải
        self.SD_Box = QtWidgets.QComboBox(self.frame)
        self.SD_Box.setGeometry(QtCore.QRect(310, 10, 125, 41))
        self.SD_Box.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SD_Box.setObjectName("SD_Box")
        self.SD_Box.addItem("")
        self.SD_Box.addItem("")
        self.SD_Box.addItem("")
        self.SD_Box.addItem("")

        #Nút mở folder
        self.FileButton = QtWidgets.QPushButton(self.frame)
        self.FileButton.setGeometry(QtCore.QRect(260, 10, 41, 41))
        self.FileButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FileButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./remote_desktop/client/UI/icon/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileButton.setIcon(icon5)
        self.FileButton.setObjectName("FileButton")
        # Set up khi nut duoc click
        self.FileButton.clicked.connect(self.on_FileButton_clicked)
        # Bien (TRUE/False) nay dem danh dau button da duoc nhan chua de thay doi icon phu hop
        self.file_icon_flag = False
        # Set up de nut thay doi mau khi con chuot cham vao
        self.FileButton.enterEvent = self.on_File_Button_enter
        self.FileButton.leaveEvent = self.on_File_Button_leave

        MainWindow.setCentralWidget(self.centralwidget)
        # Set up khi nut duoc click
        self.SD_Box.currentIndexChanged.connect(self.on_SD_Box_Changed)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #stopwatch
        self.stopwatch_label = QtWidgets.QLabel(self.frame)
        self.stopwatch_label.setGeometry(QtCore.QRect(480, 10, 100, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stopwatch_label.setFont(font)
        self.stopwatch_label.setObjectName("stopwatch_label")

        # Create a timer to update the stopwatch every second
        self.timer = QtCore.QTimer(MainWindow)
        self.timer.timeout.connect(self.update_stopwatch)
        # self.seconds_elapsed = 0  # Variable to keep track of elapsed time

        # Start the timer
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def update_stopwatch(self):
        # Update the elapsed time and display it in the stopwatch label
        self.seconds_elapsed = time() - self.server.start_time
        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60
        time_str = "{:02}:{:02}".format(int(minutes), int(seconds))
        self.stopwatch_label.setText(time_str)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Controller"))
        self.SD_Box.setItemText(0, _translate("MainWindow", "1920 x 1080"))
        self.SD_Box.setItemText(1, _translate("MainWindow", "1440 x 900"))
        self.SD_Box.setItemText(2, _translate("MainWindow", "1360 x 768"))
        self.SD_Box.setItemText(3, _translate("MainWindow", "1280 x 720"))


    # Khi nut MouseButton duoc nhan
    def on_MouseButton_clicked(self):
        if self.mouse_icon_flag: # Tuy thuoc vao True/False se lua chon Icon de thay cho button
            new_icon = QtGui.QIcon("./remote_desktop/client/UI/icon/mouse.png")
            self.server.on_mouse()
        else:
            new_icon = QtGui.QIcon("./remote_desktop/client/UI/icon/mouse_delete.png")
            self.server.off_mouse()
            

        #Set up button moi cho Button
        self.MouseButton.setIcon(new_icon)
        # Doi true -> fale hoac nguoc lai
        self.mouse_icon_flag = not self.mouse_icon_flag

    #Khi chuot cham vao nut thi doi mau
    def on_MouseButton_enter(self, event):
        self.MouseButton.setStyleSheet("background-color: lightblue;")
    #Khi chuot dang cham vao nut ma roi di thi doi mau lai nhu cu
    def on_MouseButton_leave(self, event):
        self.MouseButton.setStyleSheet("background-color: white")

    #Cac ham phia duoi chu thich giong nhu cua nut Mouse Button
    #------------------------------------#
        
    def on_MonitorButton_clicked(self):
        if self.monitor_icon_flag:
            new_icon = QtGui.QIcon("./remote_desktop/client/UI/icon/keyboard.png")
            self.server.on_keyboard()
        else:
            new_icon = QtGui.QIcon("./remote_desktop/client/UI/icon/keyboard_delete.png")
            self.server.off_keyboard()
        self.monitorButton.setIcon(new_icon)
        self.monitor_icon_flag = not self.monitor_icon_flag
    
    def on_Monitor_Button_enter(self, event):
        self.monitorButton.setStyleSheet("background-color: lightblue;")
    
    def on_Monitor_Button_leave(self, event):
        self.monitorButton.setStyleSheet("background-color: white")
    
    #------------------------------------#
        
    def on_RecorderButton_enter(self, event):
        self.RecorderButton.setStyleSheet("background-color: lightblue;")
    
    def on_RecorderButton_leave(self, event):
        self.RecorderButton.setStyleSheet("background-color: white")

    def on_RecorderButton_clicked(self):
        if not self.recording: # Tuy thuoc vao True/False se lua chon Icon de thay cho button
            new_icon = QtGui.QIcon("./remote_desktop/client/UI/icon/stop.png")
            self.server.start_record()
        else:
            new_icon = QtGui.QIcon("./remote_desktop/client/UI/icon/recorder.png")
            self.server.stop_record()
            

        #Set up button moi cho Button
        self.RecorderButton.setIcon(new_icon)
        # Doi true -> fale hoac nguoc lai
        self.recording = not self.recording
        # print("Recorder clicked")

    #------------------------------------#
        
    def on_ScreenShotButton_enter(self, event):
        self.ScreenShotButton.setStyleSheet("background-color: lightblue;")
    
    def on_ScreenShotButton_leave(self, event):
        self.ScreenShotButton.setStyleSheet("background-color: white")
    
    def on_ScreenShotButton_clicked(self):
        self.server.save_screen()
        
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Thông Báo")
        msg.setText("Ảnh chụp màn hình đã được lưu.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    #------------------------------------#
        
    def on_PowerButton_enter(self, event):
        self.powerButton.setStyleSheet("background-color: lightblue;")
    
    def on_PowerButton_leave(self, event):
        self.powerButton.setStyleSheet("background-color: white")

    def on_PowerButton_clicked(self,event=None):
        self.server.stop_run()
        self.server.stop_sync()
        self.screen.close_window()
        self.mainWindow.close()
        self.mainWindow.destroy()

    #------------------------------------#
    def on_SD_Box_Changed(self, index):
        # print(self.SD_Box.itemText(index))
        self.server.change_size_screen(self.SD_Box.itemText(index))
    
    #------------------------------------#
        
    def on_File_Button_enter(self, event):
        self.FileButton.setStyleSheet("background-color: lightblue;")
    
    def on_File_Button_leave(self, event):
        self.FileButton.setStyleSheet("background-color: white")

    def on_FileButton_clicked(self):
        # os.startfile(self.server.path)
        self.file_manager = FileManagerApp()
        self.file_manager.show()
        # print("File Button Clicked")

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = UI_Status()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
