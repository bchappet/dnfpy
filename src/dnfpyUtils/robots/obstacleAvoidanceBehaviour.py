from dnfpy.core.map2D import Map2D

import numpy as np
import math

PI=math.pi
#orientation of all the sensors:
sensor_loc=np.array([-PI/2,-PI/2+0.77,-PI/2+1.27, PI/2-1.27, PI/2-0.77, PI/2,])     


class ObstacleAvoidanceBehaviour(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
     
    
    def __init__(self, name, size=2, dt=0.1, **kwargs):
        super(ObstacleAvoidanceBehaviour,self).__init__(
        name,size,dt=dt,**kwargs        
        )

        
    def _compute(self, irSensors, simulator):
        
        vL = self._data[0,0]
        vR = self._data[0,1]
        
        
        
        sensor_sq=irSensors[0,0:6]*irSensors[0,0:6]
        #sensor_sq=sensor_sq.reshape((1,8))
        max_ind=np.argmax(sensor_sq)
        print("ssq",sensor_sq)
        print("max_ind ",max_ind)
        print("ssqm ",sensor_sq[max_ind])
        if (sensor_sq[max_ind]>0):
            steer=-1/sensor_loc[max_ind]
        else:
            steer=0
        
        print("steer",steer)
        v=1	#forward velocity
        kp=0.5	#steering gain
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