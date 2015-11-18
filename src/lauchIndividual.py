import sys

from getClassUtils import getClassFromName
import dnfpy.controller.runnerView as runnerView
import dnfpy.controller.runner as runner





indiv = eval((sys.argv[1]))

modelName = sys.argv[2]
scenarioName = sys.argv[3]
statsName = sys.argv[4]

time = eval(sys.argv[5])
withView = eval(sys.argv[6])
args_scenario = None
if len(sys.argv) > 7:
        args_scenario = eval(sys.argv[7])


scenarioClass = getClassFromName(scenarioName, "scenarios")
modelClass = getClassFromName(modelName,"models")
statsClass = getClassFromName(statsName,"stats")

if args_scenario:
    scenario = scenarioClass(**args_scenario)
else:
    scenario = scenarioClass(**indiv)


model = modelClass(**indiv)
stats = statsClass(**indiv)

if withView:
    #view
    res = runnerView.launch(model, scenario,stats,timeEnd=time,timeRatio=0.5)
else:
    #no view
    timeEnd = time
    res = runner.launch(model,scenario,stats,time)
    print(res)




#exemple
#!python lauchIndiviudal.py "[1.96, 0.93, 1.30e-05, 1.]" 49 ScenarioDistracters ModelBsRsdnf NSpikeContext 1 True
#!python lauchIndiviudal.py "['size':49]" ScenarioDistracters ModelBsRsdnf  1 True
