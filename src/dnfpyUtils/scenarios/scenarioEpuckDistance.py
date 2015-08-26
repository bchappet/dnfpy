from scenario import Scenario
import numpy as np

import math
PI=math.pi

class ScenarioEpuckDistance(Scenario):
    def __init__(self,dist=0.1):
        super(ScenarioEpuckDistance,self).__init__()
        self.dist=dist

    def reset(self):
        super(ScenarioEpuckDistance,self).reset()


    def applyContext(self,model):
        """
        If we need to change parameters before modele instanciation
        """
        irSensorMap = model.getMap("IRSensors")
        directionMap = model.getMap("Direction")
        simulator = model.getMap("simulator")
        
        self.size= directionMap.getArg('size')
        simulator.connection()

        positionEPuck=simulator.getPosition("ePuck", "Cuboid")
        print("positionEPuck",positionEPuck)
        positionCuboid=simulator.getPosition("Cuboid","Cuboid")
        print("positionCuboid",positionCuboid)
        self.positionF=positionCuboid
        self.positionF[0]=positionEPuck[0]-0.15
        self.positionF[1]=positionEPuck[1]+self.dist
        print("positionF",self.positionF)
        simulator.setPositionObject("Cuboid3",self.positionF,"Cuboid")
        self.positionF=positionCuboid
        self.positionF[0]=positionEPuck[0]-0.15
        self.positionF[1]=positionEPuck[1]-self.dist
        print("positionF",self.positionF)
        simulator.setPositionObject("Cuboid11",self.positionF,"Cuboid")
        self.direction=0
 
        
        


    def apply(self,model,time,runner):
        self.nbIteration += 1
        self.time = time
        self._apply(model,time,runner)

    def _apply(self,model,time,runner):
        simulator = model.getMap("simulator")
        print("time",self.time)
        if self.time>=25:
            orientation_data=simulator.getOrientation("ePuck","Cuboid")
            #print("orientation_data", orientation_data)
            if (orientation_data[0]<=0):
                psi=orientation_data[1]
            else:
                if (orientation_data[1]<0):
                    psi=-math.pi-orientation_data[1]
                else:
                    psi=math.pi-orientation_data[1]
            print("psi",psi)
            simulator.disconnection()
            
        elif self.time>=24.7:
            orientation_data=simulator.getOrientation("ePuck","Cuboid")
            #print("orientation_data", orientation_data)
            if (orientation_data[0]<=0):
                psi=orientation_data[1]
            else:
                if (orientation_data[1]<0):
                    psi=-math.pi-orientation_data[1]
                else:
                    psi=math.pi-orientation_data[1]
            print("psi",psi)
            

        
        """
        if time > 2.0:
                self.ir[...] = 0
                self.ir[int((self.size/11*5+time)%self.size)] = 1
                self.ir[int((self.size/11*6+time)%self.size)] = 1
                self.ir[int((self.size/11*5-time)%self.size)] = 1
                self.ir[int((self.size/11*6-time)%self.size)] = 1
        else:
            pass
        """

    def finalize(self,model,runner):
        (self.time,self.direction) = \
        super(ScenarioEpuckDistance,self).finalize(model,runner)
        return  (self.time,self.direction)

