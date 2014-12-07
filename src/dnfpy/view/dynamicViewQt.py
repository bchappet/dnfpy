from PyQt4 import QtGui,  QtCore
from PyQt4.QtCore import pyqtSlot
import math
import numpy as np
from view import View
from parametersView import ParametersView
from mapView import ArrayWidget


class GlobalParams(QtGui.QWidget):
        """
            Global parameter of the runner
        """
        def __init__(self, runner):
            super(GlobalParams, self).__init__()

            self.runner = runner
            layout = QtGui.QHBoxLayout(self)
            bSaveFig = QtGui.QPushButton("Save Figures")
            bSaveFig.clicked.connect(runner.saveFigSlot)
            bSaveArr = QtGui.QPushButton("Save Data")
            bSaveArr.clicked.connect(runner.saveArrSlot)
            bPlay = QtGui.QPushButton("Play/Pause")
            bPlay.clicked.connect(runner.playSlot)
            bStep = QtGui.QPushButton("Step")
            bStep.clicked.connect(runner.stepSlot)
            spinSpeedRatio = QtGui.QDoubleSpinBox()
            spinSpeedRatio.setMinimum(0.0)
            spinSpeedRatio.setMaximum(10.0)
            spinSpeedRatio.setValue(runner.getTimeRatio())
            spinSpeedRatio.setSingleStep(0.1)
            spinSpeedRatio.setDecimals(1)
            spinSpeedRatio.valueChanged.connect(runner.setTimeRatio)
            spinSpeedRatio.setPrefix("Speed : ")

            layout.addWidget(bSaveFig)
            layout.addWidget(bSaveArr)
            layout.addWidget(bPlay)
            layout.addWidget(bStep)
            layout.addWidget(spinSpeedRatio)


class DisplayModelQt(QtGui.QWidget, View):
    def __init__(self, renderable):
        super(DisplayModelQt,  self).__init__()
        self.widgetV = QtGui.QWidget()
        self.layoutV = QtGui.QVBoxLayout(self.widgetV)

        self.layoutH = QtGui.QHBoxLayout(self)
        self.renderable = renderable

        self.setGeometry(0,  0,  1000,  700)


    #Override View
    def setRunner(self, runner):
        self.runner = runner
        self.globalParams = GlobalParams(self.runner)
        self.rightPanel = ParametersView(self.runner)
        self.displayMaps = DisplayMapsQt(self.renderable,self.runner,self.rightPanel)
        self.layoutV.addWidget(self.displayMaps)
        self.layoutV.addWidget(self.globalParams)

        self.layoutH.addWidget(self.widgetV)
        self.layoutH.addWidget(self.rightPanel)

    #Override View
    @pyqtSlot()
    def update(self):
        self.displayMaps.update()
        self.repaint()


    #Override View
    @pyqtSlot(str)
    def updateParams(self,mapName):
        self.displayMaps.updateParams(mapName)



class DisplayMapsQt(QtGui.QWidget):
    """
        Temporary class for diplay
        TODO add parameter file

    """

    def __init__(self, renderable, runner,parametersView):
        super(DisplayMapsQt,  self).__init__()
        self.renderable = renderable
        self.parametersView = parametersView
        self.runner = runner
        size = len(self.renderable.getArrays())
        self.simuTime = 0

        self.listLabels= {}
        self.dictInfoMap = {}
        self.nbCols = int(math.ceil(math.sqrt(size))) #nb cols in the label matrix
        self.nbRows = int(math.ceil(size/float(self.nbCols))) #nb rows in the label matrix
        self.grid = QtGui.QGridLayout(self)

        #debug
        self.paintEventCount = 0
        self.mapUpdate = 0

        self.__initArrays()



    def __initArrays(self):
        """
            Add all arrays of renderable
        """
        maps = self.renderable.getArrays()
        for map in maps:
            self.addMap( map)

    def addMap(self,  map_):
        """
            Add a new map to the view
            return the index of the map
        """
        label = ArrayWidget(map_,self.runner,self.parametersView)
        self.listLabels.update({map_.getName():label})
        index = len(self.listLabels)-1
        row = index / self.nbCols
        col = index % self.nbCols
        self.grid.addWidget(label, row, col)
        label.setVisible(True)

    def __updateInfoMap(self, name, map_):
        infoMap = InfoMap(map_.shape, np.min(map_), np.max(map_))
        self.dictInfoMap.update({name:infoMap})


    def update(self):
        """
            The controller will send a update signal to say that a map changed
            The map ids to update will be stored in idsToUpdate
            The map itself will be in mapToUpdate in the same order
        """
        maps = self.renderable.getArrays()
        labels = self.listLabels.values()
        for map in maps:
            self.listLabels[map.getName()].updateArray(map)

        self.mapUpdate += 1

    def updateParams(self,mapName):
            label = self.listLabels[unicode(mapName)]
            label.onParamsChanged()
