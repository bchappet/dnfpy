from multiprocessing import Process,Lock
from multiprocessing import Queue
import numpy as np
import time

class WorkerManager:
    def __init__(self,nbThread,evaluationFunction,waitingTask,constraintsFunc,args):
        self.waitingTask = waitingTask
        self.constraintsFunc = constraintsFunc
        self.args = args
        self.evaluationFunction = evaluationFunction
            

        self.workerList = []
        for i in range(nbThread):
            self.workerList.append(self.initWorker(i))

        self.workerResultsQueue = Queue() #will store tuple: (particleId,fitness)
        self.inProcessPart = []

    def initWorker(self,i):
        return Worker(i,self.evaluationFunction,self.constraintsFunc,self.onWorkerResult,self.args)


    def runEvaluation(self,i,indiv):
        #request a worker for particle i. If no worker are available wait.
        #If a worker already works on i, return None, i will not be evaluated again
        worker = self.requestWorker(i)
        if worker:
            worker.evaluate(i,indiv)




    def requestWorker(self,i):
        """
        Give a worker for particle i. If no worker available wait using waiting task
        if a worker already work on i, return null
        """
        if i not in self.inProcessPart:
            while(not(self.workerResultsQueue.empty())):
                tup = self.workerResultsQueue.get()
                self.waitingTask(*tup)

            for i_worker in range(len(self.workerList)):
                worker = self.workerList[i_worker]
                if not(worker.is_alive()):
                    newWorker =  self.initWorker(i_worker)
                    self.workerList[i_worker] = newWorker
                    self.inProcessPart.append(i)
                    return newWorker

            #we treat the queue instead of sleeping
            else:
                time.sleep(0.01)
        else:
            return


        return self.requestWorker(i)

    def finishWork(self):
        """
        Finish the epoch synch all threads
        """
        for worker in self.workerList:
            if worker.is_alive():
                worker.join()
        while(not(self.workerResultsQueue.empty())):
            tup = self.workerResultsQueue.get()
            self.waitingTask(*tup)

    def onWorkerResult(self,i,newFitness):
        self.workerResultsQueue.put((i,newFitness))





class Worker(Process):
    def __init__(self,id,function,constrFunc,onResult,args):
        super(Worker,self).__init__()
        self.function = function
        self.constrFunc = constrFunc
        self.args = args
        self.onResult = onResult
        self.indiv = {}
        self.id = id
        self.i = None
        self.working = False
        self.lock = Lock()


    def evaluate(self,i,indiv):

        self.lock.acquire()
        self.indiv = indiv
        self.i = i
        self.working = True
        #print("worker %s start"%self.id)
        self.start()
        self.lock.release()

    def isWorking(self):
        self.lock.acquire()
        ret =  self.working
        self.lock.release()
        return ret;


    def run(self):
        time1 = time.time()
        #Check constraints
        if self.constrFunc(self.indiv,*self.args) > 0:
            #constraints not met return nan
            self.onResult(self.i,np.nan)
        else:
            result = self.function(self.indiv,*self.args)
            self.onResult(self.i,result)

        time2 = time.time()
        self.working = False
        #print("worker %s stop after %0.3f ms %s"%(self.id,(time2-time1)*1000.0,self.working))

class WorkerDNF(Worker):
    def __init__(self,function,onResult):
        super(WorkerDNF,self).__init__(function,onResult)




