#!/usr/bin/python
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
import math
import plotArrayQt



class DisplayMapsQt(QtGui.QWidget):
    """
        Temporary class for diplay
        TODO add parameter file

    """
    
    def __init__(self,size):
        super(DisplayMapsQt, self).__init__()
        self.initUI()
        self.listImg = [] #list of the displayed QImage
        self.listLabel = [] #list of labels

        #Store the change to do on next update signal
        self.idsToUpdate = []
        self.mapsToUpdate = []
        self.nbCols = int(math.ceil(math.sqrt(size))) #nb cols in the label matrix
        self.nbRows = int(math.ceil(size/float(self.nbCols))) #nb rows in the label matrix
        self.grid = QtGui.QGridLayout(self)

        #debug
        self.paintEventCount = 0
        self.mapUpdate = 0

    def __addLabel(self,label,title):
        index = len(self.listLabel)-1
        row = index / self.nbCols
        col = index % self.nbCols
        self.grid.addWidget(label,row,col)
        label.setVisible(True)
        return index

    def addMap(self,map):
        """
            Add a new map to the view
            return the index of the map
        """
        img =plotArrayQt.npToQImage(map)
        self.listImg.append(img)
        label = QtGui.QLabel(self)
        label.setScaledContents(True)
        self.listLabel.append(label)
        #Compute the position of the widget

        pixmap =QtGui.QPixmap(img)
        label.setPixmap(pixmap)
        
        return self.__addLabel(label,"Test")

    def addMapToUpdate(self,_id,_map):
        """
            Add one map to update : will change the state of map id
        """
        self.idsToUpdate.append(_id)
        self.mapsToUpdate.append(_map)

    def addMapsToUpdate(self,maps):
        """
            Add all the maps to update
            We assume that the maps indexes are 0 -> len(maps-1)
            maps must be a tuple 
        """
        for i in range(len(maps)):
            self.idsToUpdate.append(i)
        self.mapsToUpdate.extend(maps)

    @pyqtSlot()
    def update(self):
        """
            The model will send a update signal to say that a map changed
            The map ids to update will be stored in idsToUpdate
            The map itself will be in mapToUpdate in the same order
        """
        for id,map in zip(self.idsToUpdate,self.mapsToUpdate):
            self.updateGui(id,map)

        self.idsToUpdate = []
        self.mapsToUpdate = []
        self.mapUpdate += 1

    def paintEvent(self,event):
        self.paintEventCount +=1


    
    def updateGui(self,id,map):
        img = plotArrayQt.npToQImage(map)
        self.listImg[id] = img
        label  = self.listLabel[id]
        w = label.width()
        h = label.height()
        pixmap = QtGui.QPixmap.fromImage(img).scaled(w,h)
        label.setPixmap(pixmap)

    def resizeEvent(self, event):
        for label in self.listLabel:
            w = label.width()
            h = label.height()
            label.setPixmap(label.pixmap().scaled(w,h))

        
    def initUI(self):      
        self.setGeometry(300, 300,500, 500)
        self.setWindowTitle('Draw text')
