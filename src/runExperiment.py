import sys
import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import logging
from multiprocessing import Process, Lock

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

    if not parameterDict:
        parameterDict.update({"DEFAULT":999})

    if not iterationDict:
        iterationDict.update({"DEFAULT":[999]})

    return parameterDict,iterationDict

class BatchRunner(object):
    def __init__(self,savePrefix="exp",logfile="logExp.log"):

        self.lock = Lock()
        self.fileCSV = open(savePrefix+".csv",'w')
        logging.basicConfig(filename=logfile,level=logging.DEBUG)
        self.iteration = 0 #current iteration to display

    def finalize(self):
        self.fileCSV.close()


    def run(self,modelNameList,contextNameList,sceanrioNameList,nbRepetition=100,timeEnd=10,nbThread=3,
                  paramDictModel={"size":49,"nbStep":[2,3,4,0]},paramDictContext={},paramDictScenario={}):
                  #paramDictModel={"size":49,"sizeStream":[100,200,300,500,1000]},paramDictContext={},paramDictScenario={}):
        self.fileCSV.write("model,scenario,keymodel,valuemodel,keyscenario,valuescenario,it,ErrorDist,WellClusterized,NbIteration,ConvergenceTime\n")
        (parameterDictModel,iterationDictModel) = getDictionaryList(paramDictModel)
        (parameterDictScenario,iterationDictScenario) = getDictionaryList(paramDictScenario)
        logging.info("START nbRepetition: %s."%nbRepetition)
        logging.info("self.modelNameList: %s, self.contextNameList: %s, self.sceanrioNameList: %s"%(modelNameList,contextNameList,sceanrioNameList))
        logging.info("paramDictModel: %s, paramDictContext: %s, paramDictScenario: %s"%(paramDictModel,paramDictContext,paramDictScenario))
        logging.info("self.parameterDictModel: %s, self.iterationDictModel: %s"%(parameterDictModel,iterationDictModel))
        logging.info("self.parameterDictScenario: %s, self.iterationDictScenario: %s"%(parameterDictScenario,iterationDictScenario))


        nbIterationPerThread = [nbRepetition/nbThread]*nbThread
        mod = nbRepetition%nbThread
        for i in range(nbThread):
            if i < mod:
                nbIterationPerThread[i] += 1
        print("Nb Iteration per thread %s"%nbIterationPerThread)


        for self.modelName in modelNameList:
                modelClass = getClassFromName(self.modelName,"models")
                logging.info("modelClass : %s"%modelClass)
                for self.sceanrioName in sceanrioNameList:
                    scenarioClass = getClassFromName(self.sceanrioName,"scenarios")
                    logging.info("scenarioClass : %s"%scenarioClass)


                    for self.keyModel in iterationDictModel.keys():
                        valuesModel = iterationDictModel[self.keyModel]
                        for self.valueModel in valuesModel:
                                    paramsModel = {self.keyModel:self.valueModel}
                                    parameterDictModel.update(paramsModel)
                                    parameterDictModel.pop("DEFAULT",None)
                                    logging.info("loaded %s with %s"%(modelClass,parameterDictModel))

                                    for self.keyScenario in iterationDictScenario.keys():
                                        valuesScenario = iterationDictScenario[self.keyScenario]
                                        for self.valueScenario in valuesScenario:
                                            paramsScenario = {self.keyScenario:self.valueScenario}
                                            parameterDictScenario.update(paramsScenario)
                                            parameterDictScenario.pop("DEFAULT",None)
                                            logging.info("loaded %s with %s"%(scenarioClass,parameterDictScenario))
                                            print("model: %s,scenario: %s, self.keyModel: %s, value: %s, self.keyScenario: %s, value: %s"\
                                                %(self.modelName,self.sceanrioName,self.keyModel,self.valueModel,self.keyScenario,self.valueScenario))

                                            threadList = [] #list of threads
                                            for threadId in range(nbThread):
                                                try:
                                                    model = modelClass(**parameterDictModel)
                                                    scenario = scenarioClass(**parameterDictScenario)
                                                    th = MyThread(self,threadId,nbThread,nbIterationPerThread[threadId],model,scenario,timeEnd)
                                                    threadList.append(th)
                                                    th.start()
                                                except:
                                                    print("Error unable to start thread %s error %s"%(threadId,sys.exc_info()))
                                            for th in threadList:
                                                th.join()



    def printData(self,res,globalRepetition):
        self.lock.acquire();
        logging.info("res %s"%(res,))
        self.fileCSV.write(self.modelName+","+self.sceanrioName+",")
        self.fileCSV.write(self.keyModel +","+ str(self.valueModel)+",")
        self.fileCSV.write(self.keyScenario+","+str(self.valueScenario)+",")
        self.fileCSV.write(str(globalRepetition)+",")
        self.fileCSV.write(strToCsv(str(res)))
        self.fileCSV.write("\n")
        self.lock.release();

class MyThread (Process):
    def __init__(self,batchRunner,threadId,nbThreads,nbRepetition,model,scenario,timeEnd):
        Process.__init__(self)
        self.batchRunner= batchRunner
        self.threadId = threadId
        self.nbThreads = nbThreads
        self.nbRepetition = nbRepetition
        self.model = model
        self.scenario = scenario
        self.timeEnd = timeEnd

    def run(self):
        for i in range(self.nbRepetition):
            globalRepetition = i* self.nbThreads + self.threadId
            #logging.info("thread %s, thread repetition %s, global repetition %s"%(self.threadId,i,globalRepetition))
            print("thread %s, thread repetition %s, global repetition %s"%(self.threadId,i,globalRepetition))
            res = runner.launch(self.model,None,self.scenario,self.timeEnd)
            self.batchRunner.printData(res,globalRepetition)
            self.model.reset() #reset time
            self.model.resetParams() #reset params
            self.scenario.reset()


def strToCsv(string):
    resStr = str(string)
    resStr = resStr.replace("(","")
    resStr = resStr.replace(")","")
    resStr = resStr.replace("[","")
    resStr = resStr.replace("]","")
    resStr = resStr.replace("\'","")
    return resStr



if __name__ == "__main__":
    modelNameList = eval(sys.argv[1])
    contextNameList = eval(sys.argv[2])
    sceanrioNameList = eval(sys.argv[3])
    nbRepetition = eval(sys.argv[4])
    timeEnd = eval(sys.argv[5])
    savePrefix = sys.argv[6]
    logfile = sys.argv[7]
    nbThread = eval(sys.argv[8])


    batchRunner = BatchRunner(savePrefix=savePrefix,logfile=logfile)
    batchRunner.run(modelNameList=modelNameList,contextNameList=contextNameList,
                  sceanrioNameList=sceanrioNameList,nbRepetition=nbRepetition,
                  timeEnd=timeEnd,nbThread=nbThread)
    batchRunner.finalize()





