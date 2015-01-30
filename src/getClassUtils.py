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


