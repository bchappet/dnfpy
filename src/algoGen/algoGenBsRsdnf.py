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
from dnfpyUtils.models.modelBsRsdnf import ModelBsRsdnf
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
    contextParam[3] = individual[3]
    contextParam[4] = individual[4]*10
    contextParam[5] = individual[5]
    return contextParam


def evaluate(individual, size=51, timeEnd=8,allowedTime=25,dt=0.01):
    if all(x > 0 for x in individual):
        params = genToContext(individual)
        context = NSpikeContext(*params)
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        model = ModelBsRsdnf(size)
        (meanErrorR, wellClusterizedR,nbItR) = runner.launch(
                model, context, scenarioR, timeEnd,allowedTime=allowedTime)
        if nbItR < timeEnd/dt:
            print("nbItr %s < timeEnd/dt %s"%(nbItR,timeEnd/dt))
            fitnessError = timeEnd/dt - nbItR
            fitnessCluster = timeEnd/dt -nbItR
        else:
            if meanErrorR < 1 and wellClusterizedR < 2:
                (meanErrorS, wellClusterizedS,nbItS) = runner.launch(
                    model, context, scenarioS, 6.,allowedTime=allowedTime)
            else:
                (meanErrorS, wellClusterizedS) = (1, 4)

            fitnessError = (meanErrorR + meanErrorS)/2.
            fitnessCluster = (wellClusterizedR + wellClusterizedS)/2.
    else:
        fitnessError = 2.
        fitnessCluster = 4.


    print("%s,%s"%(fitnessError, fitnessCluster))
    return (fitnessError, fitnessCluster)


size = 51
timeEnd = 20
nbGen = 30
popSize = 20

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", myRandom)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=6)

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

popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=nbGen,
                             stats=stats, halloffame=hof, verbose=True)
for ind in hof:
    print genToContext(ind)
