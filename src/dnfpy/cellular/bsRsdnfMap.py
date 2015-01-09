from dnfpy.core.map2D import Map2D
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
            PROBA_SYNAPSE=2

        class Registers:
            SPIKE_BS=0

        class Attributes:
            NB_BIT_RECEIVED=0
            ACTIVATED=1
            DEAD=2

        def __init__(self,name,size,dt=0.1,sizeStream=20,probaSpike=1.,
                     probaSynapse=1.,**kwargs):
            self.lib = HardLib(size,size,"cellbsrsdnf","rsdnfconnecter")
            super(BsRsdnfMap,self).__init__(name=name,size=size,dt=dt,
                                           sizeStream=sizeStream,
                                            probaSpike=probaSpike,
                                            probaSynapse=probaSynapse,
                                            **kwargs)

        def _compute(self,size,activation):
            self.lib.setArrayAttribute(self.Attributes.ACTIVATED,activation)
            self.lib.step()
            self.lib.synch()
            self.lib.getArrayAttribute(self.Attributes.NB_BIT_RECEIVED,self._data)

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
            self.lib.setArrayAttribute(self.Attributes.NB_BIT_RECEIVED, \
                                       np.zeros((size,size),dtype=np.bool))


        def reset(self):
            size = self.getArg('size')
            self._data = np.zeros((size,size),dtype=np.intc)
            if self.lib:
                self.lib.reset()
                self.lib.getArrayAttribute(self.Attributes.NB_BIT_RECEIVED
                                           ,self._data)

        def _onParamsUpdate(self,sizeStream,probaSpike,probaSynapse):
            self.lib.setMapParam(self.Params.SIZE_STREAM,sizeStream)
            self.lib.setMapParam(self.Params.PROBA_SPIKE,probaSpike)
            self.lib.setMapParam(self.Params.PROBA_SYNAPSE,probaSynapse)
            return {}
