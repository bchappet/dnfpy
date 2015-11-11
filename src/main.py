import sys
import dnfpy.controller.runnerView as runner
from getClassUtils import getClassFromName
import begin #very usefull arg parsing library


"""
Parameter:
ModelName: str: ModelNSpike...
Scenario: str ScenarioTracking...


"""
@begin.start
def main(model = "ModelDNF",size="101",tr="0.5",stats="None",scenario="None",params="{}",pause="False"):
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

    modelClass = getClassFromName(model, "models")
    scenarioInstance = None
    statsInstance = None
    statsName = stats
    if statsName != "None":
        statsClass = getClassFromName(statsName,'stats')
        statsInstance = statsClass()
    scenarioName = scenario
    if scenarioName != "None":
        scenarioClass = getClassFromName(scenarioName, 'scenarios')
        scenarioInstance = scenarioClass()

    params = eval(params)

    kwparams = dict(size=size)
    kwparams.update(params)


    #print(kwparams)
    model = modelClass(**kwparams)

    runner.launch(model, scenarioInstance,statsInstance, timeRatio,pause=pause)
