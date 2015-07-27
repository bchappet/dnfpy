# -*- coding: utf-8 -*-
import math
import numpy as np
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
import cv2
from dnfpy.core.map2D import Map2D
from dnfpy.model.multiLayerMap import MultiLayerMap

#spots
#!python main.py ModelCellular 301 0.3 "{'model':'TuringPatterns','radius':0.1,'delta':10,'threshold':1.0}"
#small stripes
#!python main.py ModelCellular 501 0.3 "{'model':'TuringPatterns','radius':0.03,'delta':7,'threshold':0.2}"

#moving
#!python main.py ModelCellular 501 0.3 "{'model':'TuringPatterns','radius':0.05,'delta':10,'threshold':0.4,'shiftY':0.03,'shiftX':0.03}"

#without random
#!python main.py ModelCellular 501 0.3 "{'model':'TuringPatterns2','radius':0.03,'delta':13,'threshold':0.3,'shiftY':0.02,'shiftX':0.00,'colTh':180}"


#TODO we can have a smaller kernel
class KernelMap(Map2D):
    def __init__(self,name,size,globalSize,dt=1e10,radius=0.1,shiftX=0.,shiftY=0.,mapSize=1):
        super(KernelMap,self).__init__(name,size,dt=dt,dtype=np.int32,globalSize=globalSize,mapSize=mapSize,
        radius=radius,shiftX=shiftX,shiftY=shiftY,radius_=1,shiftX_=1,shiftY_=1)


    def _onParamsUpdate(self,size,radius,shiftX,shiftY,mapSize,globalSize):
        size = mapSize * globalSize
        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure odd
        radius_ = radius * globalSize
        shiftX_ = shiftX * globalSize
        shiftY_ = shiftY * globalSize
        return dict(radius_=radius_,shiftX_=shiftX_,shiftY_=shiftY_,size=size)


    def _compute(self,size,radius_,shiftX_,shiftY_):
        #size should be odd
        middle = (size -1) / 2
        gauss = utils.gauss2d(size,False,1,radius_,middle+shiftY_,middle+shiftX_)
        self._data = np.where(gauss > 0.5,1,0)
        self._data.astype(np.int32,copy=False)





class TuringPatterns2(MultiLayerMap):
    def __init__(self,name,size,dt=0.1,wrap=False,threshold=1.,delta=7,radius=0.1,shiftX=0.00,shiftY=0.00,
                 nbCol=4,colTh=125,**kwargs):
        super(TuringPatterns2,self).__init__(name=name,size=size,dt=dt,
        dtype=np.int32,threshold=threshold,radius=radius,
            wrap = wrap,threshold_=1,delta=delta,
            nbCol=nbCol,colTh=colTh,
            **kwargs)

        sizeK = int(radius*size)
        self.kernel = KernelMap("kernel",sizeK,mapSize=0.2,globalSize=size,dt=dt,radius=radius,shiftX=shiftX,shiftY=shiftY)
        self.addChildren(kernel=self.kernel)

    def initModel(self,size):
        X = np.zeros((size,size),dtype=np.int32)
        self.init2(size,X)
        return X

    def init2(self,size,X):
        X += np.random.randint(0,100,(size,size)).astype(np.int32)

    def getType(self):
        pass
        #return 'binary'

    def _onParamsUpdate(self,size,threshold):
        threshold_ = float(threshold) * (size**2)
        return dict(threshold_=threshold_)


    def _compute(self,wrap,kernel,threshold_,delta):
        if wrap:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT

        sumNeighs = cv2.filter2D(self._data,-1,cv2.flip(kernel,-1),
                                  anchor=(-1,-1),borderType=border)
        #print threshold_
        deltaArr = np.where(sumNeighs>threshold_,-delta,+delta)
        self.updateColors(self._data,neighType='conv',kernel=kernel,borderType=border)
        self._data += deltaArr
        np.clip(self._data,0,255,self._data)
        self.eraseColorThreshold(self._data)



    def onClick(self,x,y):
        radius = self.getArg('radius')
        size = self.getArg('size')
        gauss = utils.gauss2d(size,False,1,radius/2.*size,x,y)
        spot = np.where(gauss > 0.5,255,0)
        spot.astype(np.int32,copy=False)
        self._data += spot
        np.clip(self._data,0,255,self._data)
        self.colorise(spot,True)

