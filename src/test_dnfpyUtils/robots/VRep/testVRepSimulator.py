from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
import unittest
import vrep
import time
class TestVRepSimulator(unittest.TestCase):
    def setUp(self):
        self.uut=VRepSimulator("uut", 1, 0.1)
        self.uut.synchronous=True
        
    def testConnectionError(self):
        self.uut.port=19998
        self.assertRaises(IOError, self.uut.connection)
        
    def testConnectionOk(self):
        self.uut.port=19997
        self.uut.connection()
        self.assertNotEquals(self.uut.clientID,-1)
        
    def testDisconnectionOk(self):
        self.uut.port=19997
        self.uut.connection()
        self.uut.disconnection()
      
    def testCompute1(self):
        self.uut.port=19997
        self.uut.connection()
        #t1=vrep.simxGetLastCmdTime(self.uut.clientID)
        self.uut.compute()
        #t2=vrep.simxGetLastCmdTime(self.uut.clientID)
        self.uut.disconnection()
        if self.uut.synchronous==True:
            self.assertEquals(self.uut.returnSynchro,0)
    
    def testGetSensor(self):
        self.uut.port=19997
        self.uut.connection()
        a=0.0
        self.uut.compute()
        a=self.uut.getSensor("ePuck_proxSensor2","prox")
        a=self.uut.getSensor("ePuck_proxSensor2","prox")
        self.assertNotEquals(a,0)
        self.uut.disconnection()
        
    def testGetController(self):
        self.uut.port=19997
        val=1
        self.uut.connection()
        self.uut.setController("ePuck_leftJoint", "motor", val)
        t = time.time()
        if self.uut.synchronous==True:
            for i in range(200):
                self.uut.compute()
        else:
            while (time.time()-t)<5:
                pass
        
        self.uut.disconnection()
    
    def testGetSensors(self):
        self.uut.port=19997
        self.uut.connection()
        a=0.0
        self.uut.compute()
        listname = (["ePuck_proxSensor1","ePuck_proxSensor2","ePuck_proxSensor3"])
        b=self.uut.getSensors(listname,"prox")
        b=self.uut.getSensors(listname,"prox")
        self.assertNotEquals(a,b.all)
        self.uut.disconnection()
    
        
        
if __name__ == '__main__':
    unittest.main()
        
