# -*- coding: utf-8 -*-
import numpy as np
from dnfpy.cellular.cellularMap import CellularMap
import dnfpy.core.utils as utils
import cv2
from dnfpy.core.map2D import Map2D
import scipy.misc


#spots
#!python main.py ModelCellular 301 0.3 "{'model':'TuringPatterns','radius':0.1,'delta':10,'threshold':1.0}"
#small stripes
#!python main.py ModelCellular 501 0.3 "{'model':'TuringPatterns','radius':0.03,'delta':7,'threshold':0.2}"

#moving
#!python main.py ModelCellular 501 0.3 "{'model':'TuringPatterns','radius':0.05,'delta':10,'threshold':0.4,'shiftY':0.03,'shiftX':0.03}"

#without random
#!python main.py ModelCellular 501 0.3 "{'model':'TuringPatterns','radius':0.03,'delta':13,'threshold':0.3,'shiftY':0.02,'shiftX':0.00}"



class KernelMap(Map2D):
    def __init__(self,name,size,dt=1e10,radius=0.1,shiftX=0.,shiftY=0.):
        super(KernelMap,self).__init__(name,size,dt=dt,dtype=np.int32,
        radius=radius,shiftX=shiftX,shiftY=shiftY,radius_=1,shiftX_=1,shiftY_=1)


    def _onParamsUpdate(self,size,radius,shiftX,shiftY):
        radius_ = radius * size
        shiftX_ = shiftX * size
        shiftY_ = shiftY * size
        return dict(radius_=radius_,shiftX_=shiftX_,shiftY_=shiftY_)


    def _compute(self,size,radius_,shiftX_,shiftY_):
        #size should be odd
        middle = (size -1) / 2
        gauss = utils.gauss2d(size,False,1,radius_,middle+shiftY_,middle+shiftX_)
        self._data = np.where(gauss > 0.5,1,0)
        self._data.astype(np.int32,copy=False)





class TuringPatterns(CellularMap):
    def __init__(self,name,size,dt=0.1,wrap=False,threshold=1.,delta=7,radius=0.1,shiftX=0.00,shiftY=0.00,maximum=255,**kwargs):
        super(TuringPatterns,self).__init__(name=name,size=size,dt=dt,
        dtype=np.int32,threshold=threshold,radius=radius,
            wrap = wrap,threshold_=1,delta=delta,
            maximum = maximum,
            **kwargs)

        self.kernel = KernelMap("kernel",size,dt=dt,radius=radius,shiftX=shiftX,shiftY=shiftY)
        self.addChildren(kernel=self.kernel)

    def init(self,size):
        X = np.zeros((size,size),dtype=np.int32)
        self.init2(size,X)
        return X

    def init2(self,size,X):
        pass
        #X += np.random.randint(0,255,(size,size)).astype(np.int32)
        #data = scipy.misc.lena()
        #X += data


    def _onParamsUpdate(self,size,threshold):
        threshold_ = float(threshold) * (size**2)
        return dict(threshold_=threshold_)


    def _compute(self,wrap,kernel,threshold_,delta,maximum):
        if wrap:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT

        sumNeighs = cv2.filter2D(self._data,-1,cv2.flip(kernel,-1),
                                  anchor=(-1,-1),borderType=border)
        #print threshold_
        deltaArr = np.where(sumNeighs>threshold_,-delta,+delta)
        self._data += deltaArr
        np.clip(self._data,0,maximum,self._data)



    def onClick(self,x,y):
        maximum = self.getArg('maximum')
        radius = self.getArg('radius')
        size = self.getArg('size')
        gauss = utils.gauss2d(size,False,1,radius*size,x,y)
        spot = np.where(gauss > 0.5,maximum,0)

        #data = scipy.misc.lena()
        self._data += spot
        np.clip(self._data,0,maximum,self._data)




