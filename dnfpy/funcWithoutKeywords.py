from map2D import Map2D

class FuncWithoutKeywords(Map2D):
    """To use with a function taking an undifined amount of args
    It can takes only children args or a constant list"""
    def __init__(self,size,dt,globalRealParams,func,cstList=None):
        """TODO : the attributes globalRealParams is unused in this class"""
        super(FuncWithoutKeywords,self).__init__(size,dt,globalRealParams)
        self.cstList = cstList or [] #constant which will be passed to the function
        self.func = func #function to call at every computation with children

    def compute(self):
        """Call the func with the good arguments"""
        super(FuncWithoutKeywords,self).compute()
        args = self.__getChildrenArgs() + self.cstList
        self.data = self.func(*args)

    def __getChildrenArgs(self):
        """Return a list with children  value"""
        ret = [v.getData() for v in self.children.values()]
        return ret
