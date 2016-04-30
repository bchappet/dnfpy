
from dnfpy.view.arrayView import ArrayView
from PyQt4 import QtCore
import dnfpy.view.plotArrayQt as plotArrayQt
from PyQt4 import QtGui
import numpy as np
from dnfpy.view.trajectoryView import TrajectoryView


class TupleView(TrajectoryView):
    """
    Display the tuple as a trace [x,y]
    If the tuple is 1-dimensional with display [x,t]

    if there are several tuples in map.getViewData() they will be all traced on the same canva (and scale)


    expect the map to have getViewSpace() method to get the shape of the space where to plot the tuple


    """
    def updateArray(self):
        points =  self.map.getViewData()
        if points is None:
            points = self.map.getData()


        dim = self.map.getArg('dim')
        try:#test that it is a tuple of coords
            if dim == 2:
                x = points[0][0]
            elif dim == 1:
                x = points[0]    
        except (IndexError,TypeError):
            points = (points,)

        #if dim > 1:
            #print(self.map.getName())
            #assert(len(points[0]) == dim)
        
        #make sure data has the rigth len
        nbCoords = len(points)
        while len(self.data) < nbCoords:
                self.data.append([])


        if dim == 1: #we add time to the tuple
            self.time = self.map.getArg("time")
            for i in range(len(points)):
                self.data[i].append(np.array([self.time,points[i]]))
        else:
            for i in range(len(points)):
                    self.data[i].append(np.array(points[i]))

        points = np.array(points)

        self.updateMinMax()
        if len(self.data[0]) > self.curveSize: #max point on the curve
            for i in range(len(self.data)):
                del self.data[i][0]

    def updateMinMax(self):
            shapeSpace = self.map.getViewSpace()
            if len(shapeSpace) == 1:
                    #1 dim space, max x is the max time, min x is the min time
                    minTmp = np.min(np.nanmin(self.data,axis=1),axis=0)
                    maxTmp = np.max(np.nanmax(self.data,axis=1),axis=0) #global max for x and y
                    self.minPt = np.array([minTmp[0],0])
                    self.maxPt = np.array([maxTmp[0],shapeSpace[0]])
            elif len(shapeSpace) == 2:
                    self.minPt = np.array([0,0])
                    self.maxPt = np.array([shapeSpace[0],shapeSpace[1]])
            else:
                    pass

            assert(len(self.maxPt) == 2)
            assert(len(self.minPt) == 2)








