from dnfpy.core.map2D import Map2D
import random
import sys
import numpy as np
from dnfpy.cellular.hardlib import HardLib

class BsRsdnfMap(Map2D):
        """
        Map to handle the CellBsRsdnf in hardlib.
        This  map use a standard XY routing scheme with 4 router by cell
        A spike  is interpreted as a stochastic bitstream of probability
        PARAMS{PROBA_SPIKE}.
        When "activation" is 1, a bit stream of size  PARAMS{SIZE_STREAM} will
        be initialized and generated for PARAMS{SIZE_STREAM} iteration.
        The routers have their cell spike stream as input and some other
        neighbours cell's routers (XY routage scheme)
        The router's input bitstream (4 max here) are multiplied by the synapse
        bit stream (of proba PARAMS{PROBA_SYNAPSE}) with an AND gate
        and added with OR gate

        CHILDREN NEEDED
        *"activation": an activation map with bool or int of value 0 or 1
        """
        class Params:
            PROBA_SPIKE=0
            SIZE_STREAM=1
            PRECISION_PROBA_SPIKE = 2
            NB_NEW_RANDOM_BIT = 3

        class SubParams:
            PROBA_SYNAPSE = 0
            PRECISION_PROBA = 1

        class Reg:
            SPIKE_BS=0
            NB_BIT_RECEIVED=1
            ACTIVATED=2
            NB_BIT_TO_GEN=3

        class SubReg:
            BS_OUT = 0

        def __init__(self,name,size,dt=0.1,sizeStream=20,probaSpike=1.,
                     probaSynapse=1.,
                     precisionProba=30,
                     routerType="orRouter",
                     reproductible=True,
                     errorType = 'none', #'none' | 'transient'|'permanent'
                     errorProb = 0.0001,#the error probability for every register bit
                     nstep=1,
                     **kwargs):
            self.lib = HardLib(size,size,"cellbsrsdnf","rsdnfconnecter",routerType)
            super(BsRsdnfMap,self).__init__(name=name,size=size,dt=dt,
                                           sizeStream=sizeStream,
                                            probaSpike=probaSpike,
                                            probaSynapse=probaSynapse,
                                            precisionProba=precisionProba,
                                            routerType=routerType,
                                            reproductible=reproductible,
                                            nstep=nstep,errorType=errorType,errorProb=errorProb,
                                            **kwargs)

            self.newActivation = True #true when we want to get the new activation
            self.errorBitSize = self.lib.getTotalRegSize()

        def _compute(self,size,activation,nstep,errorType,errorProb):
            if self.newActivation:
                self.setActivation(activation)
                self.newActivation = False

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
            self.setErrorMaskFromArray(bits)

        #def setErrorMaskFromArray(self,array):
        #    self.lib.setErrorMaskFromArray(array)
 
        def setErrorMaskFromArray(self,array,errorType):
            self.lib.setErrorMaskFromArray(array,errorType)


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
            self.lib.setRegArray(self.Reg.NB_BIT_RECEIVED, \
                                       np.zeros((size,size),dtype=np.intc))
            self.newActivation=True


        def reset(self):
            super(BsRsdnfMap,self).reset()
            size = self._init_kwargs['size']
            self._data = np.zeros((size,size),dtype=np.intc)
            if self.lib:
                self.lib.reset()
                self.lib.getRegArray(self.Reg.NB_BIT_RECEIVED,self._data)

        def _onParamsUpdate(self,sizeStream,probaSpike,probaSynapse,
                            precisionProba,reproductible):
            self.lib.setMapParam(self.Params.SIZE_STREAM,sizeStream)
            self.lib.setMapParam(self.Params.PROBA_SPIKE,probaSpike)
            self.lib.setMapSubParam(self.SubParams.PROBA_SYNAPSE,probaSynapse)
            self.lib.setMapParam(self.Params.PRECISION_PROBA_SPIKE,2**precisionProba-1)
            self.lib.setMapSubParam(self.SubParams.PRECISION_PROBA,2**precisionProba-1)
            if reproductible:
                self.lib.initSeed(0)
            else:
                seed = random.randint(0, 1e10)
                self.lib.initSeed(seed)
            return {}
