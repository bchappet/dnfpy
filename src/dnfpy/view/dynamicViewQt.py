#!/usr/bin/python
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
import math
import plotArrayQt
from dnfpy.view.renderable import Renderable



class DisplayMapsQt(QtGui.QWidget):
    """
        Temporary class for diplay
        TODO add parameter file

    """
    
    def __init__(self,renderable):
        super(DisplayMapsQt, self).__init__()
        self.renderable = renderable
        size = len(self.renderable.getArraysDict())

        self.__initUI()
        self.dictImg = {} #dict  of {name : QImage}
        self.dictLabel = {} #list of labels

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
        self.grid.addWidget(label,row,col)
        label.setVisible(True)
        return index

    def __initArrays(self):
        """
            Add all arrays of renderable
        """
        maps = self.renderable.getArraysDict()
        for name in maps.keys():
            self.addMap(name,maps[name])


    def addMap(self,name,map_):
        """
            Add a new map to the view
            return the index of the map
        """
        img =plotArrayQt.npToQImage(map_)
        self.dictImg.update({name:img})
        label = QtGui.QLabel(self)
        label.setScaledContents(True)
        self.dictLabel.update({name:label})
        #Compute the position of the widget

        pixmap =QtGui.QPixmap(img)
        label.setPixmap(pixmap)
        
        return self.__addLabel(label,name)

    @pyqtSlot()
    def update(self):
        """
            The controller will send a update signal to say that a map changed
            The map ids to update will be stored in idsToUpdate
            The map itself will be in mapToUpdate in the same order
        """
        maps = self.renderable.getArraysDict()
        for name in maps.keys():
            self.updateGui(name,maps[name])

        self.mapUpdate += 1

    def paintEvent(self,event):
        self.paintEventCount +=1


    
    def updateGui(self,name,map_):
        img = plotArrayQt.npToQImage(map_)
        self.dictImg[name] = img
        label  = self.dictLabel[name]
        w = label.width()
        h = label.height()
        pixmap = QtGui.QPixmap.fromImage(img).scaled(w,h)
        label.setPixmap(pixmap)

    def resizeEvent(self, event):
        for label in self.dictLabel.values():
            w = label.width()
            h = label.height()
            label.setPixmap(label.pixmap().scaled(w,h))

        
    def __initUI(self):      
        self.setGeometry(300, 300,500, 500)
        self.setWindowTitle('DNFPy')
