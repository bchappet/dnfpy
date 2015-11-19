from dnfpy.core.map2D import Map2D
import numpy as np
from sklearn.cluster import DBSCAN
import scipy.spatial.distance as dist

from dnfpyUtils.stats.clusteMap import ClusterMap


class ClusterMap1(ClusterMap):
    """
    For 1 bubble!! 1 cluster is computed simply as barycenter


    Params:
    "continuity" : float if different of 0.0, we assume that the cluster are continuous
        A continuous cluster allow a loss of activity during continuity seconds.
        Otherwise, the cluster is deleted
        We add the last cluster in the current coords
        Then we deduce what label labels the new cluster
        The first iteration determines the labels for the next ones
    "threshold" : threshold for activity value to be considered
    "expectedNumberOfCluster" : 1


    Results:
        _data = np array (2) with cluster barycenter coords X,Y:

    """
    def __init__(self,name,size=0,dt=0.1,threshold=0.4,
                 sizeNpArr=1,continuity=1.0,
                 **kwargs):
        super().__init__(name=name,size=size,dt=dt,threshold=threshold,
            clustSize=clustSize=None,min_samples=None,sizeNpArr=sizeNpArr,
            continuity=continuity,expectedNumberOfCluster=1,
                                        **kwargs)





    def _compute(self,size,np_arr,threshold,clustSize_,continuity,dt):

        maxArr = np.max(np_arr)
        coords = np.where(np_arr > maxArr/1.2)
        self.nbActivation = len(coords[0])
        #if nbActivation > 0 and nbActivation < np_arr.shape[0]*1.6:
        
        #print("threshold : ",nbActMax)
        if self.nbActivation > 0 :
                self._data= np.mean(coords,axis=0)
        else:
                self._data=[np.nan,np.nan]



    def _onParamsUpdate(self,clustSize,sizeNpArr):
        clustSize_ = clustSize * sizeNpArr
        return dict(clustSize_=clustSize_)




