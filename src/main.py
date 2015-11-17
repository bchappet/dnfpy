import sys
import dnfpy.controller.runnerView as runnerView
import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import begin #very usefull arg parsing library


"""
Parameter:
ModelName: str: ModelNSpike...
Scenario: str ScenarioTracking...

python3 main.py --dim 1 --lat dog --fashion fix --params "{'iExc':1.0,'wExc':2.5,'iInh':0.5,'wInh':4.0}"
"""
@begin.start
def main(model = "ModelDNF1D",size="101",dim="2",tr="0.5",stats="None",scenario="ScenarioTracking",params="{}",pause="False",gui="True",timeEnd="40.0",lat="dog",fashion='chappet'):
    """
    model : name of the model
    size : resolution for the simulation
    tr : time ratio or period of the simulation (in seconds)
    stats : [None|StatsTemplate]
    scenario  : [None|ScenarioSwitch]
    params : dictinonary : "{'k':p}"
    pause : start in pause?
    gui : bool
    timeEnd, float in second
    lat : lateralWeights function \in {'dog','doe','dol'}
    fashion : \in {chappet,fix}

    """
    #modelName = sys.argv[1]
    size = eval(size)
    timeRatio = eval(tr)
    pause = eval(pause)
    dim = eval(dim)
    gui = eval(gui)
    timeEnd = eval(timeEnd)



    params = eval(params)
    kwparams = dict(size=size,dim=dim,lateral=lat,fashion=fashion)
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
