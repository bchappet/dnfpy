from map2D import Map2D


class FuncMap2D(Map2D):
    """On compute, the func will be called
    The arguments are the set of the funcarg:rParam name dictionary and the children names
    TODO maybe put a dictionary to associate funcarg with child name
    The children argument are pritoritary on the global arguments
    """
    def __init__(self,size,dt,globalRealParams,func,argNamesDict):
        """TODO : the attributes globalRealParams is unused in this class"""
        super(FuncMap2D,self).__init__(size,dt,globalRealParams)
        self.func = func #function to call at every computation
        
        #Dictionaries to map variables with function arguments#######
        #globalRealParams mapping
        self.argNamesDict = argNamesDict 
        #attributes getters to func arg mapping (Optional to set with mapAttributesToFunc after construction)
        self.attributesArgDict = {} 
        #the last one is children also optional
        #self.children = {} (see super)
        #Finaly we concatenate theses dictionary with this method
        self.__updateFuncArgs(globalRealParams)
        #############################################################
        

    def compute(self):
        """Call the func with the good arguments"""
        super(FuncMap2D,self).compute()
        self.funcargs.update(self.__getAttributeArgs())
        self.funcargs.update(self.__getChildrenArgs())
        self.data = self.func(**self.funcargs)

    def __getAttributeArgs(self):
        """Because of immutable type, we cannot store ref. We have to get the value at every computation
        TODO find another way"""
        newDict = dict((k,self.attributesArgDict[k]()) for k in self.attributesArgDict.keys())
        return newDict
    def __getChildrenArgs(self):
        """Return a dictionary with child name and its value"""
        newDict = dict((k,self.children[k].getData()) for k in self.children.keys())
        return newDict

        
    def addChildren(self,childrenToAdd):
        """Add the children and add them to the argNameDict"""
        super(FuncMap2D,self).addChildren(childrenToAdd)
        #self.funcargs.update(childrenToAdd)
        return None

    @staticmethod
    def __associateDict(aDict,bDict):
        """Association beteween aDict and bDict:
        {aKeys -> aVals} == {bKeys -> bVals} => {aKeys -> bVals}
        """
        newDict = dict((k,bDict[aDict[k]]) for k in aDict.keys()   )
        return newDict
    
    def updateParams(self,globalRealParams):
        """Update the globalRealParams and update the funcargs"""
        super(FuncMap2D,self).updateParams(globalRealParams)
        self.__updateFuncArgs(globalRealParams)
    
    
    def __updateFuncArgs(self,globalRealParams):
        """Update funcArgs on globalRealParams change"""
        self.funcargs = FuncMap2D.__associateDict(self.argNamesDict,globalRealParams)
        #self.funcargs.update(self.children)
        #self.funcargs.update(self.attributesArgDict)
        
    def mapAttributesToFunc(self,attributesArgDict):
        """Associate attributes getters with func args {argName : getterFunc}"""
        self.attributesArgDict = attributesArgDict
        #self.funcargs.update(self.attributesArgDict)

        

