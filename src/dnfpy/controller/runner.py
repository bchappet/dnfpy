from datetime import datetime
import numpy as np
import warnings
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
    def __init__(self,timeEnd=100,allowedTime=10e10,saveMapDict={}):
        super(Runner,self).__init__()
        self.mapDict = {} #dictionary with every map for fast access
        self.runnables = {} #dictinary of runnable to run

        self.saveMapDict = saveMapDict # time -> [],map -> []
        self.timeSave = 0

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


    def addRunnable(self,runnable,name):
            self.runnables[name] = runnable
            self.mapDict.update(runnable.getMapDict())

    def getRunnable(self,name):
        return self.runnables[name]

    def isPresent(self,name):
        """
        Return true if runnable name is present
        """
        return name in self.runnables.keys()

    def updateParam(self,mapName,name,value):
        map = self.mapDict[mapName]
        nameStr = name
        map.setParamsRec(**{nameStr:value})

    def onClick(self,mapName,x,y):
        mapName = str(mapName)
        for r in self.runnables.values():
            r.onClick(mapName,x,y)

    def onLClick(self,mapName,x,y):
        mapName = str(mapName)
        for r in self.runnables.values():
            r.onLClick(mapName,x,y)



    def onClose(self):
        return self.finalize()

    def finalize(self):
        ret = []
        for r in self.runnables.values():
            ret.extend( r.finalize())
        return ret

    def __getNameFolder(self):
        import datetime
        name = ""
        for r in self.runnables.values():
                name += r.getName()+"_"
        name_uuid = name+datetime.datetime.now().isoformat()
        return name_uuid

    def __createDir(self,name):
        if not os.path.exists(name):
            os.makedirs(name)


    def __getFolder(self):
        simutime = round(self.simuTime,5)
        timeStr  = str(simutime).replace(".","_")
        print(timeStr)
        folder = "save/" + self.saveFolder+ "/"
        self.__createDir(folder)
        return folder,timeStr


    def saveFig(self):
        import dnfpy.view.staticViewMatplotlib as mtpl
        import matplotlib.pyplot as plt
        lis = []
        folder,timeStr = self.__getFolder()
        for r in self.runnables.values():
                lis.extend(r.getArrays())

        for theMap in lis:
            fileName = folder+theMap.getName()+"_"+timeStr+".png"
            try:
                mtpl.plotArray(theMap.getData())
                print("Saving %s" % fileName)
                plt.savefig(fileName, dpi=300)
                plt.close()

            except Exception as e:
                print("could not plot: ",fileName)

       

    def saveArr(self):
        import numpy as np
        mapList = self.mapDict.values()
        self._saveArrList(mapList)

    def _saveArrName(self,nameList):
        mapList = [self.mapDict[name] for name in nameList]
        self._saveArrList(mapList)

    def _saveArrList(self,mapList):
        folder,timeStr = self.__getFolder()
        for theMap in mapList:
            print("saving... %s"%theMap.getName())
            try:
                if isinstance(theMap,Statistic):
                    fileName = folder+theMap.getName()+".csv"
                    trace = np.array(theMap.getTrace())
                    if len(trace) > 2 :
                        np.save(fileName,theMap.getTrace())
                    else:
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
            except Exception as e:
                print("failure ",e)

    def getNextUpdateTime(self):
            snut = [r.getNextUpdateTime() for r in self.runnables.values()]
            return min(snut)



    def step(self):
            if self.simuTime == 0:
                for r in self.runnables.values():
                    r.firstComputation()
            nextTime = self.getNextUpdateTime()
            self.lastSimuTime = self.simuTime
            self.simuTime = nextTime
            if  len(self.saveMapDict) > 0 and self.timeSave < len(self.saveMapDict['time']):
                if abs(self.simuTime - self.saveMapDict['time'][self.timeSave]) < 1e-8:
                    print(self.saveMapDict['name']=='*')
                    if self.saveMapDict['name'] == '*':
                        self.saveArr()
                    else:
                        self._saveArrName(self.saveMapDict['name'])
                    self.timeSave += 1

            for r in self.runnables.values():
                r.updateRunnable(self.simuTime)

    def resetSlot(self):
        self.startTime = timer.clock()
        self.lastUpdateTime = datetime.now()
        self.simuTime = 0.
        self.lastSimuTime = 0.
        self.timeSave = 0
        for r in self.runnables.values():
            r.resetRunnable()

        for r in self.runnables.values():
            r.applyContext()

    def resetParamsSlot(self):
        for r in self.runnables.values():
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

def constructRunner(model,scenario,stats,timeEnd,allowedTime=10e10,saveMapDict = {}):
    runner = Runner(timeEnd=timeEnd,allowedTime=allowedTime,saveMapDict=saveMapDict)
    runner.addRunnable(model,"model")
    if scenario:
        scenario.init(runner)
        runner.addRunnable(scenario,"scenario")
    if stats:
        stats.init(runner)
        runner.addRunnable(stats,"stats")
    return runner




def launch(model,scenario,stats,timeEnd,allowedTime=10e10,seed=None,save=False,saveMapDict={}):
    """

    """
    np.random.seed(seed)
    runner = constructRunner(model,scenario,stats,timeEnd,allowedTime,saveMapDict)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        ret= runner.run()
    if save:
        runner.saveArr()
    return ret
