import sys
import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName


"""
Parameter:
    ModelName: str: ModelNSpike...
    view: bool True,False
    Contexte: str ContexteNSpike...
    Scenario: str ScenarioTracking...


"""

if __name__ == "__main__":
    modelClass = getClassFromName(sys.argv[2],"models")
    contextClass = None
    scenarioClass = None
    size= eval(sys.argv[2])
    timeEnd= eval(sys.argv[3])
    if len(sys.argv) > 4:
        contextClass = getClassFromName(sys.argv[4],"contexts")
    if len(sys.argv) > 5:
        scenarioClass = getClassFromName(sys.argv[5],"scenrios")

    scenario = None
    context = None
    if contextClass:
        context = contextClass()

    if scenarioClass:
        scenario = scenarioClass()

    runner.launch(modelClass,context,scenario,size,timeEnd)


