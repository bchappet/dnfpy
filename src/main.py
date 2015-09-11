import sys
import dnfpy.controller.runnerView as runner
from getClassUtils import getClassFromName


"""
Parameter:
ModelName: str: ModelNSpike...
Scenario: str ScenarioTracking...


"""
if __name__ == "__main__":
    modelClass = getClassFromName(sys.argv[1], "models")
    contextClass = None
    scenarioClass = None
    size = eval(sys.argv[2])
    timeRatio = eval(sys.argv[3])
   # timeRatio = 0.3
    if len(sys.argv) > 4:
        #we put the following args in a dict to give to the model
        #except if we have scenario:'scenarioName'

        params = eval((sys.argv[4]))
        if 'scenario' in params:
            scenarioName = params['scenario']
            scenarioClass = getClassFromName(scenarioName, "scenarios")
            del params['scenario']
    else:
        params = {}

    if scenarioClass:
        scenario = scenarioClass()
    else:
        scenario = None

    kwparams = dict(size=size)
    kwparams.update(params)


    model = modelClass(**kwparams)

    runner.launch(model, scenario, timeRatio)
