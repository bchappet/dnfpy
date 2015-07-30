import math
from PyQt4.QtCore import pyqtSlot
import numpy as np
import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from worker import Worker
import time
from multiprocessing import Queue
import sys
class AlgoGen(QtCore.QThread):
    triggerUpdate = QtCore.pyqtSignal()
    """Genetic algorithm optimisation class"""
    #def __init__(self,view,swarmSize=100,nbEvaluationMax=1000,omega=.9,
    #             phiP=2.,phiG=2.,nbThread=8,argv=[""]):
    def __init__(self,view,swarmSize=100,nbEvaluationMax=1000,eliteRatio=0.2,
                 bestIndRatio=0.2,mutationRate=1.,nbMutation=2,nbThread=8,argv=[""]):
        super(AlgoGen,self).__init__()
        if view:
            self.triggerUpdate.connect(view.updateData,type=QtCore.Qt.DirectConnection)
        #self.triggerUpdate.connect(view.updateData)

        self.listParam = self.getListParam()
        self.nbDim = len(self.listParam)

        self.constantParamsDict = self.getConstantParamsDict()
        self.evaluationParamsDict = self.getEvaluationParamsDict()

        self.bounds = self.getBounds()
        self.startingBounds = self.getStartBounds()

        #Bound execution nbIteration
        self.acceptableFitness = self.getObjectiveFitness()
        self.nbEvaluationMax = nbEvaluationMax

        self.swarmSize = swarmSize #swarmSize

        self.eliteNb = int(round(self.swarmSize*eliteRatio))
        print("eliteNb : %s"%self.eliteNb)
        self.bestIndNb = int(round(self.swarmSize*bestIndRatio))
        print("bestInd : %s"%self.bestIndNb)
        self.mutationRate = mutationRate
        self.nbMutation = nbMutation
        self.mutationVar = [abs(high-low)/10. for low,high in zip(self.bounds[0],self.bounds[1])]
        #print("mutation vars: %s"%self.mutationVar)

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
            return self.getBounds()

    def evaluate(self,indiv):
        x = indiv['x']
        y = indiv['y']
        time.sleep(1)

        #print("evaluate %s"%indiv)
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
       # print self.inProcessPart
        if i not in self.inProcessPart:
            while(not(self.workerResultsQueue.empty())):
                tup = self.workerResultsQueue.get()
                #print("get a tup to handle")
                waitingTask(*tup)

            for i_worker in range(len(self.workerList)):
                #print("i_worker %s"%i_worker)
                worker = self.workerList[i_worker]
                if not(worker.is_alive()):
                    newWorker =  self.initWorker(i_worker)
                    self.workerList[i_worker] = newWorker
                    self.inProcessPart.append(i)
                    return newWorker

           #we treat the queue instead of sleeping
            else:
                #print("sleep")
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

    def runEvaluation(self):
        #request a worker for particle i. If no worker are available wait.
        #If a worker already works on i, return None, i will not be evaluated again
        for i in range(self.swarmSize):
            #print(i)
            #compute fitness of poupulation
            worker = self.requestWorker(i,waitingTask=self.handleFitness)
            if worker:
               worker.evaluate(i,self.indivToParams(self.pop[i,:]))

        self.finishWork(self.handleFitness)



    def handleFitness(self,i,newFitness):
        #update best known position
        #in GA we don't keep old fitness
        #update particle's best known fitness
        self.fitness[i] = newFitness
        #print("part best position : i: %s, position : %s"%(i,newFitness))
        #update swarm's best-known position
        if newFitness < self.bestFitness :
            self.bestIndex = i
            indiv = self.pop[self.bestIndex]
            self.bestX = indiv
            self.bestXList.append(indiv)
            self.bestXTimeList.append(self.evaluationNb)
            self.bestFitness = newFitness
            #print("##bestFitness : %s, indiv: %s"%(self.bestFitness,self.indivToParams(indiv)))

        if (self.evaluationNb % self.swarmSize) == 0:
            self.savePart.append(np.copy(self.pop))
            self.timeStamps.append(self.evaluationNb)
            self.triggerUpdate.emit()
            print("end of generation %s best fitness: %s, bestIndiv: %s"%(self.evaluationNb/self.swarmSize,self.bestFitness,self.indivToParams(self.bestX)))

            

        self.inProcessPart.remove(i)
        #print("evaluationNb : %s"%self.evaluationNb)
        self.evaluationNb += 1


    def run(self):
        (lowerBounds,upperBounds)= self.bounds
        (startLow,startUp) = self.startingBounds

        #Initialize population
        self.pop = self.initPopulation(self.swarmSize,self.nbDim,startLow,startUp) #particles positions
        self.fitness = np.zeros((self.swarmSize))
        self.evaluationNb = 0
        self.bestFitness = 1e30


        while self.evaluationNb < self.nbEvaluationMax and self.bestFitness > self.acceptableFitness:

            #compute fitness of population in parallel
            self.runEvaluation()


            #order indiv according to fitness
            orderedPop = self.orderPop(self.pop,self.fitness)
            #create the next generation
            #the elite stays in the next gen
            self.pop[0:self.eliteNb] = orderedPop[0:self.eliteNb]
            #recombinate the best individuals
            self.pop[self.eliteNb:] = self.recombinations(orderedPop[0:self.bestIndNb],len(self.pop)-self.eliteNb)
            #mutate individuals (not elite)
            self.mutations(self.pop[self.eliteNb:],self.mutationRate)
            #print("before mut :  after mut %s"%(save-self.pop[self.eliteNb:]))


        #return best solution
        self.bestX = self.pop[self.bestIndex,:]
        #print("best index : %s, bestX : %s"%(bestIndex,self.bestX))
        #self.drawFig()
        #plt.show()
        print(self.bestFitness,self.indivToParams(self.bestX))
        self.triggerUpdate.emit()


    def mutations(self,population,mutationRate):
        indexes = np.random.random(len(population)) <= mutationRate
        population[indexes]=self.mutate_array(population[indexes])
        #self.mutate_array(population[indexes])

    def mutate(self,indiv):
        """
        gaussian mut: gaussian sample around the value
        """
        res = np.copy(indiv)

        for i in xrange(self.nbMutation):
            #chose the position of mutation
            positionI = np.random.randint(0,self.nbDim)
            res[positionI] = self.mutationPoint(indiv,positionI)
        return res
        #print("before mut : %s, after mut %s"%(save,indiv))

    def mutationPoint(self,indiv,position):
            return np.random.normal(indiv[position],self.mutationVar[position])

    def mutate_array(self,pop):
        res = np.zeros_like(pop)
        for i in xrange(len(pop)):
            res[i] = self.mutate(pop[i])
        return res





    def recombinations(self,individuals,nbChildren):
        children = np.zeros((nbChildren,self.nbDim))
        indexes = np.arange(0,len(individuals))

        for i in xrange(nbChildren):
            #choose the two parents
            parentI = np.random.choice(indexes,2,replace=False)
            child = self.recombinate(individuals[parentI[0]],individuals[parentI[1]])
            children[i] = child

        return children

    def recombinate(self,parent1,parent2):
        """
        One point cross-over
        """
        children = np.zeros_like(parent1)
        crossPoint = np.random.randint(0,len(parent1))
        children[0:crossPoint] = parent1[0:crossPoint]
        children[crossPoint:] = parent2[crossPoint:]
        return children




    def orderPop(self,pop,fitness):
        """
        Order population according to fitness array
        """
        sortedIndexes = fitness.argsort()
        return pop[sortedIndexes]



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




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([""])
    view = QtApp()
    model = AlgoGen(view,swarmSize=100,nbEvaluationMax=10e10,nbThread=8)
    view.setModel(model)
    model.start()
    sys.exit(app.exec_())
