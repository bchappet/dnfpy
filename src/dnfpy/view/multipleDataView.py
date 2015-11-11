from PyQt4 import QtGui
import qimage2ndarray #http://kogs-www.informatik.uni-hamburg.de/~meine/software/qimage2ndarray/doc/#converting-ndarrays-into-qimages
from PyQt4 import QtCore
import numpy as np
import dnfpy.view.plotArrayQt
from dnfpy.view.arrayView import ArrayView



def colStr(color):
    return str(color.red())+","+str(color.green())+","+str(color.blue())+","+str(color.alpha())


def getColorTables(colors):
        li = []
        for col in colors:
            li.append(getColorTable(col))
        return li

def getColorTable(color):
        li = []
        col = QtGui.QColor(color)
        for i in range(256):
            col.setAlpha(i)
            li.append(col.rgba())

        #print("color : %s : %s"%(colStr(QtGui.QColor(li[1])),colStr(QtGui.QColor(li[-1]))))
        return li





class MultipleDataView(ArrayView):
    """
    Only 2D for now
    """
    def __init__(self,map,runner,mapView):
            self.liCT = None
            self.compositionMode = QtGui.QPainter.CompositionMode_Multiply
            super().__init__(map,runner,mapView)
            self.images = []

    def updateArray(self):
        self.viewData = self.map.getViewData() #should be tuple
        if not(self.liCT):
                self.liCT = getColorTables(self.map.getColors())

        if self.viewData is None:
            self.viewData = (self.map.getData(),)
        self.array = self.viewData[0]

        self.images = []
        for i in range(len(self.viewData)):
            data = self.viewData[i]
            img = qimage2ndarray.gray2qimage(data,(0,np.max(data)))
            img.setColorTable(self.liCT[i])
            self.images.append(img)

        #now merge the image with différent color

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setCompositionMode(self.compositionMode)
        for img in self.images:
            qp.drawImage(event.rect(), img)







