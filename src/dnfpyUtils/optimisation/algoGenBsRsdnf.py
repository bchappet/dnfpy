from deap import base
import random
from deap import creator
from deap import tools
from deap import algorithms
import dnfpy.controller.runner as runner
from dnfpyUtils.contexts.nSpikeContext import NSpikeContext
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.models.modelBsRsdnf import ModelBsRsdnf
import numpy as np
import multiprocessing
import logging

def myRandom():
    return random.random()


#listParam = ["iExc","iInh","pExc","pInh","alpha","tau"]
# listGen = ["iExc","ik = iInh/iExc","pK=pExc/pInh","pInh","alpha/10","tau"

listParam = ["iExc","iInh","pExc","pInh"]#,"alpha","tau"]

def contextToGen(contextParam):
    individual = [0] * len(contextParam)
    individual[0] = contextParam[0]
    individual[1] = contextParam[1]/contextParam[0]
    individual[2] = contextParam[2]/contextParam[3]
    individual[3] = contextParam[3]
    return individual



def genToContext(individual):
    contextParam = [0] * len(individual)
    contextParam[0] = individual[0]
    contextParam[1] = individual[1]*individual[0]
    contextParam[2] = individual[2]*individual[3]
    contextParam[3] = individual[3]
    return contextParam

def indivToDict(size,listParam,individual):
    kwargs = {'size':size}
    for i in range(len(individual)):
        kwargs[listParam[i]] = individual[i]
    return kwargs


def evaluate(individual, size=51, timeEnd=8.,allowedTime=60):
    if all(x > 0 for x in individual):
        params = genToContext(individual)
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        model = ModelBsRsdnf(**indivToDict(size,listParam,individual))
        (meanErrorR, wellClusterizedR,simuTimeEnd,convTime,maxNbAct,meanNbAct,elapsedTime,shapeR)\
        = runner.launch(
                model, scenarioR, timeEnd,allowedTime=allowedTime)
        print("forParams %s"%params)
        logging.info(params)
        if simuTimeEnd < timeEnd:
            print("simuTimeEnd %s < timeEnd %s (elapsed time %s allowed %s)"%\
                  (simuTimeEnd,timeEnd,elapsedTime,allowedTime))
            fitnessError = timeEnd - simuTimeEnd
            fitnessCluster = timeEnd -simuTimeEnd
        else:
            if meanErrorR < 1 and wellClusterizedR < 2:
                (meanErrorS, wellClusterizedS,simuTimeEnds,convTimes,maxNbActs,meanNbActs,elapsedTime,shapeS)\
                    = runner.launch(\
                    model, scenarioS, 6.,allowedTime=allowedTime)
            else:
               (meanErrorS, wellClusterizedS,shapeS) = (1, 2,10)

            fitnessError = (meanErrorR + meanErrorS)/2.
            fitnessCluster = (wellClusterizedR + wellClusterizedS)/2.
            fitnessShape = (shapeR + shapeS)/2.
            #fitnessError = meanErrorR
            #fitnessCluster = wellClusterizedR
    else:
        fitnessError = 2.
        fitnessCluster = 4.
        fitnessShape = 10


    print("%s,%s,%s"%(fitnessError, fitnessCluster,fitnessShape))
    logging.info("%s,%s,%s"%(fitnessError, fitnessCluster,fitnessShape))
    return (fitnessShape,)


size = 49
timeEnd = 20
allowedTime=360*10
nbGen = 30
popSize = 30
logging.basicConfig(filename='algoGenBsRsdnf.log',level=logging.DEBUG)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", myRandom)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=4)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate, size=size, timeEnd=timeEnd,allowedTime=allowedTime)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)
hof = tools.HallOfFame(5)


random.seed()
pop = toolbox.population(n=popSize)
initParams = [1.96, 0.93, 1.30e-05, 1.]
pop[0][:] = contextToGen(initParams)


pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

# popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=nbGen,
                             stats=stats, halloffame=hof, verbose=True)
for ind in hof:
    print genToContext(ind)
    logging.info(str(genToContext(ind)))
