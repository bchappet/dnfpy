from PyQt4 import QtGui
import pyqtgraph as pg
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
from PyQt4 import QtCore
import numpy as np
import dnfpy.view.plotArrayQt
class ArrayView2(pg.GraphicsLayoutWidget):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnRClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(ArrayView2,  self).__init__()
        self.map = map
        #self.updateArray()
        self.runner = runner
        self.triggerOnClick.connect(runner.onClick)
        self.triggerOnRClick.connect(runner.onRClick)
        self.triggerOnParamChanged.connect(mapView.onParamsChanged)
        self.img = pg.ImageItem()
        self.img.setLookupTable(plotArrayQt.getColorMap())
        view = self.addViewBox()
        view.setAspectLocked(True)
        view.addItem(self.img)


       # qGraphicScene = QtGui.QGraphicsScene(self)
       # qGraphicScene.addItem(self.img)
       # self.setScene(qGraphicScene)

    def reset(self):
        pass

    def updateArray(self):
        self.array = np.copy(self.map.getData())
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
                self.img = plotArrayQt.npToQImage(stackedArray)
            else:
                self.img.setImage(self.array,autoDownsample=True,_callSync='off')
                print(self.array[70:,70:])
                
        else:
            pass



#    def mousePressEvent(self,  event):
#        labXY = np.array([event.x(), event.y()], dtype=np.float32)
#        size = self.rect().size()
#        labWH = np.array([size.width(), size.height()]) - 1
#        shapeWH = np.array([self.array.shape[0],
#                            self.array.shape[1]]) - 1
#        arrXY = (labXY / labWH) * shapeWH
#        arrXY = np.round(arrXY).astype(int)
#        #value = self.array[arrXY[1], arrXY[0]]
#        #print arrXY
#        #print value
#        if event.buttons() == QtCore.Qt.LeftButton:
#            self.triggerOnClick.emit(self.map.getName(),arrXY[0],arrXY[1])
#        elif event.button() == QtCore.Qt.RightButton:
#            self.triggerOnRClick.emit(self.map.getName(),arrXY[0],arrXY[1])
#
#        self.triggerOnParamChanged.emit()#TDOD dirty
