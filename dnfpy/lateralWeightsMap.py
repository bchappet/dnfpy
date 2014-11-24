import utils
import cv2
from map2D import Map2D
from funcMap2D import FuncMap2D
class LateralWeightsMap(Map2D):
    def __init__(self,size,kernelType):
        super(LateralWeightsMap,self).__init__(size,kernelType=kernelType)
        center = (size - 1)/2
        dtKern = 1e30
        if kernelType == 'gauss':
            kernelExc = FuncMap2D(utils.gauss2d,size,dt=dtKern,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',width='wExc')
            kernelInh = FuncMap2D(utils.gauss2d,size,dt=dtKern,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',width='wInh')
        elif kernelType == 'exp':
            kernelExc = FuncMap2D(utils.exp2d,size,dt=dtKern,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',proba='pExc')
            kernelInh = FuncMap2D(utils.exp2d,size,dt=dtKern,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',proba='pInh')
        else:
                print("Error bad kernel param %s"%kernelType)
        
        kernel = FuncMap2D(utils.subArrays,size,dt=dtKern)
        kernel.addChildren(a=kernelExc,b=kernelInh)

        self.addChildren(kernel=kernel)
        self._setArg(dt=dtKern)

    def _compute(self,act,kernel,wrap):
        if wrap:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT
        self.lat = cv2.filter2D(act,-1,cv2.flip(kernel,-1),anchor=(-1,-1),borderType=border)

