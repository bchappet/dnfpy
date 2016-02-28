import sys
import operator
import itertools
import math
import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import logging
from multiprocessing import Process, Lock, Queue
import begin #very usefull arg parsing library

"""
Arguments:
    [ModelNames]: list string
    [Contexts]: list string
    [Scenarios] : list string
    nbRepitition : int
    savePrefix : string
    logfile : string
    size : int

    will save one file for a set of reepetition with:
    repetition#, Charac1, Charac2,...

    The charac list names is gotten from the scenario using:
    getCharacNameList()


"""


def getParameteterProductList(modelNameList,scenarioNameList,iterationDictModel,iterationDictScenario,iterationDictGlobal):
    """
    return a list of dictionary
    each dictionary contains the right parameter for the iteration
    """
    ret = [] #returned list
    productList = [modelNameList,scenarioNameList]
    keyList = ["ModelName","ScenarioName"]
    for key in iterationDictModel:
        keyList.append(key)
        productList.append(iterationDictModel[key])
    for key in iterationDictScenario:
        keyList.append(key)
        productList.append(iterationDictScenario[key])
    for key in iterationDictGlobal:
        keyList.append(key)
        productList.append(iterationDictGlobal[key])

    for it in itertools.product(*productList):
        ret.append(dict(zip(keyList,it)))

    return ret


def getDictionaryList(le_dict):
    """
    Take a dictionary {key:val and key:list} and split it in two dictionary
    parameter dict the parameter used for every iterations
    itarationDict the dict{key:list} over which we have to iterate
    """
    parameterDict = dict()#the parameter used for every iterations
    iterationDict = dict()#the dict{key:list} over which we have to iterate

    for key in le_dict.keys():
        if isinstance(le_dict[key],list):
            iterationDict.update({key:le_dict[key]})
        else:
            parameterDict.update({key:le_dict[key]})
    return parameterDict,iterationDict

