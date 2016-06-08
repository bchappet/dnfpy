import numpy as np
from dnfpyUtils.stats.statistic import Statistic
import scipy.spatial.distance as dist
from sklearn.cluster import DBSCAN

from dnfpy.core.mapND import MapND
import dnfpy.core.utils as utils

def getClusterLabels(activation,targetCenterList,clustSize,size,min_samples=0):
    """
    Perform DBSCAN on the activation using targetCenterList as seed
    """
    coords = np.where(activation>0)
    coordsArray = list(zip(coords[1],coords[0]))
    coordsArray.extend(np.array(targetCenterList)*size)
    coordsArrayNp = np.array(coordsArray)
    distanceMat = dist.cdist(coordsArrayNp,coordsArrayNp,'cityblock')
    db = DBSCAN(min_samples=min_samples,eps=clustSize).fit(distanceMat) 
    return db.labels_,coordsArrayNp 

def getBarycenterLabel(coordsArrayNp,labels,lab):
    """
    Return the barycenter of activity with the label "lab"
    """
    coorBary = coordsArrayNp[np.where(labels == lab)]
    barycenter = np.mean(coorBary,axis=0)
    return barycenter

def getClusterList(labels,coordsArrayNp,nbTarget,dim):
    """
    Return the barycenter of the cluster fitting to the targetCenterList
    return a list of coord of same size as targetCenterList
    """
    if nbTarget > 0:
        labelTargetList = labels[-nbTarget:] #the labels are in the same order as the coordArrayNp
        labels = labels[:-nbTarget]
        ret = []
        for lab in labelTargetList:
            if lab < 0:
                ret.append(list((np.nan,)*dim))
            else:
                ret.append(getBarycenterLabel(coordsArrayNp,labels,lab))
        return ret
    else:
        return []

def getBadLabel(labels,nbTarget):
    #we add outliers and label not in targetCenterList
    labelTargetList = labels[-nbTarget:] if nbTarget > 0 else []
    badLabel = labels[~np.in1d(labels,labelTargetList)]
    return badLabel

def getNewClusterList(labels,coordsArrayNp,nbTarget):
    """ 
    Return the barycenter of the cluster not fitting to the targetCenterList
    return a list of coord 
    """
    badLabels = getBadLabel(labels,nbTarget)
    newLabels = set(badLabels[badLabels!=-1]) #we do not want outliers
    return [getBarycenterLabel(coordsArrayNp,labels,lab) for lab in newLabels]

def  getValidClusterList(clusterList):
    """
    return a list of valid cluster and their coordinate in the main list
    """
    validCoord = []
    validClusterIndex = []
    for i,coord in zip(range(len(clusterList)),clusterList):
        if not(np.any(np.isnan(coord))) :
            validCoord.append(coord)
            validClusterIndex.append(i)
    return validCoord,validClusterIndex



class ClusterMapList(Statistic):
        """
        Input: 
            map : map (child)
        Output:
            list of coordinates of the barycenter normalized (tuple of size dim) 
            past and present clusters : the list is geting bigger.
            diseapered clusters are (nan)*dim
        Limitcases:
            if map empty : return (nan)*dim
        TODO :
            set some threshold for removing cluster

        """
        def __init__(self,name,sizeMap=49,clustSize=0.3,dim=1,dt=0.1,min_samples=0,**kwargs):
                super().__init__(name=name,size=0,dim=dim,dt=dt,sizeMap=sizeMap,
                        clustSize=clustSize,clustSize_=10,
                        min_samples=min_samples,
                        **kwargs)
                self.trace = []

        def reset(self):
             super().reset()
             dim = self.getArg('dim')
             #self._data = [(np.nan,)*dim]
             self._data = []
             self.outsideAct = [] #another trace for outside activation
             self.trace = []

        def getTrace(self):
            return self.trace

        def _compute(self,map,dim,clustSize_,sizeMap,min_samples):

                if np.sum(map) == 0 :
                    baryList = [(np.nan,)*dim for t in self._data]
                    nbOutsideAct = 0
                else:
                    validCoord,validClusterIndex= getValidClusterList(self._data)
                    labels,coordsArrayNp = getClusterLabels(map,validCoord,clustSize_,sizeMap,min_samples)
        
                    #update coord of clusters   
                    validCoord = getClusterList(labels,coordsArrayNp,len(validCoord),dim)
                    #check if there arre new cluster
                    newCoord = getNewClusterList(labels,coordsArrayNp,len(validCoord))
                    nbOutsideAct = len(getBadLabel(labels,len(validCoord)))
                    
                    baryList = np.ones((len(self._data)+len(newCoord),dim))*np.nan
                    #set the cluster coords at their right position
                    for i,bary in zip(validClusterIndex,validCoord):
                        baryList[i,:] = bary
                    #add the new clusters
                    for i,bary in zip(range(len(self._data),len(self._data)+len(newCoord)),newCoord):
                        baryList[i,:] = bary


                self._data = [np.array(b)/sizeMap for b in baryList]
                self.outsideAct.append(nbOutsideAct)
                self.trace.append(np.copy(self._data))


        def getViewSpace(self):
                return (1,)*self.getArg('dim')


        def _onParamsUpdate(self,clustSize,sizeMap):
            clustSize_ = clustSize * sizeMap
            return dict(clustSize_=clustSize_)
