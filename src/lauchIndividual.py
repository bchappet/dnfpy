import sys

from getClassUtils import getClassFromName
import dnfpy.controller.runnerView as runnerView



#indiv DNF: [1.25,0.7,0.1,10,10,0.64]

def evaluateView(individual,modelClass,contextClass,scenario, size=51,timeRatio=1):
    context = contextClass(*individual)
    model = modelClass(size=size)
    return runnerView.launch(model, context, scenario, timeRatio)


print sys.argv[1]
indiv = eval((sys.argv[1]).strip().replace(" ",""))
size = eval(sys.argv[2])
scenarioName = sys.argv[3]
modelName = sys.argv[4]
contextName = sys.argv[5]
timeRatio = eval(sys.argv[6])

scenarioClass = getClassFromName(scenarioName, "scenarios")
contextClass = getClassFromName(contextName,"contexts")
modelClass = getClassFromName(modelName,"models")
evaluateView(indiv,modelClass,contextClass, scenarioClass(), size,timeRatio)
