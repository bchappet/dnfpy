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
import multiprocessing as mp
from scoop import futures

class AlgoGen(object):
    def __init__(self,modelClass,contextClass,size=51,timeEnd=20,nbGen=30,popSize=20,pool=None):
        random.seed()
        self.modelClass = modelClass
        self.contextClass = contextClass
        self.size = size
        self.timeEnd = timeEnd
        self.nbGen = nbGen

        self.toolbox = base.Toolbox()
        self.constructAlgo()
        self.hof = tools.HallOfFame(5, similar=np.array_equal)
        self.pop = self.toolbox.population(n=popSize)
        if pool:
            self.toolbox.register("map", pool.map)



    def lauch(self):
        # self.popEnd = algorithms.eaSimple(self.pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=40,
        self.popEnd = algorithms.eaSimple(self.pop, self.toolbox, cxpb=0.5, mutpb=0.3, ngen=self.nbGen,
                             stats=self.stats, halloffame=self.hof, verbose=True)



    def myRandom(self):
        return random.random()

    def finalize(self):
        for ind in self.hof:
            print self.genToContext(ind)

    def evaluate(individual,modelClass,contextClass, size=51, timeEnd=10):
        # if individual[0] > individual[1] and individual[2] < individual[3] and\
        if (individual > 0).all():
            # iExc > iInh   #wExc < wInh
            params = self.genToContext(individual)
            context = contextClass(*params)
            scenarioR = ScenarioRobustness()
            scenarioS = ScenarioSwitch()
            model = modelClass(size)
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

    def genToContext(self,individual):
        return individual




    def constructAlgo(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

        self.toolbox.register("attr_float", self.myRandom)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                        self.toolbox.attr_float, n=6)

        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.evaluate,
                              modelClass=self.modelClass,contextClass=self.contextClass,
                              size=self.size, timeEnd=self.timeEnd)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", self.cxTwoPointCopy)


        self.stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        self.stats.register("avg", np.mean, axis=0)
        self.stats.register("std", np.std, axis=0)
        self.stats.register("min", np.min, axis=0)
        self.stats.register("max", np.max, axis=0)

    def cxTwoPointCopy(self,ind1, ind2):
        """Execute a two points crossover with copy on the input individuals. The
        copy is required because the slicing in np returns a view of the data,
        which leads to a self overwritting in the swap operation. It prevents
        """
        size = len(ind1)
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:  # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1

        ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] \
            = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()

        return ind1, ind2


from dnfpyUtils.models.modelDNF import ModelDNF
from dnfpyUtils.contexts.dnfContext import DnfContext

class AlgoGenDNF(AlgoGen):
    def __init__(self,size=51,timeEnd=20,nbGen=30,popSize=20,pool=None):
        super(AlgoGenDNF,self).__init__(modelClass=ModelDNF,contextClass=DnfContext,
                                        size=size,timeEnd=timeEnd,nbGen=nbGen,popSize=popSize,
                                        pool=pool)

    def genToContext(self,individual):
        contextParam = np.array(individual)
        contextParam[0] = individual[0]
        contextParam[1] = individual[1]*individual[0]
        contextParam[2] = individual[2]*individual[3]
        contextParam[3] = individual[3]*2
        contextParam[4] = individual[4]*10
        contextParam[5] = individual[5]
        return contextParam

if __name__ == "__main__":
    pool = mp.Pool()
    algo = AlgoGenDNF(pool=pool)
    algo.lauch()
    algo.finalize()


