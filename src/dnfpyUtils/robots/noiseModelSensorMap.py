from dnfpy.core.mapND import MapND
import math
import numpy as np
import dnfpy.core.utilsND as utils

class NoiseModelSensorMap(MapND):
    """
    
    """
    
    def __init__(self, name, size=8, dt=0.1, wrap=False, intensity=1, width=0.1, **kwargs):
        super(GetDirection,self).__init__(
        name,size,dt=dt, wrap=wrap, intensity=intensity, width=width, **kwargs        
        )
        
    def _compute(self, sensor, size, wrap, intensity, width):
        coordSensor=np.where(sensor==1)
        for coord in coordSensor:
            utils.gaussNd(size,wrap,intensity, width, coord)