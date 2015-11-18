
from dnfpy.model.inputMap1D import InputMap
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.mapDNFSpace import MapDNFSpace
from dnfpy.core.constantMapND import ConstantMapND
import numpy as np
import math

class ModelDNFSpace(Model,Renderable):
    def initMaps(self,size=49,model="cnft",activation="step",nbStep=0,dim=2,
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=10.,alpha=10.,th=0.75,h=0,noiseI=0.01,
                 iStim1=0.1,beta=8,tau=0.64,lateral='dog',fashion='fix',xStart=-10,xEnd=10,dt=0.1,
                 globalInh = 0.0,
        
                 ):
        # print("iExc : %s, iInh: %s, wExc %s, wInh %s"%(iExc,iInh,wExc,wInh))

        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure size is odd for convolution
        #Define the space matrix:
        axis = np.linspace(xStart,xEnd, size)
        axiss = [axis]*dim
        space = np.meshgrid(*axiss)


        self.field = MapDNFSpace("Potential",size=size,dim=dim,dt=dt,space=space,model=model,activation=activation,nbStep=nbStep,
               iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,th=th,h=h,beta=beta,tau=tau,lateral=lateral,fashion=fashion,
               globalInh=globalInh)
        #return the roots
        roots =  [self.field]
        return roots

    #override Renderable
    def getArrays(self):
        ret =  [self.field,self.field.act,self.field.lat,self.field.kernel,]
        return ret

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%(unicode(mapName),x,y))
