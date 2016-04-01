from dnfpy.core.map2D import Map2D
import numpy as np
from sklearn.cluster import DBSCAN
import scipy.spatial.distance as dist



class ClusterMap(Map2D):
    """
    Params:
    "continuity" : float if different of 0.0, we assume that the cluster are continuous
        A continuous cluster allow a loss of activity during continuity seconds.
        Otherwise, the cluster is deleted
        We add the last cluster in the current coords
        Then we deduce what label labels the new cluster
        The first iteration determines the labels for the next ones
    "threshold" : threshold for activity value to be considered
    "min_sample" : how many activation are enough to be considered as a cluster
    "clustSize" : in [0,1] max size of the expected cluster
    "expectedNumberOfCluster" : as its name suggest. We will not compute anything if
    the number of activation is higher than
        (np.pi*(clustSize_/2.0)**2)*expectedNumberOfCluster
        where clustSize_ is the actual clustSize = clustSize*size


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
    def __init__(self,name,size=0,dt=0.1,threshold=0.4,min_samples=3,
                 clustSize=0.15,sizeNpArr=1,continuity=1.0,expectedNumberOfCluster=1,
                 **kwargs):
        super(ClusterMap,self).__init__(name=name,size=size,dt=dt,threshold=threshold,
            clustSize=clustSize,min_samples=min_samples,sizeNpArr=sizeNpArr,
            continuity=continuity,expectedNumberOfCluster=expectedNumberOfCluster,
                                        **kwargs)



    def reset(self):
        super().reset()
        self.clusters = []#cluster coords saved
        #if continuity > 0, the cluster shoul not be off for more than continuity seconds
        self.clusterOff = [] #we save the number of iteration that the cluster is off in this list
        self.setArg(nbOutliners=0)
        self.setArg(nbNewCluster=0)
        self.setArg(nbDiscountinuousCluster=0)
        self.setArg(nbComputationEmpty=0)
        self.sumNbClusterSave = []
        self.setArg(nbClusterSum=0)
        self.setArg(maxNbAct=0)
        self.nbActList = []
        self.nbActivation = 0
        self.diffNbClusterSum = 0 #add |nbClust - expectedNumberOfCluster| at every step
        self._data = []


    def _compute(self,size,np_arr,threshold,min_samples,clustSize_,continuity,expectedNumberOfCluster,dt):
        self.toProf(size,np_arr,threshold,min_samples,clustSize_,continuity,expectedNumberOfCluster,dt)

    def getMaxNbAct(self):
        if len(self.nbActList) > 0:
            return np.max(self.nbActList)
        else:
            return np.nan

    def getMeanNbAct(self):
        if len(self.nbActList) > 0:
            return np.mean(self.nbActList)
        else:
            return np.nan

    def toProf(self,size,np_arr,threshold,min_samples,clustSize_,continuity,
               expectedNumberOfCluster,dt):
        maxArr = np.max(np_arr)
        coords = np.where(np_arr > maxArr/1.2)
        self.nbActivation = len(coords[0])
        print(self.nbActivation)
        #if nbActivation > 0 and nbActivation < np_arr.shape[0]*1.6:
        
        #print(expectedNumberOfCluster,clustSize_)
        nbActMax = (np.pi*(clustSize_/2.0)**2)*expectedNumberOfCluster
        if self.nbActivation < nbActMax and (self.nbActivation > 0 or (continuity > 0) and (len(self.clusters)>0)):
            #print("nbActivation : %s"%self.nbActivation)
            self.nbActList.append(self.nbActivation)
            coordsArray = list(zip(coords[1],coords[0]))
            nbClust = len(self.clusters)

            if continuity > 0:
                #we add the previous clusters to the coordArray : hence we 'll have the same label
                for i in range(nbClust):
                    coordsArray.append(self.clusters[nbClust-1-i])


            
            coordsArrayNp = np.array(coordsArray)
            distanceMat = dist.cdist(coordsArrayNp,coordsArrayNp)
            db = DBSCAN(min_samples=min_samples,eps=clustSize_).fit(distanceMat)

            #set of labels (minus outliners)
            unique_labels = set(db.labels_) - set([-1])
            #print(db.labels_)
            set_label = list(set(db.labels_))
            #print(set_label)

            dictLabel = {} #dictionray {index cluster -> label}
            self.clusters = []
            #set the number discontinuous cluster
            nbDiscontinuousCluster = 0
            nbNewCluster = 0
            if continuity > 0:
                clusterToDelete = [] #if cluster i is deleted, we need to delete self.clusterOff[i]
                labelToDelete = []
                #print("nbLabel %s"%len(set_label))
                for i in range(nbClust): 
                    #lab =  db.labels_[-1-i]
                    #print("index %s nb %s"%(-1-i,len(set_label)))
                    if i < len(set_label):
                        lab =  db.labels_[-1-i]#the labels are in the same ordre as the coordArray we added
                    else:
                        #print("to few label!")
                        clusterToDelete.extend(range(i,nbClust))
                        break

                    #print("i : %s. label %s , sum %s"%(i,lab,np.sum(db.labels_==lab)))
                    #remove clusters from coordsArrayNp
                    #np.delete(db.labels_,-1-i)
                    labelToDelete.append(lab)
                    #set_label.remove(lab)
                    if lab == -1:
                        nbDiscontinuousCluster += 1

                    if np.sum(db.labels_ == lab) == 1:
                        #There is only the artificial activation we introduced => no cluster
                        #we can allow that only for minClusterFreq
                        if self.clusterOff[i] > continuity/dt:
                                #the cluster is deleted
                                #print("delete " + str(i))
                                unique_labels = unique_labels - set([lab])
                                clusterToDelete.append(i)
                        else:
                                #the cluster is still allowed
                                #print("clusterAllowed %s"%i)
                                self.clusterOff[i] += 1
                                dictLabel[i] = lab
                    else:
                        dictLabel[i] = lab
                #delete clusterOff
                clusterToDelete.reverse()
                for i in clusterToDelete:
                    #print(" actually delete " + str(i))
                    del self.clusterOff[i]





                #outliner are the labels which are -1 and not in the cluster list
                nb_outliners = len(np.where(db.labels_ == -1)[0])

                #update cluster positions
                for key in dictLabel.keys():
                    lab = dictLabel[key]
                    barycenter = self.__getBarycenter(coordsArrayNp,db.labels_,lab)
                    self.clusters.append(barycenter)

                #check for new cluster
                for lab in unique_labels -set(dictLabel.values()):
                    barycenter = self.__getBarycenter(coordsArrayNp,db.labels_,lab)
                    #print("add cluster")
                    self.clusters.append(barycenter)
                    self.clusterOff.append(0)
                    nbNewCluster += 1
                
                
                #print("nb cluster ",len(self.clusters))
                #print("nb clusterOff ",len(self.clusterOff))
                self.setArg(nbNewCluster=nbNewCluster)
                self.setArg(nbDiscontinuousCluster=nbDiscontinuousCluster)

            else:
                nb_outliners = len(np.where(db.labels_ == -1)[0])
                for lab in unique_labels:
                    barycenter = self.__getBarycenter(coordsArrayNp,db.labels_,lab)
                    self.clusters.append(barycenter)

            self.setArg(nbOutliners=nb_outliners)
            if len(self.clusters) > expectedNumberOfCluster:
                self.sumNbClusterSave.append(len(self.clusters))
                self.setArg(nbClusterSum=np.sum(self.sumNbClusterSave))

            self.diffNbClusterSum += np.abs(len(self.clusters) - self.getArg("expectedNumberOfCluster"))

            self._data = np.array(self.clusters)
        elif self.nbActivation == 0:
            self.setArg(nbComputationEmpty=self.getArg("nbComputationEmpty")+1)
        else:
            #to many activation we don't compute cluster
            self._data = np.array([np.array([-1,-1])])



    def __getBarycenter(self,coordsArrayNp,labels,lab):
                coorBary = coordsArrayNp[np.where(labels == lab)]
                barycenter = np.mean(coorBary,axis=0)
                return barycenter


    def _onParamsUpdate(self,clustSize,sizeNpArr):
        clustSize_ = clustSize * sizeNpArr
        return dict(clustSize_=clustSize_)




