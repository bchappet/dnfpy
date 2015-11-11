
from dnfpy.view.arrayView import ArrayView
from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy as np
import warnings


class TrajectoryView(ArrayView):
    """
    For map of dimension 0

    the data for plot are get from map.getViewData() (if None with map.getData())

    if the data is a tuple, there will be a many curves as element


    """
    def __init__(self,  map, runner,mapView):
        self.reset()
        self.curveSize = 200
        super(TrajectoryView,self).__init__(map,runner,mapView)
        self.color_cycle = [QtGui.QColor(0,0,0),QtGui.QColor(0,0,255),QtGui.QColor(0,255,0),QtGui.QColor(255,0,0)]

    def reset(self):
        self.data = [] #[curve,time,xy]
        finfo = np.finfo(float)
        self.maxPt = np.ones((2))*finfo.min
        self.minPt = np.ones((2))*finfo.max


    def updateArray(self):
        points =  self.map.getViewData()
        if points is None:
            points = self.map.getData()


        #make sure it is iterable
        try:
            iterator = iter(points)
        except TypeError:
            points = (points,)
        
        #make sure data has the rigth len
        while len(self.data) < len(points):
                self.data.append([])


        self.time = self.map.getArg("time")
        for i in range(len(points)):
            self.data[i].append(np.array([self.time,points[i]]))

        self.updateMinMax()
        if len(self.data[0]) > self.curveSize: #max point on the curve
            for i in range(len(self.data)):
                del self.data[i][0]

    def updateMinMax(self,mode='global'):

            minTmp = np.nanmin(np.nanmin(self.data,axis=1),axis=0)
            maxTmp = np.nanmax(np.nanmax(self.data,axis=1),axis=0) #global max for x and y

            if mode == 'global':
                    self.maxPt[1] = np.maximum(self.maxPt[1],maxTmp[1])
                    self.minPt[1] = np.minimum(self.minPt[1],minTmp[1])
                    self.maxPt[0] = maxTmp[0]
                    self.minPt[0] = minTmp[0]
                    
            else:
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

            #assert(len(self.data[0][0]) == 2)
            assert(len(self.maxPt) == 2)
            assert(len(self.minPt) == 2)
            assert(not(np.isnan(self.maxPt).any()))

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%f" %self.maxPt[1])
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%f" %self.minPt[1])


        value = [str(self.data[x][-1]) for x in range(len(self.data))]
        value = ', '.join(value)
        qp.drawText(event.rect(),  QtCore.Qt.AlignCenter,  "%s" %value)

        qp.drawText(event.rect(),  QtCore.Qt.AlignRight,  "%f" %self.maxPt[0])

        if len(self.data[0]) > 1:
            size = self.rect().size()
            sizeWH = np.array([size.width(), size.height()])

            for j in range(0,len(self.data)): #j is the curve
                qp.setPen(QtGui.QPen(self.color_cycle[j],2)) #set the color

                #take the first non nan point
                i1 = 0
                while i1 < len(self.data[j]) and np.isnan(self.data[j][i1]).all() :
                    i1 = i1 +1
                prevPtNp = self.scale(self.data[j][i1],sizeWH)
                prevPt = QtCore.QPoint(prevPtNp[0],prevPtNp[1])
                #plot the rest non nan (TODO remove nan before plotting (if we don't need data for stats))
                for i in range(i1+1,len(self.data[j])):
                    thePoint = self.data[j][i]
                    if np.isnan(thePoint).any():
                        pass
                    else:
                        newPtnp = self.scale(thePoint,sizeWH)
                        newPt = QtCore.QPoint(newPtnp[0],newPtnp[1])
                        qp.drawLine(prevPt,newPt)
                        prevPt = newPt


    def scale(self,pt,sizeWH):
        scaled = (pt - self.minPt)/(self.maxPt-self.minPt)
        shifted = np.array([scaled[0], 1 - scaled[1]])
        return  np.round(shifted*sizeWH).astype(np.int)




