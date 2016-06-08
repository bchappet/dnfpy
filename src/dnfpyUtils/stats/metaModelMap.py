import numpy as np
import dnfpy.core.utils as utils

from dnfpy.core.mapND import MapND
class MetaModelMap(MapND):
        """
        Input: 
            track : map will be used to acquire the intensity of the stimulu alpha and position z0 (child)
            tau,a : float (constructor) parameters of the meta model
            


        Output:
            Inspired from Fung,Wong and Wu , A moving bump in a continuous manifold:...
            In one dimension
            We model the position of the buble  z with
            dz/dt = alpha/tau * (z0 - z) exp[-(z0 - z)²/(8a²)]
            z is normalized
            z is a tuple 

        """
        def __init__(self,name,trackMap,dim=1,dt=0.1,wrap=True,tau=0.64,a=0.3,**kwargs):
                super(MetaModelMap,self).__init__(name=name,size=0,dim=dim,dt=dt,tau=tau,a=a,wrap=wrap,**kwargs)
                self.track = trackMap
                self.z0 = (np.nan,)*dim #z0 is the center of the track
                self.lag = 0


        def _compute(self,tau,a,dt,wrap):
                sizeMap = self.track.getArg('size')
                a = a /10

                alpha,width = self.track.getShape() #intensity,width

                self.z0 = np.array(self.track.getCenter())
                self.z0 = self.z0 / sizeMap

                if wrap:
                    dist = utils.wrappedVector(self.z0,self._data,1)
                else:
                    dist= self.z0 - self._data

                self.lag =  np.linalg.norm(dist) #z0 - z
                
                div = 8*a**2
                exp = np.exp( -((self.lag**2)/(div)))

                self._data = self._data + dt*(alpha/tau * (dist)  * exp  )


        def initPos(self,z):
            self._data = z

        def getViewData(self):
                return (self.lag,)

        def getViewSpace(self):
                return (1,)





