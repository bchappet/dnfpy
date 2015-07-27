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
    def __init__(self,name,size=1,dt=0.1,sizeArray=20,canSwitch=False,
                 coherencyTime=2.,distMax=0.2,**kwargs):
        super(TrackedTarget,self).__init__(name=name,size=size,dt=dt,
                sizeArray=sizeArray,
                canSwitch=canSwitch,distMax=distMax,
                coherencyTime=coherencyTime,
                                           **kwargs)
        self.coherency = 0
        self.saveClosestTrackIndices = []
        self.freezed = False #true when long enough coherency

    def isFreezed(self):
        return self.freezed

    def _compute(self,time,coherencyTime,canSwitch,distMax_):
        potentialTargetData = self.potentialTarget.getData()
        if not(self.freezed) or canSwitch:
            #for every cluster find the track with dist < distMax_
            closestTrack = []
            closestTrackIndices = []
            #print("clusterCoord%s"%self.clusterMap.getData())
            clusterCoords = self.clusterMap.getData()
            for clusterCoord in clusterCoords:
                closest = np.array([-1,-1])
                closestIndex = -1
                i_track = 0
                for trackCoord in potentialTargetData:
                    if distance.euclidean(clusterCoord,trackCoord) <= distMax_:
                        closest = trackCoord
                        closestIndex = i_track
                        break
                    i_track += 1

                closestTrack.append(closest)
                closestTrackIndices.append(closestIndex)

            if len(clusterCoords) > 0 and\
                closestTrackIndices == self.saveClosestTrackIndices \
                and not (-1 in closestTrackIndices):
                    self.coherency += 1
            else:
                self.coherency = 0

            if coherencyTime <= self.coherency * self.getArg('dt'):
                if not canSwitch:
                    self.freezed = True

            closestTrackArr = np.array(closestTrack)
            self._data = closestTrackArr
            self.saveClosestTrackIndices = closestTrackIndices
        else:
            #we are freezed
            closestTrack = []
            i = 0
            for clusterCoord in self.clusterMap.getData():
                closest = np.array([-1,-1])
                if i < len(self.saveClosestTrackIndices):
                    index = self.saveClosestTrackIndices[i]
                    if index != -1:
                        closest = potentialTargetData[index]
                    else:
                        pass #-1,-1
                else:
                    pass
                closestTrack.append(closest)
                i += 1


            closestTrackArr = np.array(closestTrack)
            self._data = closestTrackArr




    def _onParamsUpdate(self,distMax,sizeArray):
        distMax_ = distMax*sizeArray
        return dict(distMax_=distMax_)



    def reset(self):
        super(TrackedTarget,self).reset()
        self._data = np.array([])
        self.coherency = 0
        self.saveClosestTrackIndices = []
        self.freezed = False #true when long enough coherency


    def _onAddChildren(self,**kwargs):
        """
        expect potentialTarget and clusterMap
        """
        self.potentialTarget = kwargs["potentialTarget"]
        self.clusterMap = kwargs["clusterMap"]
