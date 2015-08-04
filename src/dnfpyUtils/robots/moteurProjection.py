from dnfpy.core.map2D import Map2D

import numpy as np
import math

PI=math.pi

sensor_loc=np.array([-PI/2,-PI/2+0.77,-PI/2+1.27, PI/2-1.27, PI/2-0.77, PI/2,])     


class MotorProjection(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
    #orientation of all the sensors: 
    
    def __init__(self, name, size=1, dt=0.1, side='r', **kwargs):
        super(MotorProjection,self).__init__(
        name,size,dt=dt,side=side**kwargs        
        )
        self.side = side
        
    def _compute(self, activation, simulator):

        v = self._data[0,0]

        meanP=(-activation[0]*5-activation[1]*3-activation[2]+activation[3]+activation[4]*3+activation[5]*5)/6
        print("meanP",smeanP)
        if np.sum(activation)<0.5:
            v=1 #forward velocity
        else:
            
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