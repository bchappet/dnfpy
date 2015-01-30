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


#listParam = ["iExc","iInh","wExc","wInh","alpha"]
# listGen = ["iExc","ik = iInh/iExc","wK=wExc/wInh","wInh/2","alpha/10"


def genToContext(individual):
    contextParam = np.array(individual)
    contextParam[0] = individual[0]
    contextParam[1] = individual[1]*individual[0]
    contextParam[2] = individual[2]*individual[3]
    contextParam[3] = individual[3]*2
    contextParam[4] = individual[4]*10
    contextParam[5] = individual[5]
    return contextParam


def evaluate(individual, size=51, timeEnd=10):
    # if individual[0] > individual[1] and individual[2] < individual[3] and\
    if (individual > 0).all():
        # iExc > iInh   #wExc < wInh
        params = genToContext(individual)
        context = DnfContext(*params)
        scenarioR = ScenarioRobustness()
        scenarioS = ScenarioSwitch()
        model = ModelDNF(size)
        (meanErrorR, wellClusterizedR) = runner.launch(
            model, context, scenarioR, timeEnd)
        if meanErrorR < 1:
            (meanErrorS, wellClusterizedS) = runner.launch(
                model, context, scenarioS, 6.)
        else:
            (meanErrorS, wellClusterizedS) = (1, 1)
        fitnessError = (meanErrorR + meanErrorS)/2.
        fitnessCluster = (wellClusterizedR + wellClusterizedS)/2.
    else:
        fitnessError = 2.
        fitnessCluster = 2.

    return (fitnessError, fitnessCluster)


def plotHistory(history):
    import matplotlib.pyplot as plt
    import networkx

    graph = networkx.DiGraph(history.genealogy_tree)
    graph = graph.reverse()     # Make the grah top-down
    colors = [toolbox.evaluate(history.genealogy_history[i])[0] for i in graph]
    networkx.draw(graph, node_color=colors)
    plt.show()


size = 51
timeEnd = 20
nbGen = 30
popSize = 20

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", myRandom)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=6)

toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate, size=size, timeEnd=timeEnd)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", cxTwoPointCopy)


stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)
hof = tools.HallOfFame(5, similar=np.array_equal)

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
    print genToContext(ind)
# plotHistory(history)
