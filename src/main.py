import sys
import math
import dnfpy.controller.runnerView as runnerView
import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import begin #very usefull arg parsing library

#defaultScenario = "ScenarioTracking"
defaultScenario = "WM1" 
#defaultScenario = "WorkingMemoryShift"
defaultModel = "ModelBsRsdnf"
defaultStats = "StatsTracking2"
#defaultStats = "None"


"""
Parameter:
ModelName: str: ModelNSpike...
Scenario: str ScenarioTracking...

"""
@begin.start
def main(model = defaultModel,size="49",dim="2",tr="0.5",stats=defaultStats,scenario=defaultScenario,params="{}",pause="False",gui="True",timeEnd="400000000",lat="dog",fashion='chappet',dt='0.1',procTime='1e10',save='False',saveMapDict="{}"):
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
    procTime : time allowed on processor in second
    save : if true will save maps at the end of the simulation

    """
    #modelName = sys.argv[1]
    timeRatio = eval(tr)
    pause = eval(pause)
    gui = eval(gui)
    timeEnd = eval(timeEnd)
    dt = eval(dt)
    dim = eval(dim)
    size = eval(size)
    size = int(((math.floor(size/2.)) * 2) + 1)#Ensure size is odd for convolution
    allowedTime = eval(procTime)
    save = eval(save)
    saveMapDict = eval(saveMapDict)



    params = eval(params)
    kwparams = dict(size=size,dim=dim,lateral=lat,fashion=fashion,dt=dt)
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
        print(runnerView.launch(model, scenarioInstance,statsInstance, timeRatio,
            pause=pause,timeEnd=timeEnd,save=save,saveMapDict=saveMapDict))
    else:
        print(runner.launch(model, scenarioInstance,statsInstance, timeEnd=timeEnd,
            allowedTime=allowedTime,save=save,saveMapDict=saveMapDict))
