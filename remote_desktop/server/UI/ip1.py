from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.Form = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(277, 136)
        Dialog.setWindowIcon(QtGui.QIcon('./remote_desktop/server/UI/icon/icon_app.png'))
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(90, 90, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 120, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 231, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton.clicked.connect(self.on_ok_clicked)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Nhập IP"))
        self.pushButton.setText(_translate("Dialog", "Ok"))
        self.label.setText(_translate("Dialog", "Nhập IP của server:"))
        
    def on_ok_clicked(self):
        self.ip = self.lineEdit.text()
        self.Form.close()

    def get_ip(self):
        return self.ip