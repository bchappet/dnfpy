import unittest
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
        self.dictionary = dict(**kwargs)
        self.computeArgs = inspect.getargspec(self.compute)[0]
        self.computeArgs.remove('self')

    def _setArg(self,**kwargs):
        """
            Protected:
            To add or change parameters in self.dictionary
        """
        self.dictionary.update(**kwargs)

    def _compute_with_params(self):
        """ Protected:
            call get the subdict of compute argument from 
            self.dictionary and gives cal compute with it
        """
        args = self.__paramsToExpectedArgs(self.dictionary,self.computeArgs)
        self.compute(**args)

    def __paramsToExpectedArgs(self,dictionary,keyList):
        return {k : self.dictionary[k] for k in keyList}


