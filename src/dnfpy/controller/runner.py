from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from datetime import datetime
import time

class Runner(QtCore.QThread):
    """
        The runner is the controller of the model and the view
        See MVC pattern
        The runner update view and model
        The view reads the model


        Attribute:
            model : Model
            view : View
    """
    triggerUpdate = QtCore.pyqtSignal()
    triggerParamsUpdate = QtCore.pyqtSignal(str)
    def __init__(self,model,view,timeEnd,paramsModelDict,timeRatio = 0.3):
        super(Runner,self).__init__()
        self.model = model
        self.paramsModelDict = paramsModelDict
        self.view = view
        self.simuTime = 0.
        self.timeEnd = timeEnd
        self.timeRatio = timeRatio
        self.triggerUpdate.connect(self.view.update)
        self.triggerParamsUpdate.connect(self.view.updateParams)
        #timing
        self.lastUpdateTime = datetime.now()
        #Control
        self.play = True

    def getTimeRatio(self):
        return self.timeRatio

    @pyqtSlot(str,str,int)
    def onParamIntChange(self,mapName,name,value):
        self.model.updateParam(mapName,name,value)

    @pyqtSlot(str,str,float)
    def onParamFloatChange(self,mapName,name,value):
        self.model.updateParam(mapName,name,value)
    @pyqtSlot(str)
    def onSpinIntValueChange(self,val):
        name = self.sender().prefix()[:-2]
        self.trigInt.emit(self.map.getName(),name,val)

    @pyqtSlot(str,str,str)
    def onParamStrChange(self,mapName,name,value):
        print("On param in t change in \"%s\" :  %s = %s "%(mapName,name,value))
        self.model.updateParam(mapName,name,value)

    @pyqtSlot(str,int,int)
    def onClick(self,mapName,x,y):
        mapName = str(mapName)
        mapToUpdate = self.model.onClick(mapName,x,y)
        if mapToUpdate:
            self.triggerParamsUpdate.emit(mapToUpdate)


    @pyqtSlot()
    def saveFigSlot(self):
            import  dnfpy.view.staticViewMatplotlib as mtpl
            import matplotlib.pyplot as plt
            dic = self.model.getArraysDict()
            for key in dic:
                mtpl.plotArray(dic[key])
                plt.savefig(key+".png",dpi=300)
                plt.close()
    @pyqtSlot()
    def saveArrSlot(self):
            import numpy as np
            dic = self.model.getArraysDict()
            for key in dic:
                np.savetxt(key+".csv",dic[key],delimiter = ",")

    @pyqtSlot(float)
    def setTimeRatio(self,timeRatio):
        self.timeRatio = timeRatio
    @pyqtSlot()
    def playSlot(self):
        self.play = not(self.play)


    @pyqtSlot()
    def stepSlot(self):
            self.__step()
    def __step(self):
            nextTime = self.model.getSmallestNextUpdateTime()
            self.simuTime = nextTime
            self.model.update(self.simuTime)
            self.triggerUpdate.emit()
    def run(self):
        while self.simuTime < self.timeEnd:
            while not(self.play):
                time.sleep(0.1)
            self.__step()
            self.__slowDown()
    def __slowDown(self):
        """
            Slow down computation to ensure that
            simuTime = timeRatio * realTime
        """
        now = datetime.now()

        delta = now - self.lastUpdateTime
        dt = self.paramsModelDict['dt']
        timeIteration = self.timeRatio * dt * 1e6
        if delta.microseconds < timeIteration:
            val = self.timeRatio*1e6 - delta.microseconds
            time.sleep((timeIteration - delta.microseconds)/1e6)
        self.lastUpdateTime = now




