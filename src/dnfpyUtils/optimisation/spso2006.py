import matplotlib.pyplot as plt
from dnfpyUtils.optimisation.worker import Worker,WorkerManager
import numpy as np
def rosen(indiv,*args):
        x = indiv['x']
        y = indiv['y']
        #time.sleep(0.0)

        return x**2 + (1-y)**2 +(2-indiv["z"])**2 + \
                    (5-indiv["a"])**2 + (10 - indiv["b"])**2
        #rosenbrock function
        #return (1 - x)**2 + 100*(y - x**2)**2
def eggHolder(indiv,*arg):
    """
    minimum is -959.6407
    """
    x = indiv['x']
    y = indiv['y']
    return -(y +47) * np.sin(np.sqrt(np.abs(y + x/2 + 47))) - x*np.sin(np.sqrt(np.abs(x-(y+47))))

def constrains(indiv,*args):
    """
    return 1 if outside valid args space
    """
    return 0;

def transformIndiv(indiv):
    return indiv

bounds = (np.array([-512,-512,-20,-20,-20]), np.array([512,512,20,20,20]))

class Spso:
    def __init__(self,n,k=3,w=0.721,c=1.193,acceptableFitness = 1e-6,nbEvaluationMax=100,wl=1,wg=0,nbThread=8,constraintsFunc = constrains,args=(),evaluationFunc=rosen,verbose=0,
            constantParamsDict={},evaluationParamsDict={},transformIndiv=transformIndiv,listParam=["x","y","z","a","b"],bounds = bounds):
        """
        n : nb particle
        k : mean of number of neighbors
        w : inertia
        c : influence of neigbors best and self best
        acceptableFitness : when to stop
        nbEvaluationMax : when to stop
        wl : influence of neigh best
        wg : influence of global best
        nbThread : nb thread for paralelisation
        """
        self.c = c
        self.w = w
        self.n = n
        self.k = k
        self.wl = wl#local weight
        self.wg = wg#global weight

        self.acceptableFitness = acceptableFitness
        self.nbEvaluationMax = nbEvaluationMax
        self.bestF = np.nan
        self.lastBestF = np.nan

        self.verbose = verbose
        self.transformIndiv = transformIndiv
        self.listParam = listParam
        self.bounds = bounds

        self.constantParamsDict = constantParamsDict
        self.evaluationParamsDict = evaluationParamsDict
        self.d =  len(self.bounds[0])
        (self.lowerBounds,self.upperBounds)= self.bounds
        (self.startLow,self.startUp) = self.bounds
        self.manager = WorkerManager(nbThread,evaluationFunc,self.handleFitness,constraintsFunc,args) 

    def reset(self):
        self.constructNeighbors()
        self.x = self.initPopulation(self.n,self.d,self.startLow,self.startUp) #x position of particle i at time t
        self.v = (self.initPopulation(self.n,self.d,self.startLow,self.startUp) - self.x)/2.0
        self.p = np.copy(self.x) #p previous best position

        self.bestX = np.nan
        self.initFitness()
        self.fp = np.copy(self.f) #best fitness
        self.l = self.getBestNeighbor() #best previous best position in neighborhood amoung p

        self.epochSummary = {'fitness':[],'bestX':[],'topology':[]}
        self.log = {'f':[],'fp':[],'x':[],'v':[],'p':[],'l':[]}
        self.epoch = 0

    def initFitness(self):
        self.f = np.ones((self.n)) * np.nan
        for i in range(self.n):
            self.manager.runEvaluation(i,self.indivToParams(self.x[i]))
            #f[i] = self.evaluate(self.indivToParams(self.p[i]))
        self.manager.finishWork()



    def updatePart(self,i):
        localDist = self.p[self.l[i]] - self.x[i] #if self.l[i] != i else 0
        globalDist = self.bestX - self.x[i] if not(np.any(np.isnan(self.bestX))) else 0
        self.v[i] = (self.w * self.v[i] 
                        + np.random.uniform(high=self.c) * ( self.p[i] - self.x[i])
                        +self.wl * np.random.uniform(high=self.c) * (localDist)
                        +self.wg * np.random.uniform(high=self.c) * (globalDist)
                        )
        self.x[i] = self.x[i] + self.v[i]


        self.confinement(i)

        self.manager.runEvaluation(i,self.indivToParams(self.x[i]))
        #self.f[i] = self.evaluate(self.indivToParams(self.x[i]))

    def handleFitness(self,i,fitness):
        #print(i,self.indivToParams(self.x[i]),fitness)
        if np.isnan(self.f[i]) :
            self.f[i] = fitness
            if np.isnan(self.bestF) or self.f[i] < self.bestF:
                self.bestF = np.copy(self.f[i])
                self.bestX = np.copy(self.x[i])
        else:
            self.f[i] = fitness
            #update l
            self.l[i] = self.bestNeigh(i)


            if self.f[i] < self.fp[i]:
                self.p[i,:] = self.x[i,:]
                self.fp[i] = self.f[i]


            if np.isnan(self.bestF) or self.f[i] < self.bestF:
                self.bestF = np.copy(self.f[i])
                self.bestX = np.copy(self.x[i])
                #print("best Fitness ",i,fitness)
                #print("bestF :",self.bestF)

        self.manager.inProcessPart.remove(i)

    def confinement(self,i):
        for d in range(self.d):
            if self.x[i,d] < self.lowerBounds[d]:
                self.x[i,d] = self.lowerBounds[d]
                self.v[i,d] = 0
            elif self.x[i,d] > self.upperBounds[d]:
                self.x[i,d] = self.upperBounds[d]
                self.v[i,d] = 0

        

    def mainLoop(self):
        while self.epoch < self.nbEvaluationMax and (np.isnan(self.bestF) or  self.bestF > self.acceptableFitness):
            irange =np.arange(self.n)
            np.random.shuffle(irange)
            for i in irange:
                self.updatePart(i)
            self.manager.finishWork()

            topo = False
            if self.lastBestF == self.bestF:
                #if fitness is stagating we change de topology
                self.constructNeighbors()
                topo = True

            self.lastBestF = np.copy(self.bestF)

            self.epoch += 1
            if self.verbose == 1:
                print(str(self.epoch) +":"+str(self.bestF)+":"+str(self.indivToParams(self.bestX)))
                #print(np.min(self.f),np.min(self.fp))
            self.epochSummary['fitness'].append(self.bestF)
            self.epochSummary['bestX'].append(self.indivToParams(self.bestX))
            self.epochSummary['topology'].append(topo)
            self.updateLog()

    def updateLog(self):
        self.log['f'].append(np.copy(self.f))
        self.log['p'].append(np.copy(self.p))
        self.log['x'].append(np.copy(self.x))
        self.log['v'].append(np.copy(self.v))
        self.log['fp'].append(np.copy(self.fp))
        self.log['l'].append(np.copy(self.l))


        




        
    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        indiv = self.transformIndiv(indiv)
        return self.indivToDict(indiv)

    def indivToDict(self,paramList):
        kwargs = {}
        for i in range(len(paramList)):
            kwargs[self.listParam[i]] = paramList[i]
        kwargs.update(self.constantParamsDict)
        return kwargs



    def getBestNeighbor(self):
        """
        Return the index of the best neighbor
        """
        bestNeigh = np.zeros((self.n),dtype=np.int)
        for i in range(self.n):
            bestNeigh[i] = self.bestNeigh(i)
        return bestNeigh

    def bestNeigh(self,i):
        neighbors = self.neighs[i,:self.nbNeigh[i]]
        bestNeighI = np.argmin(self.fp[neighbors])
        res = neighbors[bestNeighI]
        return res

    def constructNeighbors(self,nbNeighMax=10):
        self.neighs = np.random.randint(0,self.n,(self.n,nbNeighMax))
        self.nbNeigh = np.clip(np.random.normal(self.k,0.5,(self.n)).astype(np.int),1,nbNeighMax)
        assert(np.all(self.nbNeigh != 0))

    def initPopulation(self,n,dim,lower,upper):
        """Init random pop"""
        x = np.zeros((n,dim))
        for i in range(n):
            x[i] = np.random.rand(1,dim) * (upper - lower) + lower
        return x




if __name__ == "__main__":
    pso = Spso(100,nbEvaluationMax=200,evaluationFunc=eggHolder,acceptableFitness=-959.6407,verbose=1)
    pso.reset()
    pso.mainLoop()
    #print(pso.epochSummary)


