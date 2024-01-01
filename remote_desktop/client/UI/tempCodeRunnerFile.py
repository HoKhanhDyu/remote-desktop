_":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_Status()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
