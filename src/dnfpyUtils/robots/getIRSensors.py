from dnfpy.core.map2D import Map2D

import numpy as np

class GetIRSensors(Map2D):
    """
    Get IR sensors from a robot simulator
    """
    
    def __init__(self, name, size, dt, **kwargs):
        super(GetIRSensors,self).__init__(
        name,size,dt=dt,**kwargs        
        )
        
    def _compute(self, simulator):
        listname=np.array([])        
        for x in range(1,8):
            listname=np.append(listname,"ePuck_proxSensor"+str(x))
            
            
        sensors_data=simulator.getSensors(listname,"prox")
        print(sensors_data)
        self._data=sensors_data
    