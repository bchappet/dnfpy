import numpy as np


from dnfpyUtils.stats.trajectory import Trajectory

class MovingAverage(Trajectory):
        """
        Input: 
            data : (children) trace
            windowSize : (constructor) in seconds. 
        Output:
            compute the average on  data(t-windowSize) - data(t) 
        """
        def __init__(self,name,dt,windowSize,**kwargs):
                super().__init__(name=name,dt=dt,windowSize=windowSize,**kwargs)
                self.dataSave = []
                self.save = []
                self.mean = np.nan
                
                

        def _compute(self,data,windowSize,dt):
                nbData = windowSize/dt #len of array dataSave

                if not(np.isnan(data)):
                    self.dataSave.append(data)

                #make sure dataSave has the right size
                while len(self.dataSave) > nbData:
                        self.dataSave.pop(0)


                self._data = np.nanmean(self.dataSave)
                self.trace.append(self._data)




        




