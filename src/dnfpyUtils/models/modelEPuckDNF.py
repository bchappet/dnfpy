from dnfpy.view.renderable import Renderable
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

class ModelEPuckDNF(Model,Renderable):
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
        
        
        self.simulator = VRepSimulator("simulator",1,dt, synchronous=True)
        #self.simulator = RobotSimulator("simulator",1,dt)
                    
        self.simulator.connection()
        
        self.motorL = MotorProjection("motorL", 1, dt, 'l')
        self.motorR = MotorProjection("motorR", 1, dt, 'r')
        self.setMotorL = SetVelMotor("setMotorL", 1, dt, 'l')
        self.setMotorR = SetVelMotor("setMotorR", 1, dt, 'r')
        self.dnfmapI = MapDNFND("dnfmapI", size, dt=0.1, gainAff=100,tau=0.1, wInh=0.15, wrap=wrap, activation=activation)
        self.dnfmapD = MapDNFND("dnfmapD", size, dt=0.1, gainAff=2,tau=0.1, wrap=wrap, activation=activation)
        self.activationI = self.dnfmapI.getActivation()
        self.activationD = self.dnfmapD.getActivation()
        self.navigationMap = MapDNFND("navigationMap", size, dt, tau=0.1, wrap=wrap, activation = "id")
        self.navAff = FuncMapND(utils.subArrays, "navAff", size, dt=dt)
        self.noise = NoiseMap("noise",size,dt=dt,intensity=0.1)
        self.dnfmapDaff= FuncWithoutKeywords(utils.sumArrays, "dnfmapDaff", size, dt=dt)
        
        self.modelI =ConvolutionND("IRSensorsModel",size,dt=dt,wrap=wrap)
        self.modelD =ConvolutionND("DirectionModel",size,dt=dt,wrap=wrap)
        #self.kernel = FuncMapND(utils.gaussNd,"sensor_noseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        self.kernelI = FuncMapND(utils.gaussNd,"I_noiseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.1*size)
        self.kernelD = FuncMapND(utils.gaussNd,"D_noiseK",size,dt=dt,center=center,wrap=wrap,intensity=1,width=0.05*size)
        
        
        self.getIRSensors = GetIRSensors("IRSensors", size, dt, nbSensors=50)
        self.getDirection = GetDirection("Direction",size, dt)
        
        """
        irSensor = np.zeros((size))
        direction = np.zeros((size))
        
        self.getIRSensors = ConstantMap("IRSensors", size,value=irSensor)
        self.getDirection = ConstantMap("Direction",size, value=direction)
        """
        
        #Specify children
        self.navigationMap.addChildren(aff=self.navAff)
        self.navAff.addChildren(a=self.activationD, b=self.activationI)
        self.dnfmapDaff.addChildren(self.modelD, self.noise)
        self.modelI.addChildren(source=self.getIRSensors, kernel=self.kernelI)
        self.modelD.addChildren(source=self.getDirection, kernel=self.kernelD)
        
        self.motorL.addChildren(activationN=self.navigationMap.getActivation(), activationI = self.activationI)
        self.setMotorL.addChildren(motor=self.motorL, simulator=self.simulator)
        self.motorR.addChildren(activationN=self.navigationMap.getActivation(), activationI = self.activationI)
        self.setMotorR.addChildren(motor=self.motorR, simulator=self.simulator)
        
        self.activationI.addChildren(dnfmapI=self.dnfmapI)
        self.activationD.addChildren(dnfmapD=self.dnfmapD)
        self.getIRSensors.addChildren(simulator=self.simulator)
        self.getDirection.addChildren(simulator=self.simulator)
        self.dnfmapI.addChildren(aff=self.modelI)
        self.dnfmapD.addChildren(aff=self.dnfmapDaff )
        
        #return the roots
        roots =  [self.setMotorL, self.setMotorR]

        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.motorL, self.motorR, self.activationI, self.dnfmapI, self.modelI, self.activationD, self.dnfmapD,  self.modelD, self.navigationMap, self.navigationMap.getActivation()]

        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
        
    def _reset(self):
        super(ModelEPuckDNF,self)._reset(
        )
        self.simulator.disconnection()
        self.simulator.connection()
        
