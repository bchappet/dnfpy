import math
import sys
from PyQt4.QtCore import pyqtSlot
import numpy as np
import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from dnfpyUtils.optimisation.worker import Worker
import time
from multiprocessing import Queue



class PSO():
    """
    Particle swarm optimisation class
    Omega : inertia
    phiP : atracted by best of part
    phiG : attracted by best of pop

    -0.2144,-0.4040,2.03249 is good for exploration
    -0.2144,1,1 seems better for exploitation
    0.2,1,1 is very good
    """
    #def __init__(self,view,swarmSize=100,nbEvaluationMax=1000,omega=.9,
    #             phiP=2.,phiG=2.,nbThread=8,argv=[""]):
    #def __init__(self,view,swarmSize=100,nbEvaluationMax=1000,omega=-0.2144,
    #             phiP=-0.4040,phiG=2.03249,nbThread=8,argv=[""]): good
    #def __init__(self,view,swarmSize=100,nbEvaluationMax=1000,omega=0.9,
    #             phiP=1.0,phiG=1.0,nbThread=8,argv=[""]):
    def __init__(self,swarmSize=100,nbEvaluationMax=1000,omega=0.721347,
                 phiP=1.193147,phiG=1.193147,nbThread=8,verbose=False):
        #self.triggerUpdate.connect(view.updateData)

        self.verbose = verbose

        self.listParam = self.getListParam()
        self.constantParamsDict = self.getConstantParamsDict()
        self.evaluationParamsDict = self.getEvaluationParamsDict()
        self.bounds = self.getBounds()
        self.startingBounds = self.getStartBounds()

        #Bound execution nbIteration
        self.acceptableFitness = self.getObjectiveFitness()
        self.nbEvaluationMax = nbEvaluationMax

        self.swarmSize = swarmSize #swarmSize
        self.omega = omega #Inertia weight
        self.phiP = phiP #Particle's best weight
        self.phiG = phiG #Swarm's best weight
        self.nbDim = len(self.listParam)

        #save for plot
        self.savePart = []
        self.timeStamps = []
        self.bestXList = []
        self.bestXTimeList = []

        self.workerList = []
        for i in range(nbThread):
            self.workerList.append(self.initWorker(i))

        self.workerResultsQueue = Queue() #will store tuple: (particleId,fitness)
        self.inProcessPart = []

    def initWorker(self,i):
        return Worker(i,self.evaluate,self.onWorkerResult)



    def getObjectiveFitness(self):
        return 10e-10


    def getListParam(self):
        return ["x","y","z","a","b"]
        #return ["x","y"]

    def getBounds(self):
        """return (lowerBounds,upperBounds"""
        lowerBounds = np.array([-20,-20,-20,-20,-20])
        upperBounds = np.array([20,20,20,20,20])
        #lowerBounds = np.array([-100,-100,-100,-100,-100])
        #upperBounds = np.array([100,100,100,100,100])
        return (lowerBounds,upperBounds)

    def getStartBounds(self):
        """return (lowerBounds,upperBounds"""
        lowerBounds = np.array([-10,-10,-10,-10,-10])
        upperBounds = np.array([10,10,10,10,10])
        return (lowerBounds,upperBounds)

    def evaluate(self,indiv):
        x = indiv['x']
        y = indiv['y']
        time.sleep(0.2)

        return x**2 + (1-y)**2 +(2-indiv["z"])**2 + \
                    (5-indiv["a"])**2 + (10 - indiv["b"])**2
        #rosenbrock function
        #return (1 - x)**2 + 100*(y - x**2)**2

    def getConstantParamsDict(self):
        return {}

    def getEvaluationParamsDict(self):
        return {}


    def indivToParams(self,indiv):
        """return the parameters dictionary which will be given to the model"""
        return self.indivToDict(indiv)

    def indivToDict(self,paramList):
        kwargs = {}
        for i in range(len(paramList)):
            kwargs[self.listParam[i]] = paramList[i]
        kwargs.update(self.constantParamsDict)
        return kwargs

    def requestWorker(self,i,waitingTask):
        if i not in self.inProcessPart:
            while(not(self.workerResultsQueue.empty())):
                tup = self.workerResultsQueue.get()
                waitingTask(*tup)

            for i_worker in range(len(self.workerList)):
                worker = self.workerList[i_worker]
                if not(worker.is_alive()):
                    newWorker =  self.initWorker(i_worker)
                    self.workerList[i_worker] = newWorker
                    self.inProcessPart.append(i)
                    return newWorker

           #we treat the queue instead of sleeping
            else:
                time.sleep(0.1)
        else:
            return


        return self.requestWorker(i,waitingTask)

    def finishWork(self,task):
        for worker in self.workerList:
            if worker.is_alive():
                worker.join()
        while(not(self.workerResultsQueue.empty())):
            tup = self.workerResultsQueue.get()
            task(*tup)

    def onWorkerResult(self,i,newFitness):
        self.workerResultsQueue.put((i,newFitness))

    def runEvaluation(self,i,indiv):
        #request a worker for particle i. If no worker are available wait.
        #If a worker already works on i, return None, i will not be evaluated again
        worker = self.requestWorker(i,waitingTask=self.handleFitness)
        if worker:
            worker.evaluate(i,indiv)



    def addFitness(self,i,newFitness):
        self.inProcessPart.remove(i)
        self.fitness[i] = newFitness

    def handleFitness(self,i,newFitness):
        #update best known position
        if newFitness < self.fitness[i]:
                #update particle's best known fitness
                self.fitness[i] = newFitness
                #update particle's best known position
                self.p[i,:] = self.x[i,:]
                #update swarm's best-known position
                if newFitness < self.bestFitness :
                    self.bestIndex = i
                    self.bestXList.append(self.p[self.bestIndex,:])
                    self.bestXTimeList.append(self.evaluationNb)
                    self.bestFitness = newFitness
                    if self.verbose:
                        print("##bestFitness : %s, indiv: %s"%(self.bestFitness,self.indivToParams(self.x[self.bestIndex,:])))

        self.inProcessPart.remove(i)

        self.evaluationNb += 1
        if not(self.verbose):
            print(self.evaluationNb,",",newFitness,",",self.indivToParams(self.x[i,:]),",",self.fitness[i],",",self.indivToParams(self.p[i,:]),",",self.bestFitness,",",self.indivToParams(self.p[self.bestFitness]))





    def run(self):
        (lowerBounds,upperBounds)= self.bounds
        (startLow,startUp) = self.startingBounds
        #initiaize the velocity boundaries
        rangeVelocity =  upperBounds - lowerBounds
        lowerVelocity = - 0.5 * rangeVelocity
        upperVelocity = + 0.5 * rangeVelocity

        #Initialize Swarm
        self.x = self.initPopulation(self.swarmSize,self.nbDim,startLow,startUp) #particles positions
        #print("x : %s"%x)
        self.p = np.copy(self.x) #best known positions
        v = self.initPopulation(self.swarmSize,self.nbDim,lowerVelocity,upperVelocity) #Velocities
        #print("v : %s"%v)

        #compute fitness of initial particle position
        self.fitness = np.zeros((self.swarmSize))
        for i in range(self.swarmSize):
            worker = self.requestWorker(i,waitingTask=self.addFitness)
            if worker:
                worker.evaluate(i,self.indivToParams(self.x[i,:]))

        self.finishWork(self.addFitness)

        #determine fitness and index of best particles
        (self.bestFitness, self.bestIndex) = self.getMinIndex(self.fitness)

        #perform optimization iteration until acceptable fitness is achived
        #or the maximum of fitness evaluation has been performed
        self.evaluationNb = self.swarmSize#the iterations above is counted as iteartion
        self.bestXList.append(self.p[self.bestIndex,:])
        self.bestXTimeList.append(self.evaluationNb)


        if self.verbose:
                print("initBest",",",self.bestFitness,",",self.indivToParams(self.p[self.bestIndex,:]))


        while self.evaluationNb < self.nbEvaluationMax and self.bestFitness > self.acceptableFitness:
            #pick index from a random particle in the swarm
            if self.verbose and self.evaluationNb % 100 == 0:
                    print("Eval : ",self.evaluationNb)
            i = -1
            while(i not in self.inProcessPart and i== -1):
                i = random.randint(0,self.swarmSize-1)
            #pick random weights between [O,1)
            rP = random.random()
            rG = random.random()

            #update velocity for i'th particle
            v[i,:] = self.omega * v[i,:] + \
                rP * self.phiP * (self.p[i,:] - self.x[i,:] ) + \
                rG * self.phiG * (self.p[self.bestIndex,:] - self.x[i,:])

            #bound velocity
            v[i,:] = self.applyBounds(v[i,:],lowerVelocity,upperVelocity)
            #update position of the i'th particle
            self.x[i,:] = self.x[i,:] + v[i,:]
            #bound position
            self.x[i,:] = self.applyBounds(self.x[i,:],lowerBounds,upperBounds)
            #compute fitness

            self.runEvaluation(i,self.indivToParams(self.x[i,:]))
            #self.handleFitness(i,self.evaluate(self.indivToDict(self.x[i,:])))

        #return best solution
        self.bestX = self.p[self.bestIndex,:]
        #print("best index : %s, bestX : %s"%(bestIndex,self.bestX))
        #self.drawFig()
        #plt.show()
        print("BEST",",",self.bestFitness,",",self.indivToParams(self.bestX))

    def applyBounds(self,x,low,up):
        return np.minimum(up,np.maximum(low,x))


    def getMinIndex(self,array):
        """return (min,minIndex)"""
        return (np.min(array),np.argmin(array))

    def initPopulation(self,nb,dim,lower,upper):
        """Init random pop"""
        x = np.zeros((nb,dim))
        for i in range(nb):
            x[i] = np.random.rand(1,dim) * (upper - lower) + lower
        return x

    def getParticules(self):
        return (self.timeStamps,self.savePart)

    def getBestParticules(self):
        return (self.bestXTimeList,self.bestXList)

    def getNbDim(self):
        return self.nbDim

    def getSwarmSize(self):
        return self.swarmSize



