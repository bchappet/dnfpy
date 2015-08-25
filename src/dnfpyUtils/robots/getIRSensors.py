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
        self.sensors_loc=np.array([])
        self.listname=np.array([])
        
        if nbSensors>6:
            self.dec=0
        else:
            self.dec=int((6-nbSensors)/2)
        
        for x in range(1+self.dec,nbSensors+1+self.dec):
            self.listname=np.append(self.listname,"ePuck_proxSensor"+str(x))
            
        
        for i in range(nbSensors):
            angle=-PI/2-i*2*PI/nbSensors
            if angle>-PI:
                pass
                #print("1er angle "+str(i+1),angle)
            elif angle<-2*PI:
                angle=angle+2*PI
                #print("2eme angle "+str(i+1),angle)
            else:
                angle=PI+(angle+PI)
                #print("3eme angle "+str(i+1),angle)
            
                
            self.sensors_loc=np.append(self.sensors_loc,angle)


    def _compute(self, simulator, size, nbSensors):
        self.compute2(simulator, size, nbSensors)

    @profile
    def compute2(self, simulator, size, nbSensors):
        
            
        sensors_data=simulator.getSensors(self.listname,"prox")
        #print("sensors_data", sensors_data)


        
        
        sensors_dataN = np.zeros((size))

        for i in range(nbSensors):
            if sensors_data[i]>0 and self.sensors_loc[i]>-PI/2 and self.sensors_loc[i]<PI/2:
                indice=int((self.sensors_loc[i+self.dec]+math.pi)*size/(2*math.pi))
                sensors_dataN[indice]=sensors_data[i]
        

        
        
        self._data=sensors_dataN
