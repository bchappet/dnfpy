from dnfpy.core.mapND import MapND
import math
import numpy as np

class GetDirection(MapND):
    """
    Get IR sensors from a robot simulator
    """
    
    def __init__(self, name, size=8, dt=0.1, **kwargs):
        super(GetDirection,self).__init__(
        name,size,dt=dt,**kwargs        
        )
        
    def _compute(self, simulator, size):
        
            
            
        orientation_data=simulator.getOrientation("ePuck","Cuboid")
        orientation_data=simulator.getOrientation("ePuck","Cuboid")
        print("orientation_data", orientation_data)
        if (orientation_data[0]<=0):
            psi=orientation_data[1]
        else:
            if (orientation_data[1]<0):
                psi=-math.pi-orientation_data[1]
            else:
                psi=math.pi-orientation_data[1]
        print("psi",psi)
        
        position_data=simulator.getPosition("ePuck","Cuboid")
        position_data=simulator.getPosition("ePuck","Cuboid")
        print("position_data",position_data)
        tan=position_data[0]/position_data[1]
        alpha=math.atan(tan)
        print("alpha",alpha)
        print("x",position_data[0])
        print("y",position_data[1])
        if position_data[0]>0:
            if position_data[1]>0:
                beta=-psi-math.pi+alpha
                print("beta",beta)
            else:
                beta=-psi+alpha
        else:
            if position_data[1]>0:
                beta=-psi+math.pi+alpha
            else:
                beta=-psi+alpha
            
        indice=int((beta+math.pi)*size*0.9999999/(2*math.pi))
        direction = np.zeros((size))
        direction[indice]=1


        
        self._data=direction