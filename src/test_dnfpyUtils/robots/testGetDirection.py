from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpyUtils.robots.getDirection import GetDirection
import unittest

import math
class TestGetDirection(unittest.TestCase):
    def setUp(self):
        self.uut=VRepSimulator("uut", 1, 0.1)
        self.uut.synchronous=True
        self.uut.port=19997
        self.uut.connection()
        self.vvt=GetDirection("vvt",8)
        self.vvt.addChildren(simulator=self.uut)
        
    def testCompute1(self):
        
        a=0
        beta=0
        
        self.vvt.compute()
        beta=self.vvt.getData()
        print("position",beta)
        self.assertNotEquals(a,beta.any())
        self.uut.disconnection()
        
    def testCompute2(self):
        orientation_data=[]
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
        if position_data[1]==0:
            if position_data[0]<0:
                alpha=-math.pi/2
            else:
                alpha=math.pi/2
        else:
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
            
        indice=int((beta+math.pi)*size/(2*math.pi))
        direction = np.zeros((size))
        direction[indice]=1
    
        
        
if __name__ == '__main__':
    unittest.main()
        
