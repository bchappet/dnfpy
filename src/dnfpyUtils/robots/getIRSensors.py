from dnfpy.core.map2D import Map2D

import numpy as np

class GetIRSensors(Map2D):
    """
    Get IR sensors from a robot simulator
    """
    
    def __init__(self, name, size=8, dt=0.1, **kwargs):
        super(GetIRSensors,self).__init__(
        name,size,dt=dt,**kwargs        
        )
        
    def _compute(self, simulator, size):
        listname=np.array([])        
        for x in range(1,size+1):
            listname=np.append(listname,"ePuck_proxSensor"+str(x))
            
            
        sensors_data=simulator.getSensors(listname,"prox")
        print("sensors_data", sensors_data)
        self._data=sensors_data.reshape((1,size))
    