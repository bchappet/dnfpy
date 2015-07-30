from dnfpy.core.map2D import Map2D

class RobotSimulator(Map2D):
    """
    Interface for exchange with robot simulator
    """
    
    def __init__(self, name, size, dt, **kwargs):
        super(RobotSimulator,self).__init__(
        name,size,dt=dt,**kwargs        
        )
        
    def _compute(self):
        pass
    
    def connection(self):
        """
        Make connection with the robot simulator
        raise IOError if impossible to connect
        """
        pass
    
    def disconnection(self):
        """
        Make disconnection with the robot simulator
        """
        pass
    
    def getSensor(self, name, typeSensor):
        """
        Get data of robot sensors
        """
        pass
    
    def setController(self, name, typeControler):
        """
        Give an order to a controller
        """
        pass