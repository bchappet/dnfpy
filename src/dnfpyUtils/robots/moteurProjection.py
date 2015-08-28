from dnfpy.core.map2D import Map2D

import numpy as np
import math

PI=math.pi
#orientation of all the sensors: 
sensor_loc=np.array([-PI/2,-PI/2+0.385,-PI/2+0.77,-PI/2+1.02,-PI/2+1.27, PI/2-1.27, PI/2-0.77, PI/2,])     


class MotorProjection(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
    
    def __init__(self, name, size=1, dt=0.1, side='r', **kwargs):
        super(MotorProjection,self).__init__(
        name,size,dt=dt,side=side, **kwargs        
        )
        self.side = side
        
    def _compute(self, activationN, activationI):

        #v = self._data[0,0]
        if self.side=='l':
            a=-1
        else:
            a=1
            
            
        sumIP=np.sum(activationI)
        sumNP=np.sum(activationN)
        x=np.linspace(-PI,PI,activationN.shape[0])
        
        
        #sumDP=np.sum(activationD)
        fD=2/(1+np.exp(a*x))-0.5
        fO=2/(1+np.exp(-a*x*10))-1
        if(sumIP+sumNP != 0): 
            v=(np.sum(fD*activationN)+np.sum(fO*activationI))/(sumIP+sumNP)
        else:
            v=0

        
        
        
        """
        sum
        for i in range(activationI.shape[0]):
            meanIP=meanIP+activationI[i]*math.pi*(-activationI.shape[0]+1+2*i)/(activationI.shape[0])
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
                
    
        
        if self.side=='l':
            simulator.setController('ePuck_leftJoint', "motor", v)
        elif self.side=='r':
            simulator.setController('ePuck_rightJoint', "motor", v)
            
        """
        self._data=np.array([[v]])
        
    
        
    def _reset(self):
        super(MotorProjection,self)._reset(
        )
        self._data=np.array([1])
