
from arrayView import ArrayView
from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy as np


class ErrorDistView(ArrayView):
    def __init__(self,  map, runner,mapView):
        self.reset()
        self.curveSize = 100
        super(ErrorDistView,self).__init__(map,runner,mapView)

    def reset(self):
        self.pt = []
        self.maxPt = np.ones((2))
        self.minPt = np.zeros((2))


    def updateArray(self):
        self.errors = np.sum(self.map.getData())
        self.time = self.map.getArg("time")
        self.mean = self.map.getArg("mean")
        if self.errors > 0:
            pt = np.array([self.time,self.errors])
            self.pt.append(pt)
            self.updateMinMax()
            if len(self.pt) > self.curveSize:
                del self.pt[0]
        else:
            pass

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

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QColor(0,0,0))
        if self.errors > 0:
            qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "error: %f" %self.errors)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "meanError: %f" %self.mean)

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

            #draw line for mean error
            qp.setPen(QtGui.QPen(QtGui.QColor(255,0,0),3))
            scaledMeanStart =  self.scale(np.array([self.minPt[0],self.mean]),sizeWH)
            scaledMeanEnd = self.scale(np.array([self.maxPt[0],self.mean]),sizeWH)
            qp.drawLine(scaledMeanStart[0],scaledMeanStart[1],scaledMeanEnd[0],scaledMeanEnd[1])

    def scale(self,pt,sizeWH):
        scaled = (pt - self.minPt)/(self.maxPt-self.minPt)
        shifted = np.array([scaled[0], 1 - scaled[1]])
        return  np.round(shifted*sizeWH).astype(np.int)




