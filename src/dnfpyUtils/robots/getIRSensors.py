from dnfpy.core.mapND import MapND
import math
import numpy as np
from math import pi as PI
sensor_loc=np.array([-PI/2,-PI/2+0.77,-PI/2+1.27, PI/2-1.27, PI/2-0.77, PI/2,PI-(5.21-3*PI/2), -PI+(3*PI/2-4.21)]) 

class GetIRSensors(MapND):
    """
    Get IR sensors from a robot simulator
    """
    
    def __init__(self, name, size=8, dt=0.1, nbSensors=6, **kwargs):
        super(GetIRSensors,self).__init__(
        name,size,dt=dt,nbSensors=nbSensors,**kwargs        
        )
        


    def _compute(self, simulator, size, nbSensors):
        self.compute2(simulator, size, nbSensors)

    #@profile
    def compute2(self, simulator, size, nbSensors):
        listname=np.array([])
        if nbSensors>6:
            dec=0
        else:
            dec=int((6-nbSensors)/2)
            
        for x in range(1+dec,nbSensors+1+dec):
            listname=np.append(listname,"ePuck_proxSensor"+str(x))
            
            
        sensors_data=simulator.getSensors(listname,"prox")
        #print("sensors_data", sensors_data)
        
        sensors_orientation=np.array([])
        for name in listname:
            sensors_orientation=np.append(sensors_orientation,simulator.getOrientation(name,"ePuck"))
        print("sensors_orientation",sensors_orientation)
        
        sensors_dataN = np.zeros((size))

        for i in range(nbSensors):
            if sensors_data[i]>0:
                indice=int((sensor_loc[i+dec]+math.pi)*size/(2*math.pi))
                sensors_dataN[indice]=sensors_data[i]
        

        
        
        self._data=sensors_dataN
