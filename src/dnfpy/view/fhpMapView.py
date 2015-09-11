from PyQt4 import QtGui
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
from PyQt4 import QtCore
import numpy as np
import dnfpy.view.plotArrayQt
import pyqtgraph as pg
from scipy import signal
from scipy import ndimage
import scipy as sp
import cv2

from dnfpy.view.arrayView import ArrayView


from scipy.interpolate import interpolate

def permute(a,b):
        xx,yy = np.meshgrid(a,b)
        size2 = len(a) * len(b)
        xx = xx.reshape(size2)
        yy = yy.reshape(size2)
        return (np.dstack((xx,yy))).reshape(len(a),len(b),2)

def interpolateArray(data,shape,kind='linear'):
        X,Y = np.meshgrid(np.arange(data.shape[0]),np.arange(data.shape[1]))
        outgrid = interpolate.interp2d(X,Y,data,kind=kind)
        xi = np.linspace(0,data.shape[0],shape[0])
        yi = np.linspace(0,data.shape[1],shape[1])
        z = outgrid(xi,yi)
        return z



class FhpMapView(ArrayView):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnRClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(FhpMapView,  self).__init__(map,runner,mapView)
        #self.stateList.append("speed")
        self.size =self.map.getArg('size')
        self.nbPoints = 50

        x = np.linspace(0,1,self.nbPoints)
        y = np.linspace(0,1,self.nbPoints)
        self.points = permute(x,y)
        


    def updateArray(self):
        super(FhpMapView,self).updateArray()
        if self.viewState == "speed":
            self.speedViewUpdate()

    def paintEvent(self, event):
        super(FhpMapView,self).paintEvent(event)
        if self.viewState == "speed":
            self.paintSpeed(event)


    def speedViewUpdate(self):
        self.speed = self.map.celerity(self.map.getData())
        speedX = self.speed[:,:,1]
        speedY = self.speed[:,:,0]

        #echantillone
#        downX = speedX[::self.step,::self.step]
#        downY = speedY[::self.step,::self.step]
        downX = cv2.resize(speedX,(self.nbPoints,self.nbPoints))
        downY = cv2.resize(speedY,(self.nbPoints,self.nbPoints))

        self.vectors = np.dstack((downX,downY))
        self.vectors = self.vectors



    def paintSpeed(self,event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QColor(0,0,125))


        size = self.rect().size()
        sizeWH = np.array([size.width(), size.height()])
        pts = self.points * sizeWH
        #print self.vectors
        vects = self.vectors/self.nbPoints*sizeWH
        vect2 = pts + vects
        qtLines = []
        for i in range(vects.shape[0]):
            for j in range(vects.shape[1]):
                p = pts[j,i,:]
                v = vect2[j,i,:]
                qpt = QtCore.QPointF(p[0],p[1])
                qv = QtCore.QPointF(v[0],v[1])
                qtLines.append(QtCore.QLineF(qpt,qv))
                #print "v : ",v

        qp.drawLines(qtLines)




    def paintArray(self,event):
        qp = QtGui.QPainter(self)
        if self.img:
            qp.drawImage(event.rect(), self.img)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%.2f" %
                    self.max)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%.2f" %
                    self.min)

