from dnfpy.core.map2D import Map2D

import numpy as np
import math

PI=math.pi
#orientation of all the sensors: 
sensor_loc=np.array([-PI/2,-PI/2+0.77,-PI/2+1.27, PI/2-1.27, PI/2-0.77, PI/2,])     


class MotorProjection(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
    
    def __init__(self, name, size=1, dt=0.1, side='r', **kwargs):
        super(MotorProjection,self).__init__(
        name,size,dt=dt,side=side, **kwargs        
        )
        self.side = side
        
    def _compute(self, activationI, activationD, simulator):

        v = self._data[0,0]

        meanIP=0
        sumIP=np.sum(activationI)
        sum
        for i in range(activationI.shape[0]):
            meanIP=meanIP+sensor_loc[i]*activationI[i]
        if sumIP==0:
            meanDP=0
            print("taille activationD",activationD.shape[0])
            print("activationD",activationD)
            for i in range(activationD.shape[0]):
                meanDP=meanDP+activationD[i]*math.pi*(-activationD.shape[0]+1+2*i)/(activationD.shape[0])
            sumDP=np.sum(activationD)
            if sumDP==0:
                v=1
            else:
                meanDP = meanDP/sumDP
                print("meanDP",meanDP)
                if self.side=='l':
                    v=3/(1+np.exp(-meanDP))
                if self.side=='r':
                    v=3/(1+np.exp(meanDP))
        else:
            meanIP = meanIP/sumIP   
            print("meanIP",meanIP)
            if self.side=='l':
                v=3/(1+np.exp(meanIP*5))-1.5
            elif self.side=='r':
                v=3/(1+np.exp(-meanIP*5))-1.5
        
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