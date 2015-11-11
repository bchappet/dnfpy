import numpy as np

from dnfpy.core.mapND import MapND
import dnfpy.core.utilsND as utils
class BarycenterMap(MapND):
        """
        Input: 
            map : map (child)
        Output:
            coordinate of the barycenter normalized (tuple of size dim) 

        """
        def __init__(self,name,dim=1,dt=0.1,**kwargs):
                super(BarycenterMap,self).__init__(name=name,size=0,dim=dim,dt=dt,a=np.nan,**kwargs)
                self.shapeMap = ()
                self.setArg(a=np.nan)


        def _compute(self,map,dim):
                
                self.shapeMap = map.shape
                size = self.shapeMap[0]
                coords = np.where(map != np.inf)
                sumMap = np.sum(map)
                if sumMap == 0:
                        bary = (np.nan,)*dim
                else:
                    bary = []
                    #for coord,i in zip(coords,range(len(coords))):
                    #    bary.append((np.sum(coord*map.reshape(map.size))/sumMap)/self.shapeMap[i])
                    coord = np.where(map == 1 )
                    coordStart = np.array(coord)[:,0]
                    #print("coordStart")
                    #print(coordStart)
                    dist = utils.generateWrappedDistance(size,coordStart,True)

                    dist.reverse()
                    distGrid = np.meshgrid(*dist)
                    #print("dist : ")
                    #print(dist)
                    distMin = []
                    distMax = []
                    for i in range(dim):
                        mean = np.mean(distGrid[-(1 + i)][coord])
                        bary.append(((coordStart[i] + mean + size) % size)/size)

                        distMin.append(np.nanmin(distGrid[-(1+i)][coord]))
                        distMax.append(np.nanmax(distGrid[-(1+i)][coord]))


                    bary.reverse()


                    distMin = np.array(distMin)
                    distMax = np.array(distMax)
                    #print(distMin," ",distMax)
                    self.setArg(a = (distMax - distMin)/size)
                    #print(self.getArg('a'))
                   
                

                self._data = np.array(bary)

        def getViewSpace(self):
                return (1,)*self.getArg('dim')

                


        




