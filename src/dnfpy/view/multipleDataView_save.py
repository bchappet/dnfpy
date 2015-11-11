from PyQt4 import QtGui
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
from PyQt4 import QtCore
import numpy as np
import plotArrayQt
from dnfpy.view.arrayView import ArrayView

class MultipleDataView(QtGui.QLabel):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnRClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(MulipleDataView,  self).__init__()
        self.map = map
        self.updateArray()
        self.runner = runner
        self.triggerOnClick.connect(runner.onClick)
        self.triggerOnRClick.connect(runner.onRClick)
        self.triggerOnParamChanged.connect(mapView.onParamsChanged)
        self.img = None

    def reset(self):
        pass

    def updateArray(self):
        self.viewData = self.map.getViewData()


        if isinstance(self.array,np.ndarray):
            if self.array.shape == (1,1,3):
                #assume hsv
                self.img = QtGui.QImage(1,1,QtGui.QImage.Format_RGB32)
                hsv = [self.array[0,0,0]*2,self.array[0,0,1],self.array[0,0,2]]
                rgbCol = QtGui.QColor.fromHsv(*hsv)
                self.img.fill(rgbCol)
            elif self.array.dtype == np.bool and len(self.array.shape) > 2:
                #it a 2D map of boolean. We sum the 3d dimension leayers
                stackedArray = np.sum(self.array,axis=2)
                self.img = plotArrayQt.npToQImage(stackedArray,self.max,self.min)
            else:
                self.img = plotArrayQt.npToQImage(self.array,self.max,self.min)
        else:
            pass


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        if self.img:
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
        arrXY = np.round(arrXY).astype(int)
        #value = self.array[arrXY[1], arrXY[0]]
        #print arrXY
        #print value
        if event.buttons() == QtCore.Qt.LeftButton:
            self.triggerOnClick.emit(self.map.getName(),arrXY[0],arrXY[1])
        elif event.button() == QtCore.Qt.RightButton:
            self.triggerOnRClick.emit(self.map.getName(),arrXY[0],arrXY[1])

        self.triggerOnParamChanged.emit()#TDOD dirty
