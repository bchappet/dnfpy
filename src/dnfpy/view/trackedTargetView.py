
from dnfpy.view.arrayView import ArrayView
from PyQt4 import QtCore
import dnfpy.view.plotArrayQt as plotArrayQt
from PyQt4 import QtGui
import numpy as np


class TrackedTargetView(ArrayView):
    def updateArray(self):
        self.trackedTargets = self.map.getData()
        self.sizeMap = self.map.getArg("sizeArray")

        self.targets = self.map.getChild("potentialTarget").getData()
        clusterMap = self.map.getChild("clusterMap")
        self.sizeCluster = clusterMap.getArg("clustSize_")
        self.clusters = clusterMap.getData()
        data = clusterMap.getChild("np_arr").getData()
        self.img = plotArrayQt.npToQImage(data)
        self.distMax = self.map.getArg("distMax_")

        self.img = self.img.convertToFormat(QtGui.QImage.Format_ARGB32)
        #set the image transparent
        p = QtGui.QPainter(self.img)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_DestinationIn);
        p.fillRect(self.img.rect(), QtGui.QColor(0,0,0,150));
        p.end();



    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawImage(event.rect(), self.img)

        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "distMax_: %s" %self.distMax)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "targets: %s" %self.trackedTargets)

        size = self.rect().size()
        labWH = np.array([float(size.width()), float(size.height())])-1
        shapeWH = np.array([float(self.sizeMap),float(self.sizeMap)]) -1


        qp.setPen(QtGui.QColor(255,0,0))
        for coor in self.targets:
            coorWH = coor
            coorLab = np.round(coorWH / shapeWH * labWH)
            center = QtCore.QPoint(coorLab[0],coorLab[1])
            qp.drawEllipse(center,2,2)


        sizeClusterArr = np.array([self.sizeCluster,self.sizeCluster])
        circleRadius = np.round(sizeClusterArr/(shapeWH+1)*(labWH+1)/2.)
        for coor in self.clusters:
            coorLab = np.round(coor / shapeWH * labWH)
            center = QtCore.QPoint(coorLab[0],coorLab[1])
            qp.drawEllipse(center,2,2)
            qp.drawEllipse(center,circleRadius[0],circleRadius[1])

        qp.setPen(QtGui.QPen(QtGui.QColor(0,0,0),3))
        for i in range(len(self.trackedTargets)):
            clust = self.clusters[i]
            target = self.trackedTargets[i]
            clustLab = np.round(clust / shapeWH * labWH)
            targetLab = np.round(target / shapeWH * labWH)
            qp.drawLine(clustLab[0],clustLab[1],targetLab[0],targetLab[1])




