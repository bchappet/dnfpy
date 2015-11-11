import numpy as np

from dnfpyUtils.stats.trajectory import Trajectory

class Derivative(Trajectory):
        """
        Input: 
            data : (children) trace
        Output:
            compute the derivative on d data /dt
        """

        def __init__(self,name,dt,**kwargs):
                super().__init__(name=name,dt=dt,**kwargs)
                self.previous = None

        def _compute(self,data,dt):

                if not(np.isnan(data)):
                    if self.previous:
                        self._data = (data - self.previous )/dt
                        self.trace.append(self._data)
                    self.previous = data




