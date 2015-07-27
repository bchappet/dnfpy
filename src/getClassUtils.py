import importlib
def getClassFromName(className, path):
    """
    return a class given the class Name
    """
    path = "dnfpyUtils." + path + "."
    modelName = className
    moduleName = modelName[0].lower() + modelName[1:]
    module = importlib.import_module(path+moduleName)
    clazz = getattr(module, modelName)
    return clazz

def getFunctionFromName(fileName,funcName,path):
    """
    return a function in the specified file and path
    """
    path = "dnfpyUtils." + path + "."
    module = importlib.import_module(path+fileName)
    func = getattr(module,funcName)
    return func




