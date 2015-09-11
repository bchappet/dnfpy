from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy as np
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
import dnfpy.view.plotArrayQt
from dnfpy.view.arrayView import ArrayView

colors = ['white','red','green','blue','purple','cyan']

def col(color):
    return str(color.red())+","+str(color.green())+","+str(color.blue())+","+str(color.alpha())

class MultiLayerMapView(ArrayView):
    def __init__(self,  map, runner,mapView):
        self.ctFlat = self.getColorTableFlat()
        self.compositionMode = QtGui.QPainter.CompositionMode_Multiply
        if map.getType() == 'binary':
            self.compositionMode = QtGui.QPainter.CompositionMode_SourceOver
        super(MultiLayerMapView,  self).__init__(map,runner,mapView)

    def flattenColorLayers(self,colorMaps):
        res = np.zeros((colorMaps.shape[0],colorMaps.shape[1]),dtype=np.uint8)
        for i in range(colorMaps.shape[2]):
            res += colorMaps[:,:,i].astype(np.uint8) * (i)

        #print res


        return res

    def updateArray(self):
        self.array = self.map.getData()
        self.min = np.min(self.array)
        self.max = np.max(self.array)

        #Potentials are B&W
        img = plotArrayQt.npToQImage(self.array)
        self.imgList = [img]

        colorMaps = self.map.getColors()
        flat = self.flattenColorLayers(colorMaps)

        #print flat[30:50,30:50]
        imgFlat = qimage2ndarray.gray2qimage(flat)
        imgFlat.setColorTable(self.ctFlat)

        self.imgList.append(imgFlat)

    def getColorTableFlat(self):
        trans = QtGui.QColor(255,255,255,0).rgba()
        li = [trans]*256

        for i in range(len(colors)):
            col = QtGui.QColor(colors[i])
            li[i] = col.rgba()
        return li

    def getColorTable(self,color):
        colEnd = QtGui.QColor(color)
        colEnd.setAlpha(125)

        trans = QtGui.QColor(255,255,255,0).rgba()
        li = [trans]*256
        li[255] = colEnd.rgba()

        #print("color : %s : %s"%(col(QtGui.QColor(li[0])),col(QtGui.QColor(li[-1]))))
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
