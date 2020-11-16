#!/usr/local/bin/python3.7
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        widget = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(widget)
        widget.show()
        sys.exit(app.exec_())