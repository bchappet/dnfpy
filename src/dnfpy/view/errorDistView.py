
from arrayView import ArrayView
from PyQt4 import QtCore
import plotArrayQt
from PyQt4 import QtGui
import numpy as np


class ErrorDistView(ArrayView):
    def __init__(self,  map, runner,mapView):
        self.pt = []
        self.curveSize = 100
        super(ErrorDistView,self).__init__(map,runner,mapView)

    def updateArray(self):
        self.errors = self.map.getData()
        self.time = self.map.getArg("time")
        if len(self.errors) > 0:
            pt = np.array([self.time,self.errors[0]])
        else:
            pt = np.array([self.time,-1])
        self.pt.append(pt)
        if len(self.pt) > self.curveSize:
            del self.pt[0]

        self.maxPt = np.max(self.pt,axis=0)
        self.minPt = np.min(self.pt,axis=0)


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QColor(0,0,0))
        if len(self.errors) > 0:
            qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "error: %s" %self.errors[0])

        if len(self.pt ) > 0:
            qp.setPen(QtGui.QPen(QtGui.QColor(0,0,0),3))
            size = self.rect().size()
            sizeWH = np.array([size.width(), size.height()])
            prevPt = QtCore.QPoint(self.pt[0][0],self.pt[0][1])
            for i in range(1,len(self.pt)):
                newPtnp= self.scale(self.pt[i],sizeWH)
                newPtnp =  np.round(newPtnp)
                newPtnp = newPtnp.astype(np.int)
                newPt = QtCore.QPoint(newPtnp[0],newPtnp[1])
                qp.drawLine(prevPt,newPt)
                prevPt = newPt

    def scale(self,pt,sizeWH):
        scaled = (pt - self.minPt)/(self.maxPt-self.minPt)
        shifted = np.array([scaled[0], 1 - scaled[1]])
        return  shifted*sizeWH




