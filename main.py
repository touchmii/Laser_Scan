#!/usr/local/bin/python3.7
import sys
import numpy as np
import pyqtgraph as pg
# import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui ,QtWidgets, uic
from Graphs.Surface3D_Graph import Surface3D_Graph
from queue import Queue
uifilename = 'main_window.ui'
form_class = uic.loadUiType(uifilename)[0] #dirty reading of the ui file. better to convert it to a '.py'

# from lms_test import *
from lms3d import *

from ptz import *

# import asyncio
# from quamash import QEventLoop

# from pymodbus.server.asyncio import StartTcpServer
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.asyncio import StartUdpServer
from pymodbus.server.asyncio import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer

# store = ModbusSlaveContext(
#     di=ModbusSequentialDataBlock(0, [17]*100),
#     co=ModbusSequentialDataBlock(0, [17]*100),
#     hr=ModbusSequentialDataBlock(0, [17]*100),
#     ir=ModbusSequentialDataBlock(0, [0]*100))

class CallbackDataBlock(ModbusSparseDataBlock):
    """ A datablock that stores the new value in memory
    and passes the operation to a message queue for further
    processing.
    """

    # def __init__(self, devices, queue):
    #     """
    #     """
    #     self.devices = devices
    #     self.queue = queue
    #
    #     values = {k: 0 for k in devices.keys()}
    #     values[0xbeef] = len(values)  # the number of devices
    #     super(CallbackDataBlock, self).__init__(values)

    def setValues(self, address, value):
        """ Sets the requested values of the datastore

        :param address: The starting address
        :param values: The new values to be set
        """
        print(value)
        # win.start_scan.checkable(False)
        super(CallbackDataBlock, self).setValues(address, value)
        # MyWidget.Signal_NoParameters.emit()
        # x = MyWidget()
        # x.cc()
        # x.Signal_NoParameters.emit()
        # self.queue.put((self.devices.get(address, None), value))
block = CallbackDataBlock([17]*100)
store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
context = ModbusServerContext(slaves=store, single=True)

def updating_writer(register, address, value):
#    context = context[0]
    slave_id = 0x01
    values = context[slave_id].getValues(register, address, count=5)
    values = [v + 1 for v in values]
    context[slave_id].setValues(register, address, value)

def run_server():
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '2.3.0'

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    # Tcp:
    # immediately start serving:
    global context
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 2502))

defaultNumberOfData = 128

class ThreadExample(QtCore.QThread):
    printSignal = QtCore.pyqtSignal()
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    # Code to execute when running the thread
    def run(self):
        run_server()
        while True:
            time.sleep(1)
            print('xxxxx')
class ThreadScan(QtCore.QThread):
    printSignal = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def __init__(self, ip, q, s, parent=None):
        QtCore.QThread.__init__(self)
        # super(ThreadScan, self).__init__(parent)
        self.ip = ip
        self.q = q
        self.s = s
        # super().__init__(self)

    # def __del__(self):
    #     self.wait()

    # Code to execute when running the thread
    def run(self):

        # s.connect((self.ip, 2112))
        # if self.s.connect
        self.s.connect((self.ip, 2112))
        start = time.time()
        data = []
        print('xxx')
        while True:
            data.append(get_draw(self.s))
            # print(get_draw(s))
            time.sleep(0.02)
            if time.time() - start > 20:
                break
        # print(data)
        self.s.close()
        print(len(data))
        x, y, z = translate3d(data)
        self.q.put([x,y,z])
        print('len scan {}'.format(len(x)))
        self.finished.emit()

class MyWidget(QtCore.QObject):
    # 无参数的信号
    Signal_NoParameters = QtCore.pyqtSignal()
    def __init__(self):
        self.Signal_NoParameters.connect(win.onStart)
    def xx(self):
        self.trigger.emit()
