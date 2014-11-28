from PyQt4 import QtCore
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
    trigger = QtCore.pyqtSignal()
    def __init__(self,model,view,timeEnd):
        super(Runner,self).__init__()
        self.model = model
        self.view = view
        self.simuTime = 0
        self.timeEnd = timeEnd
        self.timeRatio = 0.1#
        self.dt = 0.1 #time per computation (in sec)
        self.trigger.connect(self.view.update)
        #timing
        self.lastUpdateTime = datetime.now()

    @profile
    def run(self):
        while self.simuTime < self.timeEnd:
            nextTime = self.model.getSmallestNextUpdateTime()
            self.simuTime = nextTime
            self.model.update(self.simuTime)
            self.trigger.emit()
            self.__slowDown()
    def __slowDown(self):
        now = datetime.now()
        
        delta = now - self.lastUpdateTime
        
        timeIteration = self.timeRatio * self.dt * 1e6
        if delta.microseconds < timeIteration:
            val = self.timeRatio*1e6 - delta.microseconds
            time.sleep((timeIteration - delta.microseconds)/1e6)

            #print("to slow... delta ms %s and timeIteration %s"%(delta.microseconds,timeIteration))
        self.lastUpdateTime = now 
        

            

