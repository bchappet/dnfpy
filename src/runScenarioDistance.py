import dnfpy.controller.runner as runner
from getClassUtils import getClassFromName
import sys
import numpy as np

parameterDictModel = {'size':101}



modelClass = getClassFromName("ModelEPuckDNF","models")
scenarioClass = getClassFromName("ScenarioEpuckDistance","scenarios")


model = modelClass(**parameterDictModel)

tabDist=np.array([])
tabDpdt=np.array([])
for i in range(60,120,5):
    dist=float(i)/1000
    
    parameterDictScenario = {'dist':dist}
    scenario = scenarioClass(**parameterDictScenario)
    
    for i in range(2):
        res = runner.launch(model,scenario,20)
        print("res",res)
        tabDist=np.append(tabDist,res[0])
        tabDpdt=np.append(tabDpdt,res[1])
    
    

print("tabDist",tabDist)
print("tabDpdt",tabDpdt)

    
    