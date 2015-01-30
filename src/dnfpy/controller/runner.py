from datetime import datetime
import time as timer

class Runner(object):
    """
        The runner is the controller of the model and the view
        See MVC pattern
        The runner update view and model

        Attribute:
            model : Model
    """
    def __init__(self,model,timeEnd=100,scenario=None,allowedTime=10e10):
        super(Runner,self).__init__()
        self.nbIt = 0
        self.startTime = timer.clock()
        self.allowedTime =  allowedTime
        self.model = model
        self.simuTime = 0.
        self.timeEnd = timeEnd
        #timing
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.
        #scenario
        self.scenario=scenario


    def onClick(self,mapName,x,y):
        mapName = str(mapName)
        self.model.onClick(mapName,x,y)

    def onClose(self):
        if self.scenario:
            return self.scenario.finalize(self.model,self)
        else:
            return None


    def saveFigSlot(self):
            import  dnfpy.view.staticViewMatplotlib as mtpl
            import matplotlib.pyplot as plt
            dic = self.model.getArraysDict()
            for key in dic:
                mtpl.plotArray(dic[key])
                plt.savefig(key+".png",dpi=300)
                plt.close()

    def saveArrSlot(self):
            import numpy as np
            dic = self.model.getArraysDict()
            for key in dic:
                np.savetxt(key+".csv",dic[key],delimiter = ",")

    def step(self):
            if self.simuTime == 0:
                self.model.firstComputation()
            nextTime = self.model.getSmallestNextUpdateTime()
            self.lastSimuTime = self.simuTime
            self.simuTime = nextTime
            if self.scenario:
                self.scenario.apply(self.model,self.simuTime,self)
            self.model.update(self.simuTime)

    def resetSlot(self):
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.
        self.model.reset()

    def resetParamsSlot(self):
        self.model.resetParams()



    def run(self):
        while self.simuTime < self.timeEnd:
            self.nbIt += 1
            if timer.clock() - self.startTime > self.allowedTime:
                ret = self.onClose()
                return ret

            self.step()
        ret = self.onClose()
        return ret

def launch(model,context,scenario,timeEnd,allowedTime=10e10):
    if context:
        context.apply(model)
    if scenario:
        scenario.applyContext(model)

    runner = Runner(model,timeEnd=timeEnd,scenario=scenario,allowedTime=allowedTime)
    return runner.run()
