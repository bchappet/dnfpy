from datetime import datetime
from dnfpyUtils.stats.statistic import Statistic
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
    def __init__(self,timeEnd=100,allowedTime=10e10):
        super(Runner,self).__init__()
        self.mapDict = {} #dictionary with every map for fast access
        self.runnables = [] #list of runnable to run

        self.nbIt = 0
        self.startTime = timer.clock()
        self.allowedTime =  allowedTime
        self.simuTime = 0.
        self.timeEnd = timeEnd
        #timing
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.


        self.saveFolder = self.__getNameFolder()

    def getMap(self,mapName):
            return self.mapDict[mapName]


    def addRunnable(self,runnable):
            self.runnables.append(runnable)
            self.mapDict.update(runnable.getMapDict())

    def updateParam(self,mapName,name,value):
        map = self.mapDict[mapName]
        nameStr = name
        map.setParamsRec(**{nameStr:value})

    def onClick(self,mapName,x,y):
        mapName = str(mapName)
        for r in self.runnables:
            r.onClick(mapName,x,y)

    def onLClick(self,mapName,x,y):
        mapName = str(mapName)
        for r in self.runnables:
            r.onLClick(mapName,x,y)



    def onClose(self):
        ret = []
        for r in self.runnables:
            ret.extend( r.finalize())
        return ret

    def __getNameFolder(self):
        import datetime
        name = ""
        for r in self.runnables:
                name += r.getName()+"_"
        name_uuid = name+datetime.datetime.now().isoformat()
        return name_uuid

    def __createDir(self,name):
        if not os.path.exists(name):
            os.makedirs(name)


    def saveFig(self):
        import dnfpy.view.staticViewMatplotlib as mtpl
        import matplotlib.pyplot as plt
        lis = []
        for r in self.runnables:
                lis.extend(r.getArrays())

        timeStr  = str(self.simuTime).replace(".","_")
        print(timeStr)
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
        mapList = self.mapDict.values()
        timeStr  = str(self.simuTime).replace(".","_")
        print(timeStr)
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

    def getNextUpdateTime(self):
            snut = [r.getNextUpdateTime() for r in self.runnables]
            return min(snut)



    def step(self):
            if self.simuTime == 0:
                for r in self.runnables:
                    r.firstComputation()
            nextTime = self.getNextUpdateTime()
            self.lastSimuTime = self.simuTime
            self.simuTime = nextTime
            for r in self.runnables:
                r.updateRunnable(self.simuTime)

    def resetSlot(self):
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.
        for r in self.runnables:
            r.resetRunnable()

        for r in self.runnables:
            r.applyContext()

    def resetParamsSlot(self):
        for r in self.runnables:
            r.resetParamsRunnable()




    def run(self):
        self.resetSlot()
        while self.simuTime < self.timeEnd:
            self.nbIt += 1
            if timer.clock() - self.startTime > self.allowedTime:
                ret = self.onClose()
                return ret

            self.step()
        ret = self.onClose()
        return ret

def launch(model,scenario,stats,timeEnd,allowedTime=10e10):
    """

    """
    runner = Runner(timeEnd=timeEnd,allowedTime=allowedTime)
    runner.addRunnable(model)
    if scenario:
        runner.addRunnable(scenario)
        scenario.init(runner)
    if stats:
        runner.addRunnable(stats)
        stats.init(runner)

    return runner.run()
