from dnfpy.model.inputMap import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNF import MapDNF
from dnfpy.stats.statsList import StatsList
from dnfpy.model.fieldMap import FieldMap
from dnfpy.model.activationMap import ActivationMap
from dnfpy.cellular.cellularNeuralMap import CellularNeuralMap
from dnfpy.cellular.cellularNeuralMap import BlockRotationDiffusion
import numpy as np

class ModelDNFCellular(Model,Renderable):
    def initMaps(self,size=49,dt=0.1,model="spike",lut=[0]*(2**6),da=0.011,di=-0.01,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,
                 ):
        """We initiate the map and link them"""
       # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))
        #Create maps
        self.aff = InputMap("Inputs",size,dt=dt)
                            #iStim1 = 0, iStim2 = 0,noiseI=1.,noise_dt=1e10)
        self.field = FieldMap("DNF",size,dt=dt,model=model,resetLat=True)


        self.act = ActivationMap("activation",size,dt=dt,model=model,dtype=np.bool_)
        self.act.addChildren(field=self.field)


        dtLat = dt/(size*2+100)
        self.lat = CellularNeuralMap("lat",size,dt=dtLat,da=da,di=di,activationState=1)

        #lut = np.random.randint(0,2,(2**6)).astype(np.bool_)
        #print("lut %s"%lut.astype(np.uint8))
        self.caA = BlockRotationDiffusion("caAct",size,dt=dtLat,wrap=False,p=0.05)
        self.lat.addChildren(actMap=self.caA)
        self.caA.addChildren(activation=self.act)


        self.caI = BlockRotationDiffusion("caInh",size,dt=dtLat,wrap=False,p=0.5)
        self.lat.addChildren(inhMap=self.caI)
        self.caI.addChildren(activation=self.act)

        self.field.addChildren(aff=self.aff,lat=self.lat)
        #stats
        self.stats = StatsList(size,self.aff,self.act,
                               self.field,shapeType='gauss')
        #return the roots
        roots =  [self.field]
        roots.extend(self.stats.getRoots())
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.aff,self.field,self.lat,self.caA,self.caI,self.act]
        ret.extend(self.stats.getArrays())
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
