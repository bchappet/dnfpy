from map2D import Map2D

class FuncMap2D(Map2D):
    """
    This Map2D will call a function with specific keywors argument at every computation
    There are 4 way to give the keywords argument to the function:
        1) We give a dictionary with {keyword:value} on construction (the args will be unmutable)
        2) We use the self.registerOnGlobalParamsChange(dict) method 
            This method will associate a key word arg with a global parameter key {'keyWordArg':'globalRealParamsKey'}
            On registration, the values of the globalRealParams will be adderd to the self.funcArgDict dictionary
            Then on every call of method self.updateParams , this sprecific arguments will be updated
        3) We add some children. The keys of the children has to corrensond to the func key args
            The state of the children will be computed and added to self.funcArgDict  before every func call 
        4) We use self.mapAttributesToFunc which takes a dict of key args : getter of the attribute
            The state of every attribute will be accessed and added to self.funcArgDict before every func call


    """
    def __init__(self,size,dt,globalRealParams,func,funcArgDict=None):
        """TODO : the attributes globalRealParams is unused in this class"""
        super(FuncMap2D,self).__init__(size,dt,globalRealParams)
        self.func = func #function to call at every computation
        #Dictionaries to map variables with function arguments#######
        self.funcArgDict = funcArgDict or {} #values to be given to the func 
        self.paramsArgDict = {}  #set by self.registerOnGlobalParamsChange (dict funcArgs -> globalParams )
        self.attributesArgDict = {} #set by  self.mapAttributesToFunc (dict funcArgs -> getter of sel attributes)
        

    def compute(self):
        """Call the func with the good arguments"""
        super(FuncMap2D,self).compute()
        self.funcArgDict.update(self.__getAttributeArgs())
        self.funcArgDict.update(self.__getChildrenArgs())
        self.data = self.func(**self.funcArgDict)

    def __getAttributeArgs(self):
        """Because of immutable types, we cannot store references. We have to get the value at every computation
        TODO find another way"""
        newDict = dict((k,self.attributesArgDict[k]()) for k in self.attributesArgDict.keys())
        return newDict
    def __getChildrenArgs(self):
        """Return a dictionary with child name and its value"""
        newDict = dict((k,self.children[k].getData()) for k in self.children.keys())
        return newDict

    def registerOnGlobalParamsChange(self,paramsArgDict):
        """Map global arguments to the function arguments
        Update the function arguments dictionary (self.funcArgDict) directly 
        and it will be updated on self.updateParams"""
        self.paramsArgDict = paramsArgDict
        self.funcArgDict.update(FuncMap2D.__associateDict(self.paramsArgDict,self.globalRealParams))
    
    def updateParams(self,globalRealParams):
        """Update the globalRealParams and update the funcArgDict"""
        super(FuncMap2D,self).updateParams(globalRealParams)
        self.funcArgDict.update(FuncMap2D.__associateDict(self.paramsArgDict,globalRealParams))

        
    def mapAttributesToFunc(self,attributesArgDict):
        """Associate attributes getters with func args {argName : getterFunc}"""
        self.attributesArgDict = attributesArgDict

    @staticmethod
    def __associateDict(aDict,bDict):
        """Association beteween aDict and bDict:
        {aKeys -> aVals} == {bKeys -> bVals} => {aKeys -> bVals}
        """
        newDict = dict((k,bDict[aDict[k]]) for k in aDict.keys()   )
        return newDict
        


