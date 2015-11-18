from multiprocessing import Process,Lock
import numpy as np
import time

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
            #constraints not met return -1
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




