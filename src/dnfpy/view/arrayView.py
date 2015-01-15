from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy as np
import plotArrayQt

class ArrayView(QtGui.QLabel):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(ArrayView,  self).__init__()
        self.map = map
        self.updateArray()
        self.runner = runner
        self.triggerOnClick.connect(runner.onClick)
        self.triggerOnParamChanged.connect(mapView.onParamsChanged)

    def updateArray(self):
        self.array = self.map.getData()
        self.min = np.min(self.array)
        self.max = np.max(self.array)

        if self.array.shape == (1,1,3):
            #assume hsv
            self.img = QtGui.QImage(1,1,QtGui.QImage.Format_RGB32)
            hsv = [self.array[0,0,0]*2,self.array[0,0,1],self.array[0,0,2]]
            rgbCol = QtGui.QColor.fromHsv(*hsv)
            self.img.fill(rgbCol)
        else:
            self.img = plotArrayQt.npToQImage(self.array)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawImage(event.rect(), self.img)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%.2f" %
                    self.max)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%.2f" %
                    self.min)

    def mousePressEvent(self,  event):
        labXY = np.array([event.x(), event.y()], dtype=np.float32)
        size = self.rect().size()
        labWH = np.array([size.width(), size.height()]) - 1
        shapeWH = np.array([self.array.shape[0],
                            self.array.shape[1]]) - 1
        arrXY = (labXY / labWH) * shapeWH
        arrXY = np.round(arrXY)
        value = self.array[arrXY[1], arrXY[0]]
        print arrXY
        print value
        self.triggerOnClick.emit(self.map.getName(),arrXY[0],arrXY[1])
        self.triggerOnParamChanged.emit()#TDOD dirty
