import sys

from getClassUtils import getClassFromName
import dnfpy.controller.runnerView as runnerView
import dnfpy.controller.runner as runner



#indiv DNF: [1.25,0.7,0.1,10,10,0.64]



indiv = eval((sys.argv[1]))
scenarioName = sys.argv[2]
modelName = sys.argv[3]

time = eval(sys.argv[4])


scenarioClass = getClassFromName(scenarioName, "scenarios")
modelClass = getClassFromName(modelName,"models")
scenario = scenarioClass()
model = modelClass(**indiv)
if eval(sys.argv[5]):
       
    #view
    timeRatio = time
    res = runnerView.launch(model, scenario, timeRatio)
else:
    #no view
    timeEnd = time
    res = runner.launch(model,scenario,timeEnd)




#exemple
#!python lauchIndiviudal.py "[1.96, 0.93, 1.30e-05, 1.]" 49 ScenarioDistracters ModelBsRsdnf NSpikeContext 1 True
