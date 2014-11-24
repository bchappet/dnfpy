import unittest
import copy
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
        self.__dictionary = dict(**kwargs)
        self._computeArgs = inspect.getargspec(self._compute)[0]
        self._computeArgs.remove('self')
        #Debug utilities
        self.nb_computation = 0
        self.last_computation_args = {}
        self.last_computation_dictionary = {}

    def _setArg(self,**kwargs):
        """
            Protected:
            To add or change parameters in self.dictionary
        """
        self.__dictionary.update(**kwargs)

    def _getArg(self,key):
        """
            Protected:
            Access the state of an argument
        """
        return self.__dictionary[key]
    def _getArgs(self,*keys):
        """
            Protected:
            Return a subDictionary of self.__dictionary
        """
        return self._subDictionary(self.__dictionary,list(*keys))

    def _rmArg(self,key):
        """
            Protected, Final
            Remove the argument given by key
            Return: True if the argument was successfully removed
        """
        try:
            del self.__dictionary[key]
            return True
        except KeyError:
            return False

               

    def _compute_with_params(self):
        """ Protected:
            call get the subdict of compute argument from 
            self.dictionary and gives cal compute with it
        """
        args = self._subDictionary(self.__dictionary,self._computeArgs)
        self._compute(**args)
        self.nb_computation += 1
        self.last_computation_args = args
        self.last_computation_dictionary = self.__dictionary
    def _getDictionaryNames(self):
        """
            Protected final:
            return the set of self._dictionary names
        """
        return set(self.__dictionary.viewkeys())
            

    @staticmethod
    def _subDictionary(dictio,keyList):
        return {k : dictio[k] for k in keyList}


