
import matplotlib.pyplot as plt

"""
Extract the mean and std of pso result files

Input:
    fileName = "test"
    folder =  "."
    repet = 100

"""

import begin
import numpy as np
import pickle
import os

class Batch:
    """
    A batch of experience
    """
    def __init__(self,path,fileName,nbExp,nbEpoch=9900):
        self.path = path
        self.fileName = fileName
        self.expList = []
        self.nbExp = nbExp
        self.nbEpoch = nbEpoch
        self.addExpFiles(path,fileName,1,nbExp)

    def addExpFiles(self,path,fileName,start,end):
        for i in range(start,end+1):
            print(i)
            self.addExp(Exp(path+fileName+str(i)+".csv"))

    @staticmethod
    def initOrLoad(path,fileName,nbExp):
        """
        Should call this method to get a batch
        if  .batch file is present it will load the saved batch
        else it will construct a new batch (sloww)
        return a Batch object
        """
        batchFile = path+".batch"
        if os.path.exists(os.path.join(os.getcwd(),batchFile)):
            print("Loading batch in ",batchFile)
            batch = Batch.load(batchFile)
            if int(batch.nbExp) != int(nbExp):
                print("The previous batch has ",str(batch.nbExp)," xp.")
                print("You are constructing a batch with ",str(nbExp)," xp.")
                print("Do you want to erase (e) or add (a) the exp?")
                choice = input()
                if choice == "e":
                    print("Erasing batch. Reading files...")
                    batch = Batch(path,fileName,nbExp)
                    print("Saving new batch")
                    batch.save(batchFile)
                elif choice == "a":
                    print("Adding new experiences to the batch")
                    batch.addExpFiles(path,fileName,1,nbExp)
                    print("Saving extended batch")
                    batchFile = path+".batch"


        else:
            print("Batch not present. Reading files...")
            batch = Batch(path,fileName,nbExp)
            print("Saving batch")
            batch.save(batchFile)
        print("Batch loaded")
        return batch



    def save(self,path):
        """
        It is slow to generate. We save it to experiment graphics
        """
        with open(path,'wb') as f:
            pickle.dump(self,f)
    
    @staticmethod
    def load(path):
        with open(path,'rb') as f:
            return pickle.load(f)



    def addExp(self,exp):
        self.expList.append(exp)

    def saveFitnessEvolution(self):
        array = []
        for exp in self.expList:
            li = np.array(exp.fitnessEvolution())
            ##ensure len(li) == self.nbEpoch (the multithread evaluation might result in higher number of epoch)
            shortLi = li[0:self.nbEpoch]
            array.append(shortLi)

        array = np.array(array).T
        fileName = self.path+"fitnessEvolution.csv"
        print("saving : ",fileName)
        np.savetxt(fileName,array)

    def saveBestInd(self):
        li = [exp.bestInd.ind for exp in self.expList]
        fileName = self.path + "bestInd.pi"
        print("saving : ",fileName)
        with open(fileName,'wb') as f:
            pickle.dump(li,f)

    @staticmethod
    def loadBestInd(fileName):
        with open(fileName,'rb') as f:
            return pickle.load(f)









class Indiv:
    def __init__(self,fitness,ind):
        self.fitness = fitness
        self.ind = ind

class Info:
    def __init__(self,line):
        """
        Read the line and extract the attributes
        The line is like
        eval,fitnessI,indI,bestFitnessI,bestIndI,bestFitness,bestInd

        """
        split = line.split(" , ")
        self.evalNb = eval(split[0])
        self.indI = Indiv(eval(split[1]),eval(split[2]))
        self.bestI = Indiv(eval(split[3]),eval(split[4]))
        self.best = Indiv(eval(split[5]),eval(split[6]))

class Exp:
    """
    One single exp
    """
    def __init__(self,fileName):
        self.bestInd,self.listInd = self.readFile(fileName)
       

    def fitnessEvolution(self):
        """
        Return bestFitness(t)
        """
        return [ind.best.fitness for ind in self.listInd]


    def readFile(self,fileName):
        file = open(fileName)
        lines = file.readlines()
        listInd = [Info(lines[i]) for i in range(len(lines)-1)]
        lastLine = lines[-1]
        split = lastLine.split(" , ")
        bestInd = Indiv(eval(split[1]),eval(split[2]))
        return bestInd,listInd




@begin.start
def main(fileName = "pso_",dir = "expPSO/pso_DOG_competition/",repet= "50"):

    repet = eval(repet)
    batch = Batch.initOrLoad(dir,fileName,repet)
    batch.plotFitnessEvolution()
    plt.show()