class QtApp(pg.GraphicsWindow):
    def __init__(self):
        pg.setConfigOption('background', 'w')
        super(QtApp,self).__init__("pso")
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)


    def setModel(self,model):
        self.model = model
        self.size = self.model.getNbDim()
        self.swarmSize = self.model.getSwarmSize()

        self.width = int(math.ceil(math.sqrt(self.size)))
        self.height = int(math.ceil(self.size/float(self.width)))
        nbCurve = 30
        self.nbCurveStep = int(math.ceil(float(self.swarmSize)/nbCurve))

        self.initPlot()
        self.initCurves()

    def initPlot(self):
        #Prepare the plots
        self.plots = []
        for i in range(self.size):
            if i % self.width == 0:
                self.nextRow()
            self.plots.append(self.addPlot(title=self.model.listParam[i]))

    def initCurves(self):
        self.curves = []
        blackPen = pg.mkPen(color=0.0,width=2)
        for i in range(self.size):
            self.curves.append([])
            for j in range(0,self.swarmSize,self.nbCurveStep):
                self.curves[i].append(self.plots[i].plot(pen=(40,200,40)))
            self.curves[i].append(self.plots[i].plot(pen=blackPen))

    @pyqtSlot()
    def updateData(self):
        partTuple = self.model.getParticules()
        bestTuple = self.model.getBestParticules()
        self.arr = np.array(partTuple[1])
        self.arrBest = np.array(bestTuple[1])
        self.X = np.array(partTuple[0])
        self.XBest = np.array(bestTuple[0])
        self.updateFig()

    def updateFig(self):
        for i in range(self.size):
            jj = 0
            for j in range(0,self.arr.shape[1],self.nbCurveStep):
                self.curves[i][jj].setData(self.X,self.arr[:,j,i])
                jj += 1
            self.curves[i][-1].setData(self.XBest,self.arrBest[:,i])

class PSOView(QtCore.QThread,PSO):
    triggerUpdate = QtCore.pyqtSignal()
    def __init__(self,view,swarmSize=100,nbEvaluationMax=1000,omega=0.721347,
                 phiP=1.193147,phiG=1.193147,nbThread=8,argv=[""]):
        super(PSO,self).__init__()
        PSO.__init__(self,swarmSize=100,nbEvaluationMax=1000,omega=0.721347,
                 phiP=1.193147,phiG=1.193147,nbThread=8,argv=[""])

        self.triggerUpdate.connect(view.updateData,type=QtCore.Qt.DirectConnection)

    def run(self):
        PSO.run(self)
        self.triggerUpdate.emit()
        sys.exit()


    def handleFitness(self,i,newFitness):
        PSO.handleFitness(self,i,newFitness)
        print("evaluationNb : %s"%self.evaluationNb)
        self.savePart.append(np.copy(self.x))
        self.timeStamps.append(self.evaluationNb)
        self.triggerUpdate.emit()





if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    #view = QtApp()
    model = PSO(swarmSize=100,nbEvaluationMax=10000,nbThread=8,verbose=True)
    model.run()
    #view.setModel(model)
    #model.start()
    #sys.exit(app.exec_())
