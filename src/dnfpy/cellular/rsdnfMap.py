from dnfpy.core.map2D import Map2D
import logging
import sys
import traceback
import random
import sys
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class RsdnfMap(Map2D):
        """
        Map to handle the CellRsdnf in hardlib.
        This  map use a standard XY routing scheme with 4 router by cell
        A spike  is interpreted as a stochastic bitstream of probability 1.

        When "activation" is 1, a bit stream of size nspike will be sent


        routerType = 
            "prng" the random number will be generated with the c rand() and precision Params{PRECISION_PROBA}
            "sequence" the random number are not generated but there are initialized for each router and then
            transmitted from router to router following the "sequence" neighbourhood
                    

        CHILDREN NEEDED
        *"activation": an activation map with bool or int of value 0 or 1
        """
        class Params:
            NB_SPIKE=0
            PROBA=1
            PRECISION_PROBA=2


        class Attributes:
            NB_BIT_RECEIVED=0
            ACTIVATED=1
            DEAD=2

        class SubBuffer:
            BUFFER = 0
            SPIKE_OUT = 1
            RANDOM_OUT = 2 #if routerType = sequence

        def __init__(self,name,size,dt=0.1,nspike=20,
                     proba=1.0,
                     precisionProba=30,
                     routerType="prng",
                     reproductible=True,
                     nstep=1,
                     **kwargs):
            print("init :",proba,nspike)
            self.lib = HardLib(size,size,"cellrsdnf","rsdnfconnecter",routerType)
            if routerType is "sequence":
                self.lib.addConnection("sequenceconnecter")
            super(RsdnfMap,self).__init__(name=name,size=size,dt=dt,dtype=np.intc,
                                           nspike=nspike,
                                            proba=proba,
                                            precisionProba=precisionProba,
                                            routerType=routerType,
                                            reproductible=reproductible,
                                            nstep=nstep,
                                            **kwargs)

            self.newActivation = True #true when we want to get the new activation

        def _compute(self,size,activation,nstep):
            if self.newActivation:
                self.newActivation = False
                self.setActivation(activation)

            self.lib.nstep(nstep)
            self.lib.getArrayAttribute(self.Attributes.NB_BIT_RECEIVED,self._data)

        def setActivation(self,activation):
            self.lib.setArrayAttribute(self.Attributes.ACTIVATED,activation)

        def setRandomSequence(self,npArrayInt):
            """
            If routerType = sequence it will initialise the random sequence
            npArrayInt must be a size*size*4 array of intc
            """
            self.lib.setArraySubState(self.SubBuffer.RANDOM_OUT,npArrayInt)
            self.lib.synch()

        def getRandomSequence(self):
            size = self.getArg('size')
            npArrayInt = np.zeros((size,size,4),dtype=np.intc)
            self.lib.getArraySubState(self.SubBuffer.RANDOM_OUT,npArrayInt)
            return npArrayInt




        def resetData(self):
            """
            Reset the  NB_BIT_RECEIVED attribute of the map cells
            whenever the neuron potential is updated by reading
            self._data, the resetData method should be called
            In a fully pipelined BsRSDNF, the neuron potential
            is updated on every bit reception, the resetData is the called
            at every computation
            """
            size = self.getArg('size')
            zeros = np.zeros((size,size,4),dtype=np.intc)
            self.lib.setArrayAttribute(self.Attributes.NB_BIT_RECEIVED, \
                                       np.zeros((size,size),dtype=np.bool))
            #reset buffer
            self.lib.setArraySubState(self.SubBuffer.BUFFER,zeros)
            self.lib.setArraySubState(self.SubBuffer.SPIKE_OUT,zeros)
            self.lib.synch()
            self.newActivation=True


        def reset(self):
            if self.lib:
                print("reset",self.getName())
                #logging.exception("Something awful happened!")
                self.lib.reset()
            super(RsdnfMap,self).reset()

        def _onParamsUpdate(self,nspike,proba,
                            precisionProba,reproductible,size,routerType):
            print("param update :",proba,nspike)
            self.lib.setMapParam(self.Params.NB_SPIKE,nspike)
            self.lib.setMapParam(self.Params.PROBA,proba)
            self.lib.setMapParam(self.Params.PRECISION_PROBA,2**precisionProba-1)
            if reproductible:
                self.lib.initSeed(0)
            else:
                seed = random.randint(0, sys.maxint)
                self.lib.initSeed(seed)
            
            if routerType is 'sequence':
                randomSequence = (np.random.random((size,size,4)) <= proba).astype(np.intc)
                self.setRandomSequence(randomSequence)
                randomSequence2 = self.getRandomSequence()
                assert(np.array_equal(randomSequence,randomSequence2))



                


            return {}
