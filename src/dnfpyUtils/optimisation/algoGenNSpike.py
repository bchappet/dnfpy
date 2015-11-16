from deap import base
import random
from deap import creator
from deap import tools
from deap import algorithms
from deap.tools import History
import dnfpy.controller.runner as runner
from dnfpyUtils.contexts.nSpikeContext import NSpikeContext
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.models.modelNSpike import ModelNSpike
import numpy as np
import multiprocessing

def myRandom():
    return random.random()


#listParam = ["iExc","iInh","pExc","pInh","alpha","tau"]
# listGen = ["iExc","ik = iInh/iExc","pK=pExc/pInh","pInh","alpha/10","tau"


def genToContext(individual):
    contextParam = [0] * len(individual)
    contextParam[0] = individual[0]
    contextParam[1] = individual[1]*individual[0]
    contextParam[2] = individual[2]*individual[3]
    contextParam[3] = individual[3] * 2
    return contextParam


def evaluate(individual, size=51, timeEnd=10,allowedTime=5):
    if all(x > 0 for x in individual):
        params = genToContext(individual)
        context = NSpikeContext(*params)
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        model = ModelNSpike(size=size)
        (errorR,wellClusterizedR,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShapeR)\
        = runner.launch(
        model, context, scenarioR, timeEnd,allowedTime=allowedTime)
        if errorR < 1 and wellClusterizedR < 2:
                (errorS,wellClusterizedS,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShapeS)\
                = runner.launch(
                    model, context, scenarioS, 6.,allowedTime=allowedTime)
        else:
                (errorS, wellClusterizedS,errorShapeS) = (10, 10, 10)

        fitnessError = (errorR + errorS )/2.
        fitnessCluster = (wellClusterizedR + wellClusterizedS)/2.
        fitnessShape = (errorShapeR + errorShapeS)/2.
    else:
        fitnessError = 10
        fitnessCluster = 10
        fitnessShape = 10


    print("%s,%s,%s"%(fitnessError, fitnessCluster,fitnessShape))
    return (fitnessShape,)


size = 49
timeEnd = 20
nbGen = 30
popSize = 30

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", myRandom)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=4)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate, size=size, timeEnd=timeEnd)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)
hof = tools.HallOfFame(5)


random.seed()
pop = toolbox.population(n=popSize)

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

# popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=nbGen,
                             stats=stats, halloffame=hof, verbose=True)

for ind in hof:
    print genToContext(ind)
