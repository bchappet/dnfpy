import dnfpy.core.utils as utils
from dnfpy.core.map2D import Map2D
from dnfpy.core.funcMap2D import FuncMap2D
import cv2

class LateralWeightsMap(Map2D):
    def __init__(self,size,kernelType,**kwargs):
        super(LateralWeightsMap,self).__init__(size,kernelType=kernelType,**kwargs)
        center = (size - 1)/2
        dt_max = 1e20 
        if kernelType == 'gauss':
            kernelExc = FuncMap2D(utils.gauss2d,size,dt=dt_max,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',width='wExc')
            kernelInh = FuncMap2D(utils.gauss2d,size,dt=dt_max,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',width='wInh')
        elif kernelType == 'exp':
            kernelExc = FuncMap2D(utils.exp2d,size,dt=dt_max,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap',intensity='iExc',proba='pExc')
            kernelInh = FuncMap2D(utils.exp2d,size,dt=dt_max,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap',intensity='iInh',proba='pInh')
        else:
                print("Error bad kernel param %s"%kernelType)
        
        self.kernel = FuncMap2D(utils.subArrays,size,dt=dt_max)
        self.kernel.addChildren(a=kernelExc,b=kernelInh)

        self.addChildren(kernel=self.kernel)

    def _compute(self,act,kernel,wrap):
        if wrap:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT
        self._data = cv2.filter2D(act,-1,cv2.flip(kernel,-1),anchor=(-1,-1),borderType=border)

    def _onParamUpdate(self):
        self.kernel.artificialRecursiveComputation()

    def _modifyParamsRecursively(self,params):
        size = params['size']
        params['wInh'] *= size
        params['wExc'] *= size

        alpha = params['alpha']

        params['iExc'] = params['iExc']/(size**2) * (40**2)/alpha
        params['iInh'] = params['iInh']/(size**2) * (40**2)/alpha

        params['pExc'] = params['pExc']**(1./size)
        params['pInh'] = params['pInh']**(1./size)









