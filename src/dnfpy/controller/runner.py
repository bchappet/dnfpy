from datetime import datetime
from dnfpy.stats.statistic import Statistic
import time as timer
import os

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


        self.saveFolder = self.__getNameFolder()


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

    def __getNameFolder(self):
        import datetime
        name_uuid = str(self.model)+"_"+str(self.scenario)+"_"+datetime.datetime.now().isoformat()
        return name_uuid

    def __createDir(self,name):
        if not os.path.exists(name):
            os.makedirs(name)


    def saveFig(self):
        import dnfpy.view.staticViewMatplotlib as mtpl
        import matplotlib.pyplot as plt
        lis = self.model.getArrays()
        timeStr  = str(self.simuTime).replace(".","_")
        print timeStr
        folder = "save/" + self.saveFolder+ "/"
        self.__createDir(folder)
        for theMap in lis:
            fileName = folder+theMap.getName()+"_"+timeStr+".png"
            try:
                mtpl.plotArray(theMap.getData())
                print("Saving %s" % fileName)
                plt.savefig(fileName, dpi=300)
                plt.close()

            except:
                print("could not plot: %s" % fileName)

    def saveArr(self):
        import numpy as np
        mapList = self.model.getMapDict().values()
        timeStr  = str(self.simuTime).replace(".","_")
        print timeStr
        folder = "save/" + self.saveFolder+ "/"
        self.__createDir(folder)

        for theMap in mapList:
            print("saving... %s"%theMap.getName())
            if isinstance(theMap,Statistic):
                fileName = folder+theMap.getName()+".csv"
                np.savetxt(fileName,theMap.getTrace(),delimiter=",")
                print("Saving %s" % fileName)
            else:
                data = theMap.getData()
                fileName = folder+theMap.getName()+"_"+timeStr
                if isinstance(data,np.ndarray):
                    dtype = data.dtype
                    if dtype == np.ndarray:
                        os.mkdir(fileName)
                        (height,width) = (theMap.getArg('size'),)*2
                        for row in range(height):
                             for col in range(width):
                                filename2 = fileName+"/"+str(row)+"_"+str(col)+".csv"
                                np.savetxt(filename2,data[row,col],delimiter=",")
                                print("Saving %s" % filename2)
                    else:
                        np.savetxt(fileName+".csv", data, delimiter=",")
                        print("Saving %s" % fileName+".csv")
                elif isinstance(data,float) or isinstance(data,int) or isinstance(data,bool):
                    np.savetxt(fileName+".csv", np.array([data]), delimiter=",")
                    print("Saving %s" % fileName+".csv")
                else:
                    print("could not save: %s" % theMap.getName())



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
        if self.scenario:
            self.scenario.applyContext(self.model)

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
    model.reset()
    if scenario:
        scenario.applyContext(model)

    runner = Runner(model,timeEnd=timeEnd,scenario=scenario,allowedTime=allowedTime)
    return runner.run()
