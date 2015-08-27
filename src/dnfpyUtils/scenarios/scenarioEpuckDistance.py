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
        self.directionMap = model.getMap("Direction")
        self.simulator = model.getMap("simulator")
        
        self.size= self.directionMap.getArg('size')
        self.simulator.startSimulation()


        positionCuboid=self.simulator.getPosition("Cuboid","Cuboid")
        print("positionCuboid",positionCuboid)
        positionEPuck=self.simulator.getPosition("ePuck", "Cuboid")
        print("positionEPuck",positionEPuck)
        self.positionF=positionCuboid
        self.positionF[0]=positionEPuck[0]-0.15
        self.positionF[1]=positionEPuck[1]+self.dist
        print("positionF",self.positionF)
        self.simulator.setPositionObject("Cuboid3",self.positionF,"Cuboid")
        self.positionF=positionCuboid
        self.positionF[0]=positionEPuck[0]-0.15
        self.positionF[1]=positionEPuck[1]-self.dist
        print("positionF",self.positionF)
        self.simulator.setPositionObject("Cuboid11",self.positionF,"Cuboid")
        self.direction=0
        self.i=0
        self.phi1=0
        self.phi2=0
        self.t1=0
        


    def apply(self,model,time,runner):
        self.nbIteration += 1
        self.time = time
        self._apply(model,time,runner)

    def _apply(self,model,time,runner):
        #print("time",self.time)
        psi=self.directionMap.angle
        #print("psi",psi)
        if self.time>=15 and self.i==1:
            self.phi2=psi
            self.dphidt=(self.phi2-self.phi1)/(self.time-self.t1)

            self.simulator.stopSimulation()
        elif self.time>=14.9:
            self.t1=self.time
            self.phi1=psi
            self.i=1


        
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
        return  (self.dist,self.dphidt)

