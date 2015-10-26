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
def main(model = "ModelDNF",size="101",tr="0.3",stats="None",params="{}"):
    """
    model : name of the model
    size : resolution for the simulation
    tr : time ratio or period of the simulation (in seconds)
    stats : [None|StatsTemplate]
    params : dictinonary : "{'k':p}"

    """
    #modelName = sys.argv[1]
    size = eval(size)
    timeRatio = eval(tr)

    modelClass = getClassFromName(model, "models")
    contextClass = None
    scenarioClass = None
    statsClass = None
    statsName = stats
    if statsName != "None":
            statsClass = getClassFromName(statsName,'stats')
   # timeRatio = 0.3
    #if len(sys.argv) > 4:
        #we put the following args in a dict to give to the model
        #except if we have scenario:'scenarioName'

     #   params = eval((sys.argv[4]))
    params = eval(params)
    if 'scenario' in params:
            scenarioName = params['scenario']
            scenarioClass = getClassFromName(scenarioName, 'scenarios')
            del params['scenario']

    if scenarioClass:
        scenario = scenarioClass()
    else:
        scenario = None

    if statsClass:
        stats = statsClass()
    else:
        stats = None

    kwparams = dict(size=size)
    kwparams.update(params)


    print(kwparams)
    model = modelClass(**kwparams)

    runner.launch(model, scenario,stats, timeRatio)
