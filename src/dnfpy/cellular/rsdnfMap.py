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

        class SubParams:
            PROBA=0
            PRECISION_PROBA=1


        class Reg:
            ACTIVATED=0
            NB_BIT_RECEIVED=1

        class SubReg:
            BUFFER = 0
            SPIKE_OUT = 1
            RANDOM_OUT = 2 #if routerType = sequence
        
        def __init__(self,name,size,dt=0.1,nspike=20,
                     proba=1.0,
                     precisionProba=31,
                     routerType="prng", #sequence|sequenceShort|sequenceMixte|sequenceShortMixte
                     reproductible=True,
                     errorType = 'none', #'none' | 'transient'|'permanent_high'|'permanent_low'
                     errorProb = 0.0001,#the error probability for every register bit
                     **kwargs):
            self.lib = HardLib(size,size,"cellrsdnf","rsdnfconnecter",routerType)
            if routerType == "sequence" or routerType == "sequenceMixte":
                self.lib.addConnection("sequenceconnecter",wrap=True)
            elif routerType == "sequenceShortMixte" or routerType == "sequenceShort":
                self.lib.addConnection("sequenceconnecterShort",wrap=True)
            elif routerType != 'prng':
                print("unknown router" + routerType)
                sys.exit(-1)
            super().__init__(name=name,size=size,dt=dt,dtype=np.intc,
                                           nspike=nspike,
                                            proba=proba,
                                            precisionProba=precisionProba,
                                            routerType=routerType,
                                            reproductible=reproductible,
                                            errorType=errorType,
                                            errorProb = errorProb,
                                            **kwargs)

            self.newActivation = True #true when we want to get the new activation
            self.errorBitSize = self.lib.getTotalRegSize()
            self.errorType = errorType
            if errorType == 'permanent_high' or errorType == 'permanent_low':
                self.setFaults(errorProb)

        def _compute(self,size,activation,errorType,errorProb):
            self._compute2(size,activation,errorType,errorProb)

        def _compute2(self,size,activation,errorType,errorProb):
            if self.newActivation:
                self.newActivation = False
                self.setActivation(activation)

            if errorType == 'transient':
                self.setFaults(errorProb)

            self.lib.nstep(1)
            self.lib.getRegArray(self.Reg.NB_BIT_RECEIVED,self._data)

        def setActivation(self,activation):
            self.lib.setRegArray(self.Reg.ACTIVATED,activation)
            self.lib.synch()

        def setFaults(self,errorProb):
            bits = np.random.random((self.errorBitSize)) < errorProb
            print("nb fault = ",np.sum(bits))
            self.setErrorMaskFromArray(bits,self.errorType)

        def setErrorMaskFromArray(self,array,errorType):
            self.lib.setErrorMaskFromArray(array,errorType)
            

        def setRandomSequence(self,npArrayInt):
            """
            If routerType = sequence it will initialise the random sequence
            npArrayInt must be a size*size*4 array of intc
            """
            self.lib.setArraySubState(self.SubReg.RANDOM_OUT,npArrayInt)
            self.lib.synch()

        def getRandomSequence(self):
            size = self.getArg('size')
            npArrayInt = np.zeros((size,size,4),dtype=np.intc)
            self.lib.getArraySubState(self.SubReg.RANDOM_OUT,npArrayInt)
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
            self.lib.setRegArray(self.Reg.NB_BIT_RECEIVED, \
                                       np.zeros((size,size),dtype=np.intc))
            #reset buffer
            self.lib.setArraySubState(self.SubReg.BUFFER,zeros)
            self.lib.setArraySubState(self.SubReg.SPIKE_OUT,zeros)
            self.lib.synch()
            self.newActivation=True


        def reset(self):
            if self.lib:
                self.lib.reset()
            super().reset()

            self.errorBitSize = self.lib.getTotalRegSize()
            if self.getArg('errorType') == 'permanent':
                self.setFaults(self.getArg('errorProb'),self.routerType)

        def _onParamsUpdate(self,nspike,proba,
                            precisionProba,reproductible,size,routerType):
            self.lib.setMapParam(self.Params.NB_SPIKE,nspike)
            self.lib.setMapSubParam(self.SubParams.PROBA,proba)
            self.lib.setMapSubParam(self.SubParams.PRECISION_PROBA,2**precisionProba-1)
            if reproductible:
                self.lib.initSeed(0)
            else:
                self.lib.initSeed(random.randrange(0,1e9))
            
            if routerType == 'sequence' or routerType == "sequenceShort" or routerType == "sequenceMixte" or routerType == "sequenceShortMixte":
                #TODO reproducible!!!
                randomSequence = (np.random.random((size,size,4)) <= proba).astype(np.intc)
                self.setRandomSequence(randomSequence)



                


            return {}

if __name__ == "__main__":
    size = 100
    activation = np.zeros( ( size,size),np.intc)
    uut = RsdnfMap("uut",size,activation=activation)
    uut.reset()
    activation[size//2,size//2] = 1
    uut.setParams(pExc=1,pInh=1,nspike=20)
    activation[size//2-5:size//2+5,size//2-5:size//2+5] = 1
    uut.setParams(nspike=20)

    for i in range(100*20 + 200):
        uut.compute()
    data = uut.getData()
    assert(np.sum(data)==100*100*100*20 - 100*20)