class BatchRunner(object):
    def __init__(self,savePrefix="exp",logfile="logExp.log"):

        self.fileName = savePrefix+".csv"
        try:
            os.remove(self.fileName)
        except:
            pass
        logging.basicConfig(filename=logfile,level=logging.DEBUG)
        self.iteration = 0 #current iteration to display
        self.fileCSV = open(self.fileName,'a')
        self.q = Queue()


    def finalize(self):
        self.fileCSV.close()
        print("Saving in %s"%self.fileName)


    def run(self,modelNameList,statNameList,scenarioNameList,nbRepetition=100,timeEnd=10,nbThread=3,\
            paramDictModel={},paramDictScenario={},paramDictStat={},paramDictGlobal={}):

        (parameterDictModel,iterationDictModel) = getDictionaryList(paramDictModel)
        (parameterDictScenario,iterationDictScenario) = getDictionaryList(paramDictScenario)
        (parameterDictGlobal,iterationDictGlobal) = getDictionaryList(paramDictGlobal)
        parameterDictModel.update(parameterDictGlobal)
        parameterDictScenario.update(parameterDictGlobal)
        #update 17/02/16 we consider the case were there are severa list in one dictionary#########
        self.header = ['ModelName','ScenarioName'] #header of the csv
        #we add as many key as there are in parameterDictModel
        for key in iterationDictModel:
            self.header.append(key)
        #same for scenario
        for key in iterationDictScenario:
            self.header.append(key)
        #and global
        for key in iterationDictGlobal:
            self.header.append(key)
        self.header.extend(['it','ErrorDist']) #TODO get the result form the Stats
        self.fileCSV.write(",".join(self.header)+'\n')

        logging.info("headerCSV")
        logging.info(",".join(self.header))
        ##########################################################################################
        logging.info("START nbRepetition: %s."%nbRepetition)
        logging.info("self.modelNameList: %s, self.statNameList: %s, self.scenarioNameList: %s"%(modelNameList,statNameList,scenarioNameList))
        logging.info("paramDictModel: %s, paramDictStat: %s, paramDictScenario: %s"%(paramDictModel,paramDictStat,paramDictScenario))
        logging.info("self.parameterDictModel: %s, self.iterationDictModel: %s"%(parameterDictModel,iterationDictModel))
        logging.info("self.parameterDictScenario: %s, self.iterationDictScenario: %s"%(parameterDictScenario,iterationDictScenario))


        nbIterationPerThread = [nbRepetition//nbThread]*nbThread
        mod = nbRepetition%nbThread
        for i in range(nbThread):
            if i < mod:
                nbIterationPerThread[i] += 1
        print("Nb Iteration per thread %s"%nbIterationPerThread)


        parametersProductDict = getParameteterProductList(modelNameList,scenarioNameList,iterationDictModel,iterationDictScenario,iterationDictGlobal)

        #For now one stat and no list in kwstat TODO
        statClass = getClassFromName(statNameList[0],"stats")
        parameterDictStat = paramDictStat
        for self.productDict in parametersProductDict:
            print(self.productDict)
            self.modelName = self.productDict["ModelName"]
            self.scenarioName = self.productDict["ScenarioName"]
            modelClass = getClassFromName(self.modelName,"models")
            scenarioClass = getClassFromName(self.scenarioName,"scenarios")
            dictModel = {k:self.productDict[k] for k in iterationDictModel}
            parameterDictModel.update(dictModel)
            dictScenario = {k:self.productDict[k] for k in iterationDictScenario}
            parameterDictScenario.update(dictScenario)
            dictGlobal = {k:self.productDict[k] for k in iterationDictGlobal}
            parameterDictModel.update(dictGlobal)
            parameterDictScenario.update(dictGlobal)
            parameterDictStat.update(parameterDictGlobal)

            threadList = [] #list of threads
            for threadId in range(nbThread):
                model = modelClass(**parameterDictModel)
                scenario = scenarioClass(**parameterDictScenario)
                stat = statClass(**parameterDictStat)
                th = MyThread(self,threadId,nbThread,nbIterationPerThread[threadId],model,scenario,stat,timeEnd,self.q)
                threadList.append(th)
                #try:
                th.start()
                #except:
                #    print("Error unable to start thread %s error %s"%(threadId,sys.exc_info()))
            for th in threadList:
                th.join()

            print("Writing results...")#process of the iteration of this product is done
            for i in range(self.q.qsize()):
                self.fileCSV.write(self.q.get())
                self.fileCSV.flush()




    def printData(self,res,globalRepetition):
#        logging.info("res %s"%(res,))

        resultString = ""
        for key in self.header[0:-2]:
            resultString += str(self.productDict[key]) + ","
        resultString += str(globalRepetition)+","+ strToCsv(str(res))+"\n"
        logging.info(str(res))
        print(str(res))
        return resultString

class MyThread (Process):
    def __init__(self,batchRunner,threadId,nbThreads,nbRepetition,model,scenario,stat,timeEnd,q):
        Process.__init__(self)
        self.batchRunner= batchRunner
        self.q = q
        self.threadId = threadId
        self.nbThreads = nbThreads
        self.nbRepetition = nbRepetition
        self.runner = runner.constructRunner(model,scenario,stat,timeEnd)


    def run(self):
        for i in range(self.nbRepetition):
            globalRepetition = i* self.nbThreads + self.threadId
            #logging.info("thread %s, thread repetition %s, global repetition %s"%(self.threadId,i,globalRepetition))
            print("thread %s, thread repetition %s, global repetition %s"%(self.threadId,i,globalRepetition))
            res = self.runner.run()
            resultString = self.batchRunner.printData(res,globalRepetition)
            self.q.put(resultString)




def strToCsv(string):
    resStr = str(string)
    resStr = resStr.replace("(","")
    resStr = resStr.replace(")","")
    resStr = resStr.replace("[","")
    resStr = resStr.replace("]","")
    resStr = resStr.replace("\'","")
    return resStr



@begin.start
def main(models = "['ModelDNF1D',]",size="49",dim="2",stats="['StatsTracking1',]",scenarios="['ScenarioTracking',]",params="{}",timeEnd="30",lat="dog",fashion='chappet',dt='0.1',nbRepet='50',prefix='model_scenario_repet',log='default.log',nbThread='8',kwmodel="{}",kwscenario="{}",kwstat="{}"):
    """
    --scenario "['ScenarioTracking','ScenarioNoise']" to give several scenario to iterate on
    --kwmodel "{'activation':[step,sigm],}"
    """
    #lock = Lock()
    toPrint = []

    modelNameList = eval(models)
    statNameList = eval(stats)
    scenarioNameList = eval(scenarios)
    nbRepetition = int(eval(nbRepet))
    timeEnd = eval(timeEnd)
    savePrefix = prefix
    logfile = log
    nbThread = eval(nbThread)

    dt = eval(dt)
    dim = eval(dim)
    size = eval(size)
    size = int(((math.floor(size/2.)) * 2) + 1)#Ensure size is odd for convolution
    

    kwparams = dict(size=size,dim=dim,lateral=lat,fashion=fashion,dt=dt)
    paramDictModel = eval(kwmodel)
    paramDictScenario = eval(kwscenario)
    paramDictStat = eval(kwstat)

   # paramDictModel.update(kwparams)
   # paramDictScenario.update(kwparams)
   # paramDictStat.update(kwparams)


    batchRunner = BatchRunner(savePrefix=savePrefix,logfile=logfile)
    batchRunner.run(modelNameList=modelNameList,statNameList=statNameList,
                  scenarioNameList=scenarioNameList,nbRepetition=nbRepetition,
                  timeEnd=timeEnd,nbThread=nbThread,paramDictModel=paramDictModel,
                  paramDictScenario=paramDictScenario,paramDictStat=paramDictStat,
                  paramDictGlobal=kwparams)
    batchRunner.finalize()
#python3 runExperiment2.py --models "['ModelNSpike',]" --kwmodel "{'model':['spike','cnft'],'nspike':[1,2,3,5,10]}" --scenarios "['ScenarioTracking','ScenarioNoise',]"
