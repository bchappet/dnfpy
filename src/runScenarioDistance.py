import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import sys
import numpy as np

parameterDictModel = {'size':101}



modelClass = getClassFromName("ModelEPuckDNF","models")
scenarioClass = getClassFromName("ScenarioEpuckDistance","scenarios")


model = modelClass(**parameterDictModel)

tab=np.array([])
for i in range(6,12):
    dist=float(i)/100
    
    parameterDictScenario = {'dist':dist}
    scenario = scenarioClass(**parameterDictScenario)

    res = runner.launch(model,scenario,20)
    print("res",res)
    tab=np.append(tab,res)

print("tab",tab)
    
    