from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import pyqtSlot
import math
import plotArrayQt
from dnfpy.view.renderable import Renderable
import numpy as np
from dnfpy.view.view import View

class ArrayLabel(QtGui.QLabel):
        def __init__(self,name,array):
                super(ArrayLabel,self).__init__()
                self.name = name
                self.updateArray(array)
                
        def updateArray(self,array):
                self.array = array
                self.img = plotArrayQt.npToQImage(array)
                self.shape = array.shape
                self.min = np.min(array)
                self.max = np.max(array)
        def paintEvent(self,event):
                qp = QtGui.QPainter(self)
                qp.drawImage(event.rect(),self.img)
                qp.drawText(event.rect(), QtCore.Qt.AlignTop, "%.2f"%self.max)   
                qp.drawText(event.rect(), QtCore.Qt.AlignBottom, "%.2f"%self.min)   
        def mousePressEvent(self, event):
                labXY = np.array([event.x(),event.y()],dtype=np.float32)
                size = self.rect().size()
                labWH = np.array([size.width(),size.height()]) - 1
                shapeWH = np.array([self.array.shape[0],self.array.shape[1]]) -1
                arrXY = (labXY / labWH) * shapeWH
                arrXY = np.round(arrXY)
                value = self.array[arrXY[1],arrXY[0]]
                print value
                
        def __labelToArrayCoord(self,):
                """Return the corresponding array coords"""
                arrW = self.shape[0]
                arrH = self.shape[1]
                x = labX/float(w) * arrW 
                y = labY/float(h) * arrH 
                return (x,y)
                    




class GlobalParams(QtGui.QWidget):
        """
            Global parameter of the runner
        """
        def __init__(self,runner):
            super(GlobalParams,self).__init__()
            
            self.runner = runner
            layout = QtGui.QHBoxLayout(self)
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
            layout.addWidget(bPlay)
            layout.addWidget(bStep)
            layout.addWidget(spinSpeedRatio)

            
class DisplayModelQt(QtGui.QWidget,View):
    triggerParamsUpdate = QtCore.pyqtSignal()#Will be triggered on parmas modification
    def __init__(self,renderable):
        super(DisplayModelQt, self).__init__()
        self.__paramDict = {} #copy of the global parameter dict
        self.layout = QtGui.QVBoxLayout(self)
        self.displayMaps = DisplayMapsQt(renderable)
        self.layout.addWidget(self.displayMaps)

        self.setGeometry(400, 0, 700, 700)
    #Override View
    def getParamsDict(self):
        return self.__paramDict
    #Override View
    def updateParamsDict(self,paramsDict):
        self.__paramDict.update(paramsDict)
    #Override View
    def setRunner(self,runner):
        self.runner = runner
        self.globalParams = GlobalParams(self.runner)
        self.triggerParamsUpdate.connect(runner.updateParams)
        self.layout.addWidget(self.globalParams)

    #Override View
    @pyqtSlot()
    def update(self):
        self.displayMaps.update()
        self.repaint()
        



        



class DisplayMapsQt(QtGui.QWidget):
    """
        Temporary class for diplay
        TODO add parameter file

    """
    
    def __init__(self,renderable):
        super(DisplayMapsQt, self).__init__()
        self.renderable = renderable
        size = len(self.renderable.getArraysDict())
        self.simuTime = 0

        self.dictLabel = {} #dict of labels
        self.nbCols = int(math.ceil(math.sqrt(size))) #nb cols in the label matrix
        self.nbRows = int(math.ceil(size/float(self.nbCols))) #nb rows in the label matrix
        self.grid = QtGui.QGridLayout(self)

        #debug
        self.paintEventCount = 0
        self.mapUpdate = 0

        self.__initArrays()
        

    def __addLabel(self,label,title):
        index = len(self.dictLabel)-1
        row = index / self.nbCols
        col = index % self.nbCols
        box = QtGui.QGroupBox(title)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)
        box.setLayout(vbox)
        box.focusInEvent
        self.grid.addWidget(box,row,col)
        label.setVisible(True)

    def __initArrays(self):
        """
            Add all arrays of renderable
        """
        maps = self.renderable.getArraysDict()
        for name in maps.keys():
            self.addMap(name,maps[name])

    def addMap(self,name,array):
        """
            Add a new map to the view
            return the index of the map
        """
        label = ArrayLabel(name,array)
        label.setScaledContents(True)
        self.dictLabel.update({name:label})
        self.__addLabel(label,name)

    def __updateInfoMap(self,name,map_):
        infoMap = InfoMap(map_.shape,np.min(map_),np.max(map_))
        self.dictInfoMap.update({name:infoMap})


    def update(self):
        """
            The controller will send a update signal to say that a map changed
            The map ids to update will be stored in idsToUpdate
            The map itself will be in mapToUpdate in the same order
        """
        maps = self.renderable.getArraysDict()
        for name in maps.keys():
            self.dictLabel[name].updateArray(maps[name])

        self.mapUpdate += 1



        
