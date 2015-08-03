from dnfpy.core.map2D import Map2D

import numpy as np
from math import PI

sensor_loc=np.array([-PI/2, -50/180.0*PI,-30/180.0*PI,-10/180.0*PI,10/180.0*PI,30/180.0*PI,50/180.0*PI,PI/2,PI/2,130/180.0*PI,150/180.0*PI,170/180.0*PI,-170/180.0*PI,-150/180.0*PI,-130/180.0*PI,-PI/2])     


class ObstacleAvoidanceBehaviour(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
    #orientation of all the sensors: 
    
    def __init__(self, name, size, dt, **kwargs):
        super(ObstacleAvoidanceBehaviour,self).__init__(
        name,size,dt=dt,**kwargs        
        )

        
    def _compute(self, irSensors, simulator):
        
        vL = self._data[0]
        vR = self._data[1]
        
        
        
        sensor_sq=irSensors[0:8]*irSensors[0:8]
        
        min_ind=np.where(sensor_sq==np.min(sensor_sq))
        min_ind=min_ind[0][0]
        
        if sensor_sq[min_ind]<0.002:
            steer=-1/sensor_loc[min_ind]
        else:
            steer=0
        
        v=1	#forward velocity
        kp=0.5	#steering gain
        vL=v+kp*steer
        vR=v-kp*steer
    
        simulator.setController('ePuck_leftJoint', "motor", vL)
        simulator.setController('ePuck_rightJoint', "motor", vR)
        
        self._data=np.array([vL, vR])
        
        
    def _reset(self):
        super(ObstacleAvoidanceBehaviour,self)._reset(
        )
        self._data=np.array([1, 1])