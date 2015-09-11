from PyQt4 import QtGui
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
from PyQt4 import QtCore
import numpy as np
import dnfpy.view.plotArrayQt as plotArrayQt
import pyqtgraph as pg
from scipy import signal
from scipy import ndimage


def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


class ArrayView(QtGui.QLabel):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnRClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(ArrayView,  self).__init__()
        self.map = map
        self.runner = runner
        self.triggerOnClick.connect(runner.onClickSlot)
        self.triggerOnRClick.connect(runner.onRClickSlot)
        self.triggerOnParamChanged.connect(mapView.onParamsChanged)
        self.stateList = ["default","1D"]
        self.viewState = "default"
        self.layout = QtGui.QHBoxLayout(self)
        self.img = None
        self.barGraph = None
        self.updateArray()

    def reset(self):
        pass

    def updateArray(self):
        self.array =  self.map.getViewData()
        if self.array is None:
            self.array = self.map.getData()

        if self.viewState == "default":
            self.arrayViewUpdate()
        elif self.viewState == "1D":
            self.oneDimViewUpdate()

    def oneDimViewUpdate(self):
        size = self.array.shape[0]
        #projection = array[sizeY/2,:]
        projection = np.mean(self.array[size/2-size/4:size/2+size/4],axis=0)
        kernel = signal.gaussian(10,10)
        projection = moving_average(projection,n=size/10)
        #projection = ndimage.convolve(projection,kernel,mode='wrap')/np.sum(kernel)

        x = range(len(projection))
        self.pt = np.array([x,projection]).T.astype(np.float)
        self.updateMinMax()

    def updateMinMax(self):
        maxTmp = np.max(self.pt,axis=0)
        minTmp = np.min(self.pt,axis=0)
        if (maxTmp != minTmp).all():
            self.maxPt = maxTmp
            self.minPt = minTmp
        elif (maxTmp == minTmp).all():
            pass
        elif maxTmp[0] == minTmp[0]:
            self.maxPt[1] = maxTmp[1]
            self.minPt[1] = minTmp[1]
        elif maxTmp[1] == minTmp[1]:
            self.maxPt[0] = maxTmp[0]
            self.minPt[0] = minTmp[0]






    def arrayViewUpdate(self):
        self.min = np.min(self.array)
        self.max = np.max(self.array)
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
                self.img = plotArrayQt.npToQImage2(stackedArray,self.max,self.min)
            elif self.array.dtype == np.bool_:
                self.array = self.array.astype(np.uint8,copy=False)
                self.img = plotArrayQt.npToQImage2(self.array,1,0)
            else:
                self.img = plotArrayQt.npToQImage2(self.array,self.max,self.min)
        else:
            pass

    def toggleView(self):
        iState = self.stateList.index(self.viewState)
        iState = (iState + 1) % len(self.stateList)
        self.viewState = self.stateList[iState]


    def paintEvent(self, event):
        if self.viewState == "default":
            self.paintArray(event)
        elif self.viewState == "1D":
            self.paintOneDim(event)

    def paintOneDim(self,event):
        qp = QtGui.QPainter(self)

        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%.2f" %
                    self.maxPt[1])
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%.2f" %
                    self.minPt[1])

        qp.setPen(QtGui.QColor(0,0,125))

        if len(self.pt ) > 1:
            qp.setPen(QtGui.QPen(QtGui.QColor(0,0,0),2))
            size = self.rect().size()
            sizeWH = np.array([size.width(), size.height()])
            prevPtNp = self.scale(self.pt[0],sizeWH)
            prevPt = QtCore.QPoint(prevPtNp[0],prevPtNp[1])
            for i in range(1,len(self.pt)):
                newPtnp = self.scale(self.pt[i],sizeWH)
                newPt = QtCore.QPoint(newPtnp[0],newPtnp[1])
                qp.drawLine(prevPt,newPt)
                prevPt = newPt

    def scale(self,pt,sizeWH):
        scaled = (pt - self.minPt)/(self.maxPt-self.minPt)
        shifted = np.array([scaled[0], 1 - scaled[1]])
        res = np.round(shifted*sizeWH).astype(np.int)
        return res


    def paintArray(self,event):
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
