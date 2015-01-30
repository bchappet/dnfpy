import sys
import dnfpy.controller.runnerView as runner
from getClassUtils import getClassFromName


"""
Parameter:
ModelName: str: ModelNSpike...
Contexte: str ContexteNSpike...
Scenario: str ScenarioTracking...


"""
if __name__ == "__main__":
    modelClass = getClassFromName(sys.argv[1], "models")
    contextClass = None
    scenarioClass = None
    size = eval(sys.argv[2])
    if len(sys.argv) > 3:
        timeRatio = eval(sys.argv[3])
    else:
        timeRatio = 0.3
    if len(sys.argv) > 4:
        if sys.argv[4] != "None":
            contextClass = getClassFromName(sys.argv[4], "contexts")
        if len(sys.argv) > 5:
            scenarioClass = getClassFromName(sys.argv[5], "scenarios")
    scenario = None
    context = None
    if contextClass:
            context = contextClass()

    if scenarioClass:
        scenario = scenarioClass()

    model = modelClass(size=size)

    runner.launch(model, context, scenario, timeRatio)
