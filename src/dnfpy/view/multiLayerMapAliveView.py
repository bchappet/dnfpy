from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy as np
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
import plotArrayQt
from multiLayerMapView import MultiLayerMapView

colors = ['white','red','green','blue','purple','cyan']

def colStr(color):
    return str(color.red())+","+str(color.green())+","+str(color.blue())+","+str(color.alpha())

class MultiLayerMapAliveView(MultiLayerMapView):
    def __init__(self,  map, runner,mapView):
        self.liCT = self.getColorTables()
        super(MultiLayerMapAliveView,  self).__init__(map,runner,mapView)


    def updateArray(self):
        self.array = self.map.getData()
        self.min = np.min(self.array)
        self.max = np.max(self.array)

        #Potentials are B&W
        self.imgList = []
        img = plotArrayQt.npToQImage(self.array)
        self.imgList.append(img)

        colorMaps = self.map.getColors()
        for i in range(1,colorMaps.shape[2]):
            a = colorMaps[:,:,i]
            img = qimage2ndarray.gray2qimage(a,(0,np.max(a)))
            img.setColorTable(self.liCT[i])
            self.imgList.append(img)


    def getColorTables(self):
        li = []
        for col in colors:
            li.append(self.getColorTable(col))
        return li

    def getColorTable(self,color):
        li = []
        col = QtGui.QColor(color)
        for i in range(256):
            col.setAlpha(i)
            li.append(col.rgba())


        print("color : %s : %s"%(colStr(QtGui.QColor(li[1])),colStr(QtGui.QColor(li[-1]))))
        return li


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setCompositionMode(self.compositionMode)
        for img in self.imgList:
            qp.drawImage(event.rect(), img)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%.2f" %
                    self.max)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%.2f" %
                    self.min)
