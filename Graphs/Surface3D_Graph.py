# -*- coding: utf-8 -*-
"""
Jan Adamczyk - 2018
"""
import os
import sys

import pyqtgraph.opengl as gl
import numpy as np
import datetime

import pcl


class Surface3D_Graph(gl.GLViewWidget):
    def __init__(self, defaultNumberOfData, parent=None, **kargs):
        super().__init__()
        self.numberOfData = defaultNumberOfData
        self.widthOfData = 500
        self.offset = 0
        self.color = None
        self.np_cloud = None
        self.size = None
        # pg.GraphicsWindow.__init__(self, **kargs)
        gl.GLViewWidget.__init__(self, **kargs)
        self.setParent(parent)
        self.setWindowTitle('Radar-Plot')
        # self.setBackgroundColor('w')
        # w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
        self.setCameraPosition(distance=10)

        self.adSurfaceGraph()

        self.show()

        # self.move((parent.width/2))

        g = gl.GLGridItem()
        g.scale(2, 2, 1)
        g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
        self.addItem(g)
        self.setWindowTitle('PAS Surfaceplot')
        # parent.get
        self.setGeometry(0, 0, parent.width(), parent.height())  # distance && resolution
        # self.setCameraPosition(distance=1000)

        ## Create axis
        # axis = pg.AxisItem('left', pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True)
        # axis.show()
        # axis = pg.AxisItem('left', pen = None)
        # xAxis.paint()
        # Axis.setSize(self.valueNumber, self.valueNumber, self.valueNumber)
        # axis.setStyle(showValues = True)
        # axis.show()
        # --------------------
        axis = gl.GLAxisItem()
        axis.setSize(x=10, y=10, z=10, size=None)
        # xAxis.paint()
        # axis.setSize(self.valueNumber, self.valueNumber, self.valueNumber)
        self.addItem(axis)
        # self.renderText(0., 0., 0., 'text')
    def mousePressEvent(self, ev):
        self.mousePos = ev.pos()
        print(self.mousePos)
        print(self.cameraPosition())
    def open_pcd(self, file_name='Andre_Agassi_0019.ply'):
        cloud = pcl.load(file_name)
        # cloud.
        self.np_cloud = np.asarray(cloud)
        # self.np_cloud[2] = self.np_cloud[2][::-1]
        # color = np.ones((np_cloud.shape[0],4))
        self.color = np.full((self.np_cloud.shape[0], 4), [0.2, 0, 0, 0.5])
        self.size = np.full((self.np_cloud.shape[0]), 0.02)
    def save_pcd(self, file_name=None):
        if file_name != None:
            cloud = pcl.PointCloud()
            cloud.from_array(self.np_cloud)
            pcl.save(cloud, file_name)
    def update_draw(self):
        self.surfacePlot.setData(pos = self.np_cloud, size = self.size, color=self.color, pxMode=False)
    def adSurfaceGraph(self):
        # cloud = pcl.load('downAndre_Agassi_0016.pcd')

        # for i in np.nditer(size, op_flags=['readwrite']):
        #     i = 1
        # xx = [x[0] for x in self.np_cloud]
        # yy = [x[0] for x in self.np_cloud]
        # zz = [x[0] for x in self.np_cloud]
        # zzz = np.array(zz)
        self.open_pcd()
        self.surfacePlot = gl.GLScatterPlotItem(pos = self.np_cloud, size=self.size, color=self.color, pxMode=False)
        self.addItem(self.surfacePlot)
    def update_color(self, color=None):
        self.color = np.full((self.np_cloud.shape[0],4), [i/255 for i in color])
        self.surfacePlot.setData(color=self.color)
    def addSurfaceGraph(self):
        self.x = np.linspace(-self.widthOfData / 2, self.widthOfData / 2, self.widthOfData)
        self.y = np.linspace(-self.numberOfData / 2, self.numberOfData / 2, self.numberOfData)
        self.surfacePlot = gl.GLSurfacePlotItem(self.x, self.y, shader='heightColor', computeNormals=False,
                                                smooth=False)  # smooth true = faster; dont turn on computenormals
        self.surfacePlot.shader()['colorMap'] = np.array([0.01, 0, 0.5, 0.01, 0, 1, 0.01, 0, 2])  # lut
        self.surfaceData = np.zeros((self.widthOfData, self.numberOfData), dtype=int)

        ## create a surface plot, tell it to use the 'heightColor' shader
        ## since this does not require normal vectors to render (thus we
        ## can set computeNormals=False to save time when the mesh updates)
        # p4.translate(100, 100, 0)
        self.addItem(self.surfacePlot)

        ## Add a grid to the view
        self.g = gl.GLGridItem()
        self.g.setSize(x=self.widthOfData * 2, y=self.numberOfData * 2)
        # g.scale(2,2,1000)
        self.g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
        self.addItem(self.g)

    # update via tcp
    def updateData(self, framesList):
        try:
            timeBeforeUpdate = datetime.datetime.now()
            for frame in framesList:
                self.surfaceData = np.delete(self.surfaceData, 0, 0)
                frame = np.array(frame, ndmin=2)
                for i in frame:
                    i += self.offset
                self.surfaceData = np.concatenate((self.surfaceData, frame))
                # print("x", len(self.x), "y", len(self.y), "data", self.surfaceData.shape)
            self.surfacePlot.setData(z=self.surfaceData)
            timeAfterUpdate = datetime.datetime.now()
            timeDiff = timeAfterUpdate - timeBeforeUpdate
            elapsed_ms = (timeDiff.days * 86400000) + (timeDiff.seconds * 1000) + (timeDiff.microseconds / 1000)
            # print(elapsed_ms, ' ms')
        except:
            print("3D Update:", sys.exc_info()[1])
            print("Expected Number of Data: ", self.surfaceData.shape[1], "Incoming Data: ", frame.size)

    # changes sample-quantity of shown data
    def updateWidthOfData(self, quantity):
        try:
            self.removeItem(self.surfacePlot)
            self.removeItem(self.g)
            self.widthOfData = quantity
            self.addSurfaceGraph()
        except:
            print("updateWidthOfData:", sys.exc_info()[1])

    # changes sample-quantity of incoming data
    def updateNumberOfData(self, quantity):
        try:
            self.removeItem(self.surfacePlot)
            self.removeItem(self.g)
            self.numberOfData = int(quantity)
            self.addSurfaceGraph()
        except:
            print("updateNumberOfData:", sys.exc_info()[1])

    def updateOffset(self, offset):
        self.offset = offset
    def home_view(self, dir = None):
        if dir == None:
            self.setCameraPosition(distance=10, elevation=60, azimuth=30)
        elif dir == 'left':
            # pos = self.cameraPosition()
            # pos
            # self.setCameraPosition(pos=)
            self.pan(self.opts['distance']/5,0,0)
        elif dir == 'right':
            self.pan(-self.opts['distance']/5,0,0)
        elif dir == 'in':
            self.setCameraPosition(distance=self.opts['distance']-2)
        elif dir == 'out':
            self.setCameraPosition(distance=self.opts['distance']+2)
        # self.show()