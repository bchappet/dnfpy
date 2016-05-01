import inspect
class Computable(object):
    """
        The Computables are object designed to compute a result
        by mapping a dictionary of arguments given on
        the construction to the set of argument expected
        by the compute method.
        The compute method is to implement

        Children class can modify the dictionary of
        argument by calling self.update(var:value,...)


    """
    def __init__(self,**kwargs):
        """
            A dict self.dictionary is constructed with **kwargs
            the inspection store the arguments expected by
            compute in self.computeArgs
        """
        self.__dictionary = dict()
        self._computeArgs = inspect.getargspec(self._compute)[0]
        self._computeArgs.remove('self')
        self._updateParamsArgs = inspect.getargspec(self._onParamsUpdate)[0]
        self._updateParamsArgs.remove('self')
        self._init_kwargs = kwargs
        #self.reset()
        self.setParams(**kwargs)

    def setArg(self,**kwargs):
        """
        Public:
            To add or change parameters in self.dictionary
        """
        self.__dictionary.update(**kwargs)
        #print("in %s, set arg %s"%(self,kwargs))

    def setParams(self,**kwargs):
        self.setArg(**kwargs)
        self.__update_params(**kwargs)

    def updateParams(self):
        """
        Recompute the params
        """
        self.__update_params(**self.__dictionary)

    def getArg(self,key):
        """
        Public:
            Access the state of an argument
        """
        return self.__dictionary[key]
    def getArgs(self,*keys):
        """
        Public:
            Return the value of the keys
        """
        try:
            ret =  [self.__dictionary[k] for k in keys]
        except Exception as e:
            print("in class %s"%self)
            raise e
        return ret

    def rmArg(self,key):
        """
        Public:
            Remove the argument given by key
            Return: True if the argument was successfully removed
        """
        try:
            del self.__dictionary[key]
            return True
        except KeyError:
            return False

    def __update_params(self,**kwargs):
        """
        Update the dictionary with modified version of the params
        stated in self._onParamsUpdate
        """
        updatedArgSet = set(self._updateParamsArgs) & kwargs.keys()
        if len(updatedArgSet) > 0:
            args = self._subDictionary(self._updateParamsArgs)
            newArgs = self._onParamsUpdate(**args)
            updatedArgs =dict()
            for k in updatedArgSet:
                try:
                    updatedArgs[k] = newArgs[k]
                except:
                    pass

            self.__dictionary.update(newArgs)
        else:
            pass

    def _onParamsUpdate(self):
        """
        Can choose the params
        To react on param update
        return a dict with new arg
        generaly the new args are hidden with _nameArg
        """
        return {}




    def _compute_with_params(self):
        """ Protected:
            call get the subdict of compute argument from
            self.dictionary and gives cal compute with it
        """
        args = self._subDictionary(self._computeArgs)
        self._compute(**args)
        self.nb_computation += 1
        self.last_computation_args = args
        self.last_computation_dictionary = self.__dictionary

    def _getDictionaryNames(self):
        """
            Protected final:
            return the set of self._dictionary names
        """
        return set(self.__dictionary.keys())


    def _subDictionary(self,keys):
        """
            Protected final:
            return the subductionary of self.__dictionary using the keys (must be itarable)
        """
        try:
            ret =  {k :self.__dictionary[k] for k in keys}
        except Exception as e:
            print("in class %s"%self)
            raise e
        return ret

    def hasArg(self,name):
        return name in self.__dictionary.keys()


    def reset(self):
        """
        Should be called with super
        Is called on construction before setParam(**kwargs)
        Hence one should only use self._init_kwargs
        """
        #Debug utilities
        self.nb_computation = 0
        self.last_computation_args = {}
        self.last_computation_dictionary = {}

    def resetParams(self):
        self.setParams(**self._init_kwargs)

    def close(self):
        pass
