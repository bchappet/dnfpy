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
import numpy as np

class VRepSimulator(RobotSimulator):
    """
    Class for exchange with v-rep simulator
    """
    
    def __init__(self, name, size, dt, synchronous=True, **kwargs):
        super(RobotSimulator,self).__init__(
        name,size,dt=dt,synchronous=synchronous,**kwargs        
        )
        self.synchronous=synchronous
        self.clientID=-1 #ID of client initialized
        self.port=19997 #Port initialisation
        self.returnSynchro=-1 #initialisation return flag from simsxSychronousTrigger
        self.returnStart=-1 #initialisation return flag from simsxStartSimulation
        
    def _compute(self):
        if self.synchronous:
            self.returnSynchro=vrep.simxSynchronousTrigger(self.clientID)
        self._data=self
    
    def connection(self):
        """
        Make connection with v-rep simulator
        """
        print ('Waiting for connection...')
        vrep.simxFinish(-1) # just in case, close all opened connections
        self.clientID=vrep.simxStart('127.0.0.1',self.port,True,True,5000,5) # Connect to V-REP
        if self.clientID!=-1:
            print ('Connected to remote API server')
            
            # enable the synchronous mode on the client:
            if self.synchronous:
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
        Get data of robot sensor
        Different type of sensor:
        -prox
        -cam
        """
        if typeSensor == "prox":
            
            errorCode,sensor_handle=vrep.simxGetObjectHandle(self.clientID,name,vrep.simx_opmode_oneshot_wait)
            errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(self.clientID,sensor_handle,vrep.simx_opmode_streaming)
            #errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(self.clientID,sensor_handle,vrep.simx_opmode_buffer)
            sensor_val = np.linalg.norm(detectedPoint)
            print(sensor_val)
            return sensor_val
        elif typeSensor == "cam":
            pass
                    
    def getSensors(self, listname, typeSensor):
        """
        Get data of several same robot sensors
        """
        sensors_val=np.array([])
        for name in listname:
            sensors_val=np.append(sensors_val,self.getSensor(name,typeSensor))
        return sensors_val
    
    def setController(self, name, typeController, val):
        """
        Give an order to a controller
        """
        if typeController == "motor":
            errorCode,motor_handle=vrep.simxGetObjectHandle(self.clientID,name,vrep.simx_opmode_oneshot_wait)
            vrep.simxSetJointTargetVelocity(self.clientID,motor_handle,val, vrep.simx_opmode_streaming)
        