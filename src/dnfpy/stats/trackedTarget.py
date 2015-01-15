from dnfpy.core.map2D import Map2D
from scipy.spatial import distance
import numpy as np

class TrackedTarget(Map2D):
    """
    If can switch is on, we compute the trackedTarget at every comptation

    Otherwhise, if the tracked target are coherent for
    "coherencyTime" seconds, the tracked target are constant for the rest
    of the simulation

    _data contains coords X,Y of closest track of cluster i
    or -1,-1 if no track with dist <= "distMax"*"sizeArray"

    """
    def __init__(self,name,size=0,dt=0.1,sizeArray=20,canSwitch=True,
                 coherencyTime=1.,distMax=0.2,**kwargs):
        super(TrackedTarget,self).__init__(name=name,size=size,dt=dt,
                sizeArray=sizeArray,
                canSwitch=canSwitch,distMax=distMax,
                coherencyTime=coherencyTime,
                                           **kwargs)

    def _compute(self,time,coherencyTime,canSwitch,distMax_):
        #for every cluster find the track with dist < distMax_
        closestTrack = []
        for clusterCoord in self.clusterMap.getData():
            closest = np.array([-1,-1])
            for trackCoord in self.potentialTarget.getData():
                if distance.euclidean(clusterCoord,trackCoord) <= distMax_:
                    closest = trackCoord
                    break
            closestTrack.append(closest)
            self._data = np.array(closestTrack)


    def _onParamsUpdate(self,distMax,sizeArray):
        distMax_ = distMax*sizeArray
        return dict(distMax_=distMax_)





    def _onAddChildren(self,**kwargs):
        """
        expect potentialTarget and clusterMap
        """
        self.potentialTarget = kwargs["potentialTarget"]
        self.clusterMap = kwargs["clusterMap"]


