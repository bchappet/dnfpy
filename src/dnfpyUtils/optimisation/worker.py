from multiprocessing import Process,Lock
import time

class Worker(Process):
    def __init__(self,id,function,onResult):
        super(Worker,self).__init__()
        self.function = function
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
        result = self.function(self.indiv)
        self.onResult(self.i,result)
        time2 = time.time()
        self.working = False
        #print("worker %s stop after %0.3f ms %s"%(self.id,(time2-time1)*1000.0,self.working))

class WorkerDNF(Worker):
    def __init__(self,function,onResult):
        super(WorkerDNF,self).__init__(function,onResult)




