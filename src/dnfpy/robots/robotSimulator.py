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
        self._data = self
    
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
    
    def getSensors(self, listname, typeSensor):
        """
        Get data of several same robot sensors
        """
        pass
    
    def setController(self, name, typeController, val):
        """
        Give an order to a controller
        """
        pass
    
    def getOrientation(self, name, relativeName=None):
        """
        Get the orientation of an object
        """
        
    def getPosition(self, name, relativeName):
        """
        Get the position of an object
        """
        pass
        
    def setPositionObject(self, name, relativeName, position):
        """
        Set the position of an object
        """
        pass
    
    def copyObject(self,name,relativeName=None,position):
        """
        Copy and paste an object in a specific position
        """
        pass