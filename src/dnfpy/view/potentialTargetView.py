
from arrayView import ArrayView
from PyQt4 import QtCore
import plotArrayQt
from PyQt4 import QtGui
import numpy as np


class PotentialTargetView(ArrayView):
    def updateArray(self):
        self.targets = self.map.getData()
        self.sizeMap = self.map.getArg("sizeInput")
        data = self.map.getChild("input").getData()
        self.img = plotArrayQt.npToQImage(data)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawImage(event.rect(), self.img)



        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "targets: %s" %self.targets)



        size = self.rect().size()
        labWH = np.array([float(size.width()), float(size.height())])-1
        shapeWH = np.array([float(self.sizeMap),float(self.sizeMap)]) -1

        qp.setPen(QtGui.QColor(255,0,0))
        for coor in self.targets:
            coorWH = coor
            coorLab = np.round(coorWH / shapeWH * labWH)
            center = QtCore.QPoint(coorLab[0],coorLab[1])
            qp.drawEllipse(center,2,2)

