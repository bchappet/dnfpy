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
        name,size,dt=dt,side=side, **kwargs        
        )
        self.side = side
        
    def _compute(self, activation, simulator):

        v = self._data[0,0]

        meanP=0
        sumP=np.sum(activation)
        for i in range(activation.shape[0]):
            meanP=meanP+sensor_loc[i]*activation[i]
        if sumP==0:
            v=1 #forward velocity
        else:
            meanP = meanP/sumP   
            print("meanP",meanP)
            if self.side=='l':
                v=3/(1+np.exp(meanP*5))-1.5
            elif self.side=='r':
                v=3/(1+np.exp(-meanP*5))-1.5
        
        print("v",v)
        if self.side=='l':
            simulator.setController('ePuck_leftJoint', "motor", v)
        elif self.side=='r':
            simulator.setController('ePuck_rightJoint', "motor", v)
        
        self._data=np.array([[v]])
        
        
    def _reset(self):
        super(MotorProjection,self)._reset(
        )
        self._data=np.array([1])