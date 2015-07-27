from datetime import datetime
from dnfpy.stats.statistic import Statistic
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

    def onLClick(self,mapName,x,y):
        mapName = str(mapName)
        self.model.onLClick(mapName,x,y)



    def onClose(self):
        if self.scenario:
            return self.scenario.finalize(self.model,self)
        else:
            return None


    def saveFig(self):
        import dnfpy.view.staticViewMatplotlib as mtpl
        import matplotlib.pyplot as plt
        lis = self.model.getArrays()
        timeStr  = str(self.simuTime).replace(".","_")
        print timeStr
        for theMap in lis:
            fileName = "save/"+theMap.getName()+"_"+timeStr+".png"
            try:
                mtpl.plotArray(theMap.getData())
                print("Saving %s" % fileName)
                plt.savefig(fileName, dpi=300)
                plt.close()

            except:
                print("could not plot: %s" % fileName)

    def saveArr(self):
        import numpy as np
        lis = self.model.getArrays()
        timeStr  = str(self.simuTime).replace(".","_")
        for theMap in lis:
            if isinstance(theMap,Statistic):
                fileName = "save/"+theMap.getName()+".csv"
                np.savetxt(fileName,theMap.getTrace(),delimiter=",")
                print("Saving %s" % fileName)
            else:
                ndarray = theMap.getData()
                if isinstance(ndarray,np.ndarray):
                    dtype = ndarray.dtype
                    fileName = "save/"+theMap.getName()+"_"+timeStr
                    if dtype == np.ndarray:
                        import os
                        os.mkdir(fileName)
                        (height,width) = (theMap.getArg('size'),)*2
                        for row in range(height):
                             for col in range(width):
                                filename2 = fileName+"/"+str(row)+"_"+str(col)+".csv"
                                np.savetxt(filename2,ndarray[row,col],delimiter=",")
                                print("Saving %s" % filename2)
                    else:
                        try:
                            np.savetxt(fileName+".csv", ndarray, delimiter=",")
                            print("Saving %s" % fileName+".csv")
                        except Exception, e:
                            print("1 could not save: %s." % fileName)
                            print(e)
                else:
                    print("2 could not save: %s" % fileName)



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

def launch(model,scenario,timeEnd,allowedTime=10e10):
    if scenario:
        scenario.applyContext(model)

    runner = Runner(model,timeEnd=timeEnd,scenario=scenario,allowedTime=allowedTime)
    return runner.run()
