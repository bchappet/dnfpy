"""
Lauch PSO with parameters and write result in OUT in csv:

python3 lauchPSO.py PSOClass PSOParamsDict Model Scenario ConstantParamsDict nbEvalMax 


the output is in the format

evaluation#,fitness,bestIndX0,x1,x2 ...
"""




from getClassUtils import getClassFromName
import begin



@begin.start
def main(pso="PsoDNFTemplate",meta="{'omega':0.9,'phiP':1.2,'phiG':1.2}",model="ModelDNFSpace",scenario="Competition",params="{'size':49,'model':'cnft','activation':'step','dim':1}" ,nbEval="10000",swarmSize="100",nbThread="8",verbose="False",lateral="dog",objective='0'):


    psoClass = getClassFromName(pso, "optimisation")
    metaDict = eval(meta)
    modelClass = getClassFromName(model,"models")
    scenarioClass = getClassFromName(scenario,"scenarios")
    paramsDict = eval(params)
    nbEval = eval(nbEval)
    swarmSize = eval(swarmSize)
    nbThread = eval(nbThread)
    verbose = eval(verbose)
    objective = eval(objective)


    paramsDict.update({'lateral':lateral})


    if verbose:
        print("lauching ",pso," with params ", metaDict, "on model ",modelClass, " with cst params ",paramsDict)
        print("scenario : ",scenarioClass)

    pso = psoClass(swarmSize=swarmSize,nbEvaluationMax=nbEval,nbThread=nbThread,verbose=verbose,objective=objective,**metaDict) 

    pso.setModelClass(modelClass)
    pso.setConstantParamsDict(paramsDict)
    pso.setScenarioClass(scenarioClass)


    pso.run()

    


