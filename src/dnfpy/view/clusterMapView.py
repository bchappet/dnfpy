from dnfpy.view.arrayView import ArrayView
from PyQt4 import QtCore
import dnfpy.view.plotArrayQt
from PyQt4 import QtGui
import numpy as np

class ClusterMapView(ArrayView):
     def updateArray(self):
         np.set_printoptions(formatter={'float': '{: 0.2f}'.format})
         self.kernels = self.map.getData()
         self.sizeMap = self.map.getArg("sizeNpArr")
         self.sizeCluster = self.map.getArg("clustSize_")
         np_arr = self.map.getChildren()["np_arr"].getData()
         self.img = plotArrayQt.npToQImage(np_arr)
         self.nb_outliners = self.map.getArg("nbOutliners")



     def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawImage(event.rect(), self.img)
        size = self.rect().size()

        nbKernel = len(self.kernels)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "kernels: %s" %self.kernels)
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop ,  "nbOutliners: %s" %self.nb_outliners)

        labWH = np.array([float(size.width()), float(size.height())])-1
        shapeWH = np.array([float(self.sizeMap),float(self.sizeMap)]) -1

        #qp.drawImage(event.rect(), self.img)
        sizeClusterArr = np.array([self.sizeCluster,self.sizeCluster])
        qp.setPen(QtGui.QColor(255,0,0))
        circleRadius = np.round(sizeClusterArr/(shapeWH+1)*(labWH+1)/2.)
        for coor in self.kernels:
            coorLab = np.round(coor / shapeWH * labWH)
            center = QtCore.QPoint(coorLab[0],coorLab[1])
            qp.drawEllipse(center,2,2)
            qp.drawEllipse(center,circleRadius[0],circleRadius[1])



