from dnfpy.core.map2D import Map2D
import numpy as np
from sklearn.cluster import DBSCAN
import scipy.spatial.distance as dist



class ClusterMap(Map2D):
    """
    Params:
    "continuity" : float if different of 0.0, we assume that the cluster are continuous
    Hence we add the last cluster in the current coords
    Then we deduce what label label the new cluster
    The first iteration determines the labels for the next ones

    Results:
        _data = np array (nb_clust*2) with cluster barycenter coords X,Y:
            1,2
            3,5
            3.8,3.4
    "nbOutliners" : int nb outliners found at the last compute
    if continuity > 0
    "nbNewCluster": int nb of newly build cluster
    "nbDiscontinuousCluster": int nb cluster which where outliners

    """
    def __init__(self,name,size=0,dt=0.1,threshold=0,min_samples=1,
                 clustSize=0.1,sizeNpArr=1,continuity=0.0,**kwargs):
        super(ClusterMap,self).__init__(name=name,size=size,dt=dt,threshold=threshold,
            clustSize=clustSize,min_samples=min_samples,sizeNpArr=sizeNpArr,
            continuity=continuity,
                                        **kwargs)
        self.clusters = []#cluster coords saved
        self.setArg(nbOutliners=0)
        self.setArg(nbNewCluster=0)
        self.setArg(nbDiscountinuousCluster=0)
        self.setArg(nbComputationEmpty=0)

    def _compute(self,np_arr,threshold,min_samples,clustSize_,continuity):
        self.toProf(np_arr,threshold,min_samples,clustSize_,continuity)

    @profile
    def toProf(self,np_arr,threshold,min_samples,clustSize_,continuity):
        coords = np.where(np_arr > threshold)
        nbActivation = len(coords[0])
        if nbActivation > 0:
            coordsArray = list(zip(coords[1],coords[0]))
            nbClust = len(self.clusters)

            if continuity > 0:
                for i in range(nbClust):
                    coordsArray.append(self.clusters[nbClust-1-i])


            coordsArrayNp = np.array(coordsArray)
            distanceMat = dist.cdist(coordsArrayNp,coordsArrayNp)
            db = DBSCAN(min_samples=min_samples,eps=clustSize_).fit(distanceMat)

            unique_labels = set(db.labels_) - set([-1])

            dictLabel = {}
            self.clusters = []
            #set the number discontinuous cluster
            nbDiscontinuousCluster = 0
            nbNewCluster = 0
            if continuity > 0:
                for i in range(nbClust):
                    #remove clusters from coordsArrayNp
                    #del coordsArray[nbClust-1-i]
                    #coordsArrayNp = np.array(coordsArray)
                    lab =  db.labels_[-1-i]
                    np.delete(db.labels_,-1-i)
                    if lab == -1:
                        nbDiscontinuousCluster += 1
                    dictLabel[i] = lab

                #without the previsou cluster
                nb_outliners = len(np.where(db.labels_ == -1)[0])

                for key in dictLabel.keys():
                    lab = dictLabel[key]
                    barycenter = self.__getBarycenter(coordsArrayNp,db.labels_,lab)
                    self.clusters.append(barycenter)

                for lab in unique_labels -set(dictLabel.values()):
                    barycenter = self.__getBarycenter(coordsArrayNp,db.labels_,lab)
                    self.clusters.append(barycenter)
                    nbNewCluster += 1


                self.setArg(nbNewCluster=nbNewCluster)
                self.setArg(nbDiscontinuousCluster=nbDiscontinuousCluster)

            else:
                nb_outliners = len(np.where(db.labels_ == -1)[0])
                for lab in unique_labels:
                    barycenter = self.__getBarycenter(coordsArrayNp,db.labels_,lab)
                    self.clusters.append(barycenter)

            self.setArg(nbOutliners=nb_outliners)
            self._data = np.array(self.clusters)
        else:
            self.setArg(nbComputationEmpty=self.getArg("nbComputationEmpty")+1)


    def __getBarycenter(self,coordsArrayNp,labels,lab):
                coorBary = coordsArrayNp[np.where(labels == lab)]
                barycenter = np.mean(coorBary,axis=0)
                return barycenter


    def _onParamsUpdate(self,clustSize,sizeNpArr):
        clustSize_ = clustSize * sizeNpArr
        return dict(clustSize_=clustSize_)




