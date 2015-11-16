import sys
import dnfpy.controller.runnerView as runnerView
import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import begin #very usefull arg parsing library


"""
Parameter:
ModelName: str: ModelNSpike...
Scenario: str ScenarioTracking...


"""
@begin.start
def main(model = "ModelDNF1D",size="101",dim="2",tr="0.5",stats="None",scenario="ScenarioTracking",params="{}",pause="False",gui="True",timeEnd="40.0"):
    """
    model : name of the model
    size : resolution for the simulation
    tr : time ratio or period of the simulation (in seconds)
    stats : [None|StatsTemplate]
    scenario  : [None|ScenarioSwitch]
    params : dictinonary : "{'k':p}"
    pause : start in pause?

    """
    #modelName = sys.argv[1]
    size = eval(size)
    timeRatio = eval(tr)
    pause = eval(pause)
    dim = eval(dim)
    gui = eval(gui)
    timeEnd = eval(timeEnd)



    params = eval(params)
    kwparams = dict(size=size,dim=dim)
    kwparams.update(params)

    modelClass = getClassFromName(model, "models")
    scenarioInstance = None
    statsInstance = None
    statsName = stats
    if statsName != "None":
        statsClass = getClassFromName(statsName,'stats')
        statsInstance = statsClass(**kwparams)
    scenarioName = scenario
    if scenarioName != "None":
        scenarioClass = getClassFromName(scenarioName, 'scenarios')
        scenarioInstance = scenarioClass(**kwparams)



    #print(kwparams)
    model = modelClass(**kwparams)

    if gui:
        print(runnerView.launch(model, scenarioInstance,statsInstance, timeRatio,pause=pause,timeEnd=timeEnd))
    else:
        print(runner.launch(model, scenarioInstance,statsInstance, timeEnd=timeEnd))
