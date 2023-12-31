# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def __init__(self):
        self.password = None
        self.share_screen = False
        self.control = False
        self.have_password = False

    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.setFixedSize(306, 155)
        Form.setMouseTracking(False)

        self.checkBox_4 = QtWidgets.QCheckBox(Form)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 10, 221, 20))
        self.checkBox_4.setObjectName("checkBox_4")

        self.checkBox_3 = QtWidgets.QCheckBox(Form)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 40, 391, 20))
        self.checkBox_3.setObjectName("checkBox_3")

        self.textEdit = QtWidgets.QLineEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(20, 90, 267, 26))
        self.textEdit.setObjectName("textEdit")

        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 70, 81, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.on_off_password)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 120, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.save)

        self.textEdit.hide()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.checkBox_4.setChecked(self.share_screen)
        self.checkBox_3.setChecked(self.control)
        self.checkBox_2.setChecked(self.have_password)

        if self.have_password:
            self.textEdit.show()
            self.textEdit.setText(self.password)
        else:
            self.textEdit.hide()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox_4.setText(_translate("Form", "Tắt màn hình chia sẻ"))
        self.checkBox_3.setText(_translate("Form", "Tắt điều khiển chuột và bàn phím"))
        self.checkBox_2.setText(_translate("Form", "Mật khẩu"))
        self.pushButton.setText(_translate("Form", "Lưu"))

    def on_off_password(self):
        if self.checkBox_2.isChecked():
            self.textEdit.show()
        else:
            self.textEdit.hide()

    def save(self):
        self.share_screen = self.checkBox_4.isChecked()
        self.control = self.checkBox_3.isChecked()
        self.have_password = self.checkBox_2.isChecked()

        if self.have_password:
            self.password = self.textEdit.toPlainText()
        else:
            self.password = None

        self.Form.close()

    def get_setting(self):
        return self.share_screen, self.control, self.have_password, self.password
