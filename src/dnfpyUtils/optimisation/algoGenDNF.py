from deap import base
import random
from deap import creator
from deap import tools
from deap import algorithms
from deap.tools import History
import dnfpy.controller.runner as runner
from dnfpyUtils.contexts.dnfContext import DnfContext
from dnfpyUtils.scenarios.scenarioRobustness import ScenarioRobustness
from dnfpyUtils.scenarios.scenarioSwitch import ScenarioSwitch
from dnfpyUtils.models.modelDNF import ModelDNF
import numpy as np
import multiprocessing


def myRandom():
    return random.random()


listParam = ["iExc","iInh","wExc","wInh"]
# listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh/2","alpha/10"


def genToContext(individual):
    contextParam = [0] * len(individual)
    contextParam[0] = individual[0]
    contextParam[1] = individual[1]*individual[0]
    contextParam[2] = individual[2]*individual[3]
    contextParam[3] = individual[3]*2
    return contextParam

def indivToDict(size,listParam,individual):
    kwargs = {'size':size}
    for i in range(len(individual)):
        kwargs[listParam[i]] = individual[i]
    return kwargs




def evaluate(individual, size=51, timeEnd=10):
    # if individual[0] > individual[1] and individual[2] < individual[3] and\
    if all(x > 0 for x in individual):
        # iExc > iInh   #wExc < wInh
        params = genToContext(individual)
        print(params)
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        model = ModelDNF(**indivToDict(size,listParam,individual))
        (errorR,wellClusterizedR,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShapeR)\
        = runner.launch(
            model, scenarioR, timeEnd)
        if errorR < 1:
            (errorS,wellClusterizedS,time,convergence,maxNbAct,meanNbAct,elapsedTime,errorShapeS)\
            = runner.launch(
                model, scenarioS, 6.)
        else:
            (errorS, wellClusterizedS,errorShapeS) = (10, 10, 10)
        fitnessError = (errorR + errorS )/2.
        fitnessCluster = (wellClusterizedR + wellClusterizedS)/2.
        fitnessShape = (errorShapeR + errorShapeS)/2.
    else:
        fitnessError = 10.
        fitnessCluster = 10
        fitnessShape = 10

    return ( fitnessShape,)




size = 49
timeEnd = 50
nbGen = 30
popSize = 30
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", myRandom)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=4)

toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate, size=size, timeEnd=timeEnd)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)


stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)
hof = tools.HallOfFame(5)

history = History()
# Decorate the variation operators
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate", history.decorator)

random.seed()
pop = toolbox.population(n=popSize)
history.update(pop)

pool = multiprocessing.Pool()
toolbox.register("map", pool.map)

# popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=nbGen,
                             stats=stats, halloffame=hof, verbose=True)

for ind in hof:
    print indivToDict(size,listParam,genToContext(ind))
# plotHistory(history)
