from dnfpy.robots.robotSimulator import RobotSimulator
try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
    
import time

class VRepSimulator(RobotSimulator):
    """
    Interface for exchange with v-rep simulator
    """
    
    def __init__(self, name, size, dt, **kwargs):
        super(RobotSimulator,self).__init__(
        name,size,dt=dt,**kwargs        
        )
        self.clientID=-1 #ID of client initialized
        self.port=0 #Port initialisation
        self.returnSychro=-1 #initialisation return flag from simsxSychronousTrigger
        self.returnStart=-1 #initialisation return flag from simsxStartSimulation
        
    def _compute(self):
        self.returnSychro=vrep.simxSynchronousTrigger(self.clientID);
    
    def connection(self):
        """
        Make connection with v-rep simulator
        """
        print ('Program started')
        vrep.simxFinish(-1) # just in case, close all opened connections
        self.clientID=vrep.simxStart('127.0.0.1',self.port,True,True,5000,5) # Connect to V-REP
        if self.clientID!=-1:
            print ('Connected to remote API server')
            
            # enable the synchronous mode on the client:
            vrep.simxSynchronous(self.clientID,True)
            
            # start the simulation:
            vrep.simxStartSimulation(self.clientID,vrep.simx_opmode_oneshot_wait)
            
        else:
            raise IOError('Failed connecting to remote API server')
            
            
    
    def disconnection(self):
        """
        Make disconnection with v-rep simulator
        """
        # stop the simulation:
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_oneshot_wait)
        
        # Now close the connection to V-REP:	
        vrep.simxFinish(self.clientID)
    
    def getSensor(self, name, typeSensor):
        """
        Get data of robot sensors
        """
        
    
    def setController(self, name, typeControler):
        """
        Give an order to a controller
        """
        pass