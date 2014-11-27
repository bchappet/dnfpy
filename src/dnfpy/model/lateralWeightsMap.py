import dnfpy.core.utils as utils
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.core.map2D import Map2D
import cv2

class LateralWeightsMap(FuncMap2D):
    """
        Return a gaussian or exponential kernel
    """
    def __init__(self,size,kernelType,**kwargs):
        super(LateralWeightsMap,self).__init__(utils.subArrays,size,kernelType=kernelType,**kwargs)
        center = (size - 1)/2
        if kernelType == 'gauss':
            kernelExc = FuncMap2D(utils.gauss2d,size,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',width='wExc',dt='kernel_dt')
            kernelInh = FuncMap2D(utils.gauss2d,size,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',width='wInh',dt='kernel_dt')
        elif kernelType == 'exp':
            kernelExc = FuncMap2D(utils.exp2d,size,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',proba='pExc',dt='kernel_dt')
            kernelInh = FuncMap2D(utils.exp2d,size,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',proba='pInh',dt='kernel_dt')
        else:
                print("Error bad kernel param %s"%kernelType)
        
        self.addChildren(a=kernelExc,b=kernelInh)

    def _modifyParamsRecursively(self,params):
        size = params['size']
        params['wInh'] *= size
        params['wExc'] *= size

        alpha = params['alpha']

        params['iExc'] = params['iExc']/(size**2) * (40**2)/alpha
        params['iInh'] = params['iInh']/(size**2) * (40**2)/alpha

        params['pExc'] = params['pExc']**(1./size)
        params['pInh'] = params['pInh']**(1./size)


