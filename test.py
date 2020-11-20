import sys
import time

from lms151 import *

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    print("qt5")
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("192.168.0.30", 2112))
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        # self._dynamic_ax.plot(t, np.sin(t + time.time()))
        xl, yl = get_draw(self.s)
        self._dynamic_ax.plot(yl, xl)
        self._dynamic_ax.invert_yaxis()
        # self._dynamic_ax.figure.canvas.draw()
        lx, ly = self.find_line(yl, xl)
        for i in range(len(lx) - 1):
            if 40 < len(ly[i]) < 100:
                self._dynamic_ax.plot(lx[i][2:-5], ly[i][2:-5], label='ob', color='r', linewidth=1)
                # print('length: {}, X: {}, Y: {}'.format(abs(lx[i][1]-lx[i][-1]), lx[i][int(len(lx[i])/2)], ly[i][1]))
                lenth = abs(lx[i][1] - lx[i][-1])
                x_pose = lx[i][int(len(lx[i]) / 2)]
                y_pose = ly[i][1]
                text = 'L: {}, X: {}, Y: {}'.format(format(lenth, '.3f'), format(x_pose, '.3f'), format(y_pose, '.3f'))
                self._dynamic_ax.text(0, -3, text, ha='center', va='bottom', fontsize=7)
        self._dynamic_ax.figure.canvas.draw()

    def find_line(self, xx, yy):
        a = [[]]
        b = [[]]
        for i in range(len(xx)):
            if yy[i] > 1.7 and yy[i] < 2.1:
                if len(a[-1]) == 0:
                    a[-1].append(xx[i])
                    b[-1].append(yy[i])
                elif abs(yy[i] - b[-1][-1]) < 0.2 and abs(xx[i] - a[-1][-1]) < 0.2:
                    a[-1].append(xx[i])
                    b[-1].append(yy[i])
                elif abs(xx[i] - a[-1][-1]) > 0.3:
                    a.append([xx[i]])
                    b.append([yy[i]])
        return a, b


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()