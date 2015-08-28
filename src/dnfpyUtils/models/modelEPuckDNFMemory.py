from dnfpy.view.renderable import Renderable
import math
from dnfpy.model.model import Model
from dnfpyUtils.robots.VRep.vRepSimulator import VRepSimulator
from dnfpy.robots.robotSimulator import RobotSimulator
from dnfpyUtils.robots.getIRSensors import GetIRSensors
from dnfpyUtils.robots.getDirection import GetDirection
from dnfpy.core.constantMap import ConstantMap


from dnfpyUtils.robots.moteurProjection import MotorProjection
from dnfpyUtils.robots.setVelMotor import SetVelMotor

from dnfpy.model.mapDNF1D import MapDNFND
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.model.noiseMapND import NoiseMap
from dnfpy.core.funcMapND import FuncMapND
from dnfpy.core.funcWithoutKeywordsND import FuncWithoutKeywords


import dnfpy.core.utilsND as utils
import numpy as np
from dnfpy.core.mapND import MapND
from dnfpy.core.constantMapND import ConstantMapND
from dnfpy.core.gainMap import GainMap


class ProjectionMapND(MapND):
        def __init__(self,name,size,factor=1.0,**kwargs):
                super(ProjectionMapND,self).__init__(name,size,factor=factor,**kwargs)

        def _compute(self, source,shift,size,factor):
                conv = int(np.round(factor*shift*size/(2*np.pi)))
                self._data = np.roll(source,conv)

class PsiMap(MapND):
        """
        Compute absolute angle of the robot assuming that it started at 0
        """
        def _compute(self,motorL,motorR,dt):
                r = 20.5 #mm
                L = 52 #mm


                dpsi_dt = r/L*(motorR - motorL)
                self._data = self._data + dpsi_dt*dt

class PsiMap2(MapND):
        """
        Get the absolute angle of the robot from the simulator
        """
        def _compute(self,simulator):
            orientation_data= simulator.getOrientation("ePuck")
            if (orientation_data[0]<=0):
                psi=orientation_data[1]
            else:
                if (orientation_data[1]<0):
                    psi=-math.pi-orientation_data[1]
                else:
                    psi=math.pi-orientation_data[1]

            self._data = psi






class ModelEPuckDNFMemory(Model,Renderable):
    def initMaps(self, size
                 ):
        """We initiate the map and link them"""
        dt=0.1
        nbD = 20
        nbI = 20
        center = (size - 1)/2
        wrap=True
        activation="sigm"
        #Create maps
        
        
        self.simulator = VRepSimulator("simulator",1,dt, synchronous=False)
        #self.simulator = RobotSimulator("simulator",1,dt)
                    
        self.simulator.connection()
        
        self.motorL = MotorProjection("motorL", 1, dt, 'l')
        self.motorR = MotorProjection("motorR", 1, dt, 'r')
        self.setMotorL = SetVelMotor("setMotorL", 1, dt, 'l')
        self.setMotorR = SetVelMotor("setMotorR", 1, dt, 'r')
        self.dnfmapI = MapDNFND("dnfmapI", size, dt=0.1, gainAff=140,tau=0.1, wInh=0.12,wExc=0.02, wrap=wrap, activation='sigm',noiseI=0.01)
        self.dnfmapD = MapDNFND("dnfmapD", size, dt=0.1, gainAff=2,tau=0.1, wrap=wrap, activation=activation,noiseI = 0.01)
        
        self.modelI =ConvolutionND("IRSensorsModel",size,dt=dt,wrap=wrap)
        self.modelD =ConvolutionND("DirectionModel",size,dt=dt,wrap=wrap)
        #self.kernel = FuncMapND(utils.gaussNd,"sensor_noseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        self.kernelI = FuncMapND(utils.gaussNd,"I_noiseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        self.kernelD = FuncMapND(utils.gaussNd,"D_noiseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        
        irSensor = np.zeros((size))
        direction = np.zeros((size))
        #self.getIRSensors = ConstantMap("IRSensors", size,value=irSensor)
        #self.getDirection = ConstantMap("Direction",size, value=direction)
        
        self.getIRSensors = GetIRSensors("IRSensors", size, dt, nbSensors=8)
        self.getDirection = GetDirection("Direction",size, dt)


        self.psi = PsiMap2("psi",size=1,dt=0.1)
        #self.psi.addChildren(motorL=self.motorL,motorR=self.motorR)
        self.psi.addChildren(simulator=self.simulator)


        self.projTarget = ProjectionMapND("projTarget",size=size,dt=dt)
        self.projTarget.addChildren(source=self.dnfmapD.getActivation(),shift=self.psi)


        self.projObstacle = ProjectionMapND("projObtacle",size=size,dt=dt)
        self.projObstacle.addChildren(source=self.dnfmapI.getActivation(),shift=self.psi)


        self.memObs = MapDNFND("memoryObstacle",size=size,dt=dt,tau=1.3,wrap=wrap,activation='step',iExc=3.1,wInh=0.1,wExc=0.05)
        self.memObs.addChildren(aff=self.projObstacle)

        self.navigationMap = MapDNFND("navigationMap", size, dt, tau=0.64, wrap=wrap, activation = "step",wInh=10.0,th=0.01,noiseI=0.01)
        self.navAff = FuncMapND(utils.subArrays, "navAff", size, dt=dt)
        self.navigationMap.addChildren(aff=self.navAff)
        gainObs = GainMap(self.memObs.getActivation(),gain=1.2)
        self.navAff.addChildren(a=self.projTarget, b=gainObs)


        self.navRelativeMap = ProjectionMapND("navigationRelative",size=size,dt=dt,factor=-1.0)
        self.navRelativeMap.addChildren(source=self.navigationMap.getActivation(),shift=self.psi)

        zeros = ConstantMapND("zeros",size=size,value=np.zeros((size)))
        
        #Specify children
        self.modelI.addChildren(source=self.getIRSensors, kernel=self.kernelI)
        self.modelD.addChildren(source=self.getDirection, kernel=self.kernelD)
        
        self.motorL.addChildren(activationN=self.navRelativeMap, activationI = zeros)
        self.setMotorL.addChildren(motor=self.motorL, simulator=self.simulator)
        self.motorR.addChildren(activationN=self.navRelativeMap, activationI = zeros)
        self.setMotorR.addChildren(motor=self.motorR, simulator=self.simulator)
        
        self.getIRSensors.addChildren(simulator=self.simulator)
        self.getDirection.addChildren(simulator=self.simulator)
        self.dnfmapI.addChildren(aff=self.modelI)
        self.dnfmapD.addChildren(aff=self.modelD )
        
        #return the roots
        roots =  [self.setMotorL,self.setMotorR]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.motorL, self.motorR,  self.dnfmapI, self.dnfmapD, self.navigationMap,self.navigationMap.getActivation(),self.memObs,self.memObs.kernel,self.navigationMap.kernel,self.dnfmapI.kernel,self.kernelI]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        
    def _reset(self):
        super(ModelEPuckDNF,self)._reset(
        )
        self.simulator.disconnection()
        self.simulator.connection()
        
