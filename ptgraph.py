import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui ,QtWidgets, uic
uifilename = 'main_window.ui'
form_class = uic.loadUiType(uifilename)[0] #dirty reading of the ui file. better to convert it to a '.py'

from lms_test import *

class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.onInit()

    def onInit(self):
#usually a lot of connections here
        self.x_fit = np.linspace(1,10000, 10000)
        self.y_fit = [f(_x) for _x in self.x_fit]
        self.graphicsView.plot(self.x_fit,self.y_fit,symbol='o',pen=None)
        self.graphicsView.setLabel('left',text='toto',units='')
        self.graphicsView.setLabel('top',text='tata',units='')
        self.ptz_up.pressed.connect(lambda:self.button_click())
        datagrams_generator = decode_datagram(lidar_data)
        yl,xl = translate(datagrams_generator)
        self.graphicsView_2.plot(xl, yl)
    def button_click(self):
        print("bbb")

def f(x):
    return x**2+1

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtGui.QApplication([])
        pg.setConfigOption('background', 'w')
        win = MyWindowClass()
        win.show()
        app.exec_()