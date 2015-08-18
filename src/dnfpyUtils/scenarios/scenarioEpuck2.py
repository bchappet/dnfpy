from scenario import Scenario
import numpy as np
import math
PI=math.pi

class ScenarioEpuck2(Scenario):
    def __init__(self):
        super(ScenarioEpuck2,self).__init__()

    def reset(self):
        super(ScenarioEpuck2,self).reset()


    def applyContext(self,model):
        """
        If we need to change parameters before modele instanciation
        """
        irSensorMap = model.getMap("IRSensors")
        directionMap = model.getMap("Direction")
        self.size= directionMap.getArg('size')

        self.direction = np.zeros((self.size))
        self.direction[self.size/2] = 1
        directionMap.setData(self.direction)
        
        
        self.ir = np.zeros((self.size))
        
        self.ir[int(self.size*(PI/2+0.77)/(2*PI))]=1
        self.ir[int(self.size*(3*PI/2-0.77)/(2*PI))]=1
        irSensorMap.setData(self.ir)

    def apply(self,model,time,runner):
        self.nbIteration += 1
        self.time = time
        self._apply(model,time,runner)

    def _apply(self,model,time,runner):
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
            pass;
    #   (error,wellClusterized,self.time,self.convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty) = \
    #   super(ScenarioSwitchWM,self).finalize(model,runner)
    #   return  (error,wellClusterized,self.time,self.convergence,maxNbAct,meanNbAct,elapsedTime,errorShape,compEmpty,
    #            self.wrongNumberOfCluster/float(self.nbIteration))

