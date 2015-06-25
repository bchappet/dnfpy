from deap import base
import sys
import random
from deap import creator
from deap import tools
from deap import algorithms
import dnfpy.controller.runner as runner
import dnfpy.controller.runnerView as runnerView
from dnfpyUtils.contexts.dnf_WMContext import Dnf_WMContext
from dnfpyUtils.scenarios.scenarioSwitchWM import ScenarioSwitchWM
from dnfpyUtils.models.modelDNF_WM import ModelDNF_WM
import numpy as np
import multiprocessing


def myRandom():
    return random.random() * 10.


def indivToParams(ind):
    the_dict = {}
    listParam = ["iFEF->WM","iWM->FEF","iDNF->FEF","iINPUT->FEF"]
    for i in range(len(ind)):
        the_dict[listParam[i]] = ind[i]
    return the_dict




def genToContext(individual):
    contextParam = individual
    return contextParam



def evaluate(individual, size=51, timeEnd=20,view=False):
    # if individual[0] > individual[1] and individual[2] < individual[3] and\
    if all(x > 0 for x in individual):
        # iExc > iInh   #wExc < wInh
        params = genToContext(individual)
        paramsDict = indivToParams(params)
        context = Dnf_WMContext(**paramsDict)
        scenario = ScenarioSwitchWM()
        model = ModelDNF_WM(size=size)
        if not view:
            (meanError, wellClusterized,time,convTime,errorNbCluster,nbComputationEmpty) = runner.launch(
                model, context, scenario, timeEnd)
        else:
            (meanError, wellClusterized,time,convTime,errorNbCluster,nbComputationEmpty) = runnerView.launch(
                model, context, scenario, timeRatio=1.)

    else:
        (meanError,wellClusterized,errorNbCluster,nbComputationEmpty) = (10,10,10,10)
    if meanError == 0:
        (meanError,wellClusterized,errorNbCluster,nbComputationEmpty) = (9,9,9,9)

    print (meanError,errorNbCluster,nbComputationEmpty)
    return (meanError, errorNbCluster,nbComputationEmpty)



size = 51
timeEnd = 20
nbGen = 30
popSize = 20
nb_param = 4

def runAG():

    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0,-1.0))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", myRandom)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                    toolbox.attr_float, n=nb_param)

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

    random.seed()
    pop = toolbox.population(n=popSize)

    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)

    # popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
    popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.3, ngen=nbGen,
                                stats=stats, halloffame=hof, verbose=True)

    for ind in hof:
        print genToContext(ind)

if __name__ == "__main__":
    if sys.argv[1] == "run_ag":
        runAG()
    else:
        evaluate(eval(sys.argv[1]),size,timeEnd,view=True)