class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        # self.widget_2.resize(759, 486)
        self.graph3DWidget = Surface3D_Graph(defaultNumberOfData, self.widget_3dscan)
        self.graph3DWidget.setMinimumSize(QtCore.QSize(600, 600))
        self.graph3DWidget.setObjectName("graph3DWidget")
        self.zoom_home.pressed.connect(lambda:self.graph3DWidget.home_view())
        self.zoom_left.pressed.connect(lambda:self.graph3DWidget.home_view('left'))
        self.zoom_right.pressed.connect(lambda:self.graph3DWidget.home_view('right'))
        self.zoom_in.pressed.connect(lambda:self.graph3DWidget.home_view('in'))
        self.zoom_out.pressed.connect(lambda:self.graph3DWidget.home_view('out'))
        self.get_color.pressed.connect(lambda:self.openColorDialog())
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.start_scan.pressed.connect(self.onStart)
        self.actionOpen.triggered.connect(lambda:self.open_file())
        self.actionSave.triggered.connect(lambda:self.saveFileDialog())
        self.onInit()
        self.getThread = ThreadExample()
        self.getThread.start()

        self.ptz =ptz()
        self.comboBox_serial.addItems(self.ptz.get_port_list())
        self.connect.pressed.connect(lambda:self.connect_serial())
        self.ptz_up.pressed.connect(lambda: self.ptz_go("up"))
        self.ptz_up.released.connect(lambda: self.ptz_go("stop"))
        self.ptz_down.pressed.connect(lambda: self.ptz_go("down"))
        self.ptz_down.released.connect(lambda: self.ptz_go("stop"))
        self.ptz_left.pressed.connect(lambda: self.ptz_go("left"))
        self.ptz_left.released.connect(lambda: self.ptz_go("stop"))
        self.ptz_right.pressed.connect(lambda: self.ptz_go("right"))
        self.ptz_right.released.connect(lambda: self.ptz_go("stop"))
        self.ptz_go_zeto.pressed.connect(lambda: self.ptz_go("zero"))

        self.scan_queue = Queue()

    def connect_serial(self):
        port = self.comboBox_serial.currentText()
        self.textEdit_debug.append('Connect Port{}'.format(port))
        # print()
        self.ptz.connect_port(port=port, baud=2400)
    def ptz_go(self, dir=""):
        if dir == "left":
            self.ptz.goLeft()
        elif dir == "right":
            self.ptz.goRight()
        elif dir == "up":
            self.ptz.goUp()
        elif dir == "down":
            self.ptz.goDown()
        elif dir == "stop":
            self.ptz.goStop()
        elif dir == "zero":
            self.ptz.goPose()
    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", "",
                                                  "Polygon File Format Files (*.ply);;Point Cloud Data Files (*.pcd)", options=options)
        if fileName:
            print(fileName)
            self.graph3DWidget.open_pcd(fileName)
            self.graph3DWidget.update_draw()

    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", "",
                                                  "Point Cloud Data Files (*.pcd);;Polygon File Format Files (*.ply)", options=options)
        if fileName[-4:] == '.ply' or fileName[-4:] == '.pcd':
            print(fileName)
            self.graph3DWidget.save_pcd(fileName)
    def openColorDialog(self):
        color = QtWidgets.QColorDialog.getColor()
        # self.get_color()
        if color.isValid():
            self.graph3DWidget.update_color(color.getRgb())
            print(color.getRgb())

    def timerEvent(self, event):
        if self.step >= 19:
            self.step = 0
            self.timer.stop()
            return
        self.step = self.step + 1
        self.progressBar.setValue(self.step)

    def onStart(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.close()
        add = self.lineEdit_lidaradd.text()
        print(add)
        # self.thread = QtCore.QThread()
        self.scan_thread = ThreadScan(add, self.scan_queue, self.s)
        # self.scan_thread = ThreadScan()
        # self.scan_thread.moveToThread(self.thread)
        self.scan_thread.finished.connect(self.doneScan)
        # self.thread.start()
        self.ptz.go180()
        self.scan_thread.start()
        self.step = 0
        if self.timer.isActive():
            self.timer.stop()
            # self.button.setText('Start')
        else:
            self.timer.start(1000, self)
            # self.button.setText('Stop')

    def doneScan(self):
        scan = self.scan_queue.get()
        scan_cloud = np.array(list(zip(scan[0], scan[1], scan[2])))
        self.graph3DWidget.updateDData(scan_cloud)
        self.graph3DWidget.update_draw()

    def onInit(self):
#usually a lot of connections here
        self.x_fit = np.linspace(1,10000, 10000)
        self.y_fit = [f(_x) for _x in self.x_fit]
        self.graphicsView.plot(self.x_fit,self.y_fit,symbol='o',pen=None)
        self.graphicsView.setLabel('left',text='toto',units='')
        self.graphicsView.setLabel('top',text='tata',units='')
        # self.ptz_up.pressed.connect(lambda:self.button_click())
        # datagrams_generator = decode_datagram(lidar_data)
        # yl,xl = translate(datagrams_generator)
        # self.graphicsView.plot(xl, yl)
    # def button_click(self):
    #     print("bbb")

def f(x):
    return x**2+1

if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app = QtGui.QApplication([])
        pg.setConfigOption('background', 'w')
        # loop = asyncio.get_event_loop()
        win = MyWindowClass()
        win.show()
        app.exec_()