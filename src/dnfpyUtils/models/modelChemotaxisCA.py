from dnfpy.model.model import Model
import numpy as np
from dnfpy.view.renderable import Renderable

from dnfpy.core.constantMapND import ConstantMapND
from dnfpyUtils.cellular.diffusionCA import DiffusionCA
from dnfpyUtils.cellular.amoebaeCA import AmoebaeCA

from dnfpy.view.multipleData import MultipleData

import scipy.ndimage

def loadMap(size,file):
        data = np.loadtxt(file,delimiter=',')
        #interpolate data to fit the size
        factor = size/data.shape[0]
        map = scipy.ndimage.zoom(data,factor,order=0) #nearest interp
        return map




class ModelChemotaxisCA(Model,Renderable):


    def initMaps(self,size,**kwargs):

            target = np.zeros((size,size)).astype(np.bool_)
            target[size//3,size//3] = 1

            obstacle = np.zeros((size,size)).astype(np.bool_)
            obstacle = loadMap(size,"files/maze.csv").astype(np.bool_)
            #add border 1px
            borderPx = 3
            obstacle[:,:borderPx] = True
            obstacle[:,-borderPx:] = True
            obstacle[:borderPx,:] = True
            obstacle[-borderPx:,:] = True


            targetMap = ConstantMapND("Target",size,value=target)
            obstacleMap = ConstantMapND("Obstacle",size,value=obstacle)

            m = 4

            diffusionMap = DiffusionCA("Diffusion",size,m=m,pt = 1)
            diffusionMap.addChildren(activation=targetMap,obstacle=obstacleMap)


            self.amoebaeCA = AmoebaeCA("Amoebae",size,m=m,pa=0.1)
            self.amoebaeCA.addChildren(obstacle=obstacleMap,diffusion=diffusionMap)


            self.diffusionMap = diffusionMap
            self.obstacleMap = obstacleMap
            self.targetMap = targetMap

            self.viewMap = MultipleData("World",size=size,dim=2,dt=0.1)
            self.viewMap.addMaps(self.amoebaeCA,self.diffusionMap,self.obstacleMap,self.targetMap)
            self.viewMap.setColors(["green","red","black","blue"])


            return [self.amoebaeCA,self.viewMap]



    def getArrays(self):
            #return [self.amoebaeCA,self.diffusionMap,self.obstacleMap,self.targetMap]
            return [self.viewMap]


    def onClick(self,mapName,x,y):
            if mapName=="World":
                self.amoebaeCA.onClick(x,y)
                ret = (self.amoebaeCA,self.getMap(mapName))
                return ret
            else:
                map = self.getMap(mapName)
                map.onClick(x,y)
                return map
            
