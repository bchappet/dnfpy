from deap import base
from deap import creator
from deap import tools
import random
from deap import algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, \
                                  toolbox.attr_float, n=2)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
    a = individual[0]
    b = individual[1]
    return (a**2 +(1-b)**2,)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

pop =toolbox.population(n=100)

popEnd = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10)
print(popEnd[0])


