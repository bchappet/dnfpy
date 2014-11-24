import utils
import cv2
from map2D import Map2D
from funcMap2D import FuncMap2D

class LateralWeightsMap(Map2D):
    DT_MAX = 1e30 #global constant for the static map: they will not be updated
    def __init__(self,size,kernelType,**kwargs):
        super(LateralWeightsMap,self).__init__(size,kernelType=kernelType,**kwargs)
        center = (size - 1)/2
        
        if kernelType == 'gauss':
            kernelExc = FuncMap2D(utils.gauss2d,size,dt=LateralWeightsMap.DT_MAX,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',width='wExc')
            kernelInh = FuncMap2D(utils.gauss2d,size,dt=LateralWeightsMap.DT_MAX,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',width='wInh')
        elif kernelType == 'exp':
            kernelExc = FuncMap2D(utils.exp2d,size,dt=LateralWeightsMap.DT_MAX,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',proba='pExc')
            kernelInh = FuncMap2D(utils.exp2d,size,dt=LateralWeightsMap.DT_MAX,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',proba='pInh')
        else:
                print("Error bad kernel param %s"%kernelType)
        
        kernel = FuncMap2D(utils.subArrays,size,dt=LateralWeightsMap.DT_MAX)
        kernel.addChildren(a=kernelExc,b=kernelInh)

        self.addChildren(kernel=kernel)
        self._setArg(dt=LateralWeightsMap.DT_MAX)

    def _compute(self,act,kernel,wrap):
        if wrap:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT
        self._data = cv2.filter2D(act,-1,cv2.flip(kernel,-1),anchor=(-1,-1),borderType=border)

    def _modifyParamsRecursively(self,params):
        size = params['size']
        params['wInh'] *= size
        params['wExc'] *= size

        alpha = params['alpha']

        params['iExc'] = params['iExc']/(size**2) * (40**2)/alpha
        params['iInh'] = params['iInh']/(size**2) * (40**2)/alpha

        params['pExc'] = params['pExc']**(1./size)
        params['pInh'] = params['pInh']**(1./size)









