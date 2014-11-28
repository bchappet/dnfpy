#!/usr/bin/python
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import pyqtSlot
import math
import plotArrayQt
from dnfpy.view.renderable import Renderable
import numpy as np

class ArrayLabel(QtGui.QLabel):
        def __init__(self,array):
                super(ArrayLabel,self).__init__()
                self.updateArray(array)
        def updateArray(self,array):
                self.img = plotArrayQt.npToQImage(array)
                self.shape = array.shape
                self.min = np.min(array)
                self.max = np.max(array)
                w = self.width()
                h = self.height()
                #pixmap = QtGui.QPixmap.fromImage(self.img).scaled(w,h)
                #self.setPixmap(pixmap)
        def paintEvent(self,event):
                qp = QtGui.QPainter(self)
                qp.drawImage(event.rect(),self.img)
                qp.drawText(event.rect(), QtCore.Qt.AlignTop, "%.2f"%self.max)   
                qp.drawText(event.rect(), QtCore.Qt.AlignBottom, "%.2f"%self.min)   




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

        self.__initUI()
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

    def addMap(self,name,map):
        """
            Add a new map to the view
            return the index of the map
        """
        label = ArrayLabel(map)
        label.setScaledContents(True)
        self.dictLabel.update({name:label})
        self.__addLabel(label,name)

    def __updateInfoMap(self,name,map_):
        infoMap = InfoMap(map_.shape,np.min(map_),np.max(map_))
        self.dictInfoMap.update({name:infoMap})


            



    @pyqtSlot()
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
        self.repaint()



        
    def __initUI(self):      
        self.setGeometry(300, 300,500, 500)
        self.setWindowTitle('DNFPy')
