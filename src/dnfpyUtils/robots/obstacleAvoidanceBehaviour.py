from dnfpy.core.map2D import Map2D

import numpy as np
import math

PI=math.pi

sensor_loc=np.array([PI/2-1.27, PI/2-0.77,PI/2,PI/2+1.05,-PI/2-1.05, -PI/2, -PI/2+0.77, -PI/2+1.27])     


class ObstacleAvoidanceBehaviour(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
    #orientation of all the sensors: 
    
    def __init__(self, name, size=2, dt=0.1, **kwargs):
        super(ObstacleAvoidanceBehaviour,self).__init__(
        name,size,dt=dt,**kwargs        
        )

        
    def _compute(self, irSensors, simulator):
        
        vL = self._data[0,0]
        vR = self._data[0,1]
        
        
        
        sensor_sq=irSensors[0,0:8]*irSensors[0,0:8]
        #sensor_sq=sensor_sq.reshape((1,8))
        min_ind=np.argmin(sensor_sq)
        print("ssq",sensor_sq)
        print("min_ind ",min_ind)
        print("ssqm ",sensor_sq[min_ind])
        if (sensor_sq[min_ind]<0.002):
            steer=-1/sensor_loc[min_ind]
        else:
            steer=0
        
        v=1	#forward velocity
        kp=1	#steering gain
        vL=v+kp*steer
        vR=v-kp*steer
        print("vl",vL)
        simulator.setController('ePuck_leftJoint', "motor", vL)
        simulator.setController('ePuck_rightJoint', "motor", vR)
        
        self._data=np.array([[vL, vR]])
        
        
    def _reset(self):
        super(ObstacleAvoidanceBehaviour,self)._reset(
        )
        self._data=np.array([1, 1])