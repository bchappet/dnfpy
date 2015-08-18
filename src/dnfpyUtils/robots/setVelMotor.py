from dnfpy.core.map2D import Map2D

import numpy as np



class SetVelMotor(Map2D):
    """
    Set motor to avoid obstacle in a robot simulator
    """
    
    def __init__(self, name, size=1, dt=0.1, side='r', **kwargs):
        super(SetVelMotor,self).__init__(
        name,size,dt=dt,side=side, **kwargs        
        )
        self.side = side
        
    def _compute(self, motor, simulator):

        v = motor
        
        
        if self.side=='l':
            simulator.setController('ePuck_leftJoint', "motor", v)
        elif self.side=='r':
            simulator.setController('ePuck_rightJoint', "motor", v)
        
        self._data=np.array([[v]])
        
        
    def _reset(self):
        super(SetVelMotor,self)._reset(
        )
        self._data=np.array([1])
