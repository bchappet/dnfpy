import math
import sip
from PyQt4 import QtGui
from PyQt4 import QtCore
import plotArrayQt
import numpy as np
from PyQt4.QtCore import pyqtSlot
from paramsView import ParamsView
class ArrayWidget(QtGui.QGroupBox):

    def __init__(self,map,runner,parametersView,view):
        super(ArrayWidget,self).__init__(title=map.getName())
        self.map = map
        self.view = view
        self.runner = runner
        self.parametersView = parametersView
        self.label = ArrayLabel(self.map,runner,self)
        self.label.setScaledContents(True)
        params = ArrayButtons(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(2,10,2,2)
        self.layout.addWidget(self.label)
        self.layout.addWidget(params)
        self.paramsDisplayed = False
        self.paramDict = None

    def updateArray(self):
        self.label.updateArray()
        if self.paramDict:
            self.paramDict.onMapUpdate()
    @pyqtSlot()
    def onParamsChanged(self):
        if self.paramDict:
            self.paramDict.onParamUpdate()
        

    @pyqtSlot()
    def displayParams(self):
        name = self.map.getName()
        if not (self.paramsDisplayed) :
            self.box = QtGui.QGroupBox(name)
            self.paramsDisplayed = True
            #self.arrayParam = ArrayParams(self.map)
            self.paramDict = ParamsView(self.map,self.runner,self.view)
            self.layoutB = QtGui.QVBoxLayout(self.box)
            #layout.addWidget(self.arrayParam)
            self.layoutB.addWidget(self.paramDict)

            self.parametersView.addWidget(name,self.box)
        else:
            self.paramsDisplayed = False
            sip.delete(self.paramDict)
            self.paramDict = None
            sip.delete(self.box)
            self.box = None

            self.parametersView.removeWidget(name)


class ArrayButtons(QtGui.QWidget):
    def __init__(self,arrayWidget):
        super(ArrayButtons,self).__init__()
        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        bParams = QtGui.QPushButton("Infos")
        layout.addWidget(bParams)
        bParams.clicked.connect(arrayWidget.displayParams)



class ArrayLabel(QtGui.QLabel):
    triggerOnClick = QtCore.pyqtSignal(str,int,int)#Will be triggered on click
    triggerOnParamChanged = QtCore.pyqtSignal()
    #map name coord x y
    def __init__(self,  map, runner,mapView):
        super(ArrayLabel,  self).__init__()
        self.map = map
        self.updateArray()
        self.runner = runner
        self.triggerOnClick.connect(runner.onClick)
        self.triggerOnParamChanged.connect(mapView.onParamsChanged)

    def updateArray(self):
        self.array = self.map.getData()
        self.img = plotArrayQt.npToQImage(self.array)
        self.min = np.min(self.array)
        self.max = np.max(self.array)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawImage(event.rect(), self.img)
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawText(event.rect(),  QtCore.Qt.AlignTop,  "%.2f" %
                    self.max)
        qp.drawText(event.rect(),  QtCore.Qt.AlignBottom,  "%.2f" %
                    self.min)

    def mousePressEvent(self,  event):
        labXY = np.array([event.x(), event.y()], dtype=np.float32)
        size = self.rect().size()
        labWH = np.array([size.width(), size.height()]) - 1
        shapeWH = np.array([self.array.shape[0],
                            self.array.shape[1]]) - 1
        arrXY = (labXY / labWH) * shapeWH
        arrXY = np.round(arrXY)
        value = self.array[arrXY[1], arrXY[0]]
        print arrXY
        print value
        self.triggerOnClick.emit(self.map.getName(),arrXY[0],arrXY[1])
        self.triggerOnParamChanged.emit()#TDOD dirty



