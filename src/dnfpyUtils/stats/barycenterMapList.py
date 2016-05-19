import numpy as np
import scipy.spatial.distance as dist
from sklearn.cluster import DBSCAN

from dnfpy.core.mapND import MapND
import dnfpy.core.utilsND as utils

def getClusterLabels(activation,targetCenterList,clustSize,size):
    """
    Perform DBSCAN on the activation using targetCenterList as seed
    """
    coords = np.where(activation>0)
    coordsArray = list(zip(coords[1],coords[0]))
    coordsArray.extend(np.array(targetCenterList)*size)
    coordsArrayNp = np.array(coordsArray)
    distanceMat = dist.cdist(coordsArrayNp,coordsArrayNp,'cityblock')
    db = DBSCAN(min_samples=0,eps=clustSize).fit(distanceMat) 
    return db.labels_,coordsArrayNp 

def getBarycenterLabel(coordsArrayNp,labels,lab):
    """
    Return the barycenter of activity with the label "lab"
    """
    coorBary = coordsArrayNp[np.where(labels == lab)]
    barycenter = np.mean(coorBary,axis=0)
    return barycenter

def getClusterList(labels,coordsArrayNp,nbTarget):
    """
    Return the barycenter of the cluster fitting to the targetCenterList
    return a list of coord of same size as targetCenterList
    """
    labelTargetList = labels[-nbTarget:] #the labels are in the same order as the coordArrayNp
    labels = labels[:-nbTarget]
    return [getBarycenterLabel(coordsArrayNp,labels,lab) for lab in labelTargetList]

def getBadLabel(labels,nbTarget):
    #we add outliers and label not in targetCenterList
    labelTargetList = labels[-nbTarget:]
    badLabel = labels[~np.in1d(labels,labelTargetList)]
    return badLabel


class BarycenterMapList(MapND):
        """
        Input: 
            map : map (child)
            targetCenterList :  map (child) list of target center which will bw used as seed for the DBSCAN
        Output:
            list of coordinates of the barycenter normalized (tuple of size dim) 
        Limitcases:
            if map empty : return (nan)*dim
            if targetCenterList (nan)*dim

        """
        def __init__(self,name,sizeMap=49,clustSize=0.3,dim=1,dt=0.1,convergenceTime=1.0,**kwargs):
                super().__init__(name=name,size=0,dim=dim,dt=dt,sizeMap=sizeMap,clustSize=clustSize,clustSize_=10,
                        convergenceTime=convergenceTime,
                        **kwargs)

        def reset(self):
             super().reset()
             dim = self.getArg('dim')
             self._data = [(np.nan,)*dim]
             self.outsideAct = [] #another trace for outside activation

        def _compute(self,map,dim,targetCenterList,clustSize_,sizeMap):

                if np.sum(map) == 0 or len(targetCenterList) == 0:
                    baryList = [(np.nan,)*dim for t in targetCenterList]
                    nbOutsideAct = np.sum(map)
                else:
                    labels,coordsArrayNp = getClusterLabels(map,targetCenterList,clustSize_,sizeMap)
                    baryList = getClusterList(labels,coordsArrayNp,len(targetCenterList))
                    nbOutsideAct = len(getBadLabel(labels,len(targetCenterList)))

                self._data = [np.array(b)/sizeMap for b in baryList]
                self.outsideAct.append(nbOutsideAct)


        def getViewSpace(self):
                return (1,)*self.getArg('dim')


        def _onParamsUpdate(self,clustSize,sizeMap):
            clustSize_ = clustSize * sizeMap
            return dict(clustSize_=clustSize_)
