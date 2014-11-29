import dnfpy.core.utils as utils
from dnfpy.core.funcMap2D import FuncMap2D
from dnfpy.core.map2D import Map2D
import cv2

class LateralWeightsMap(FuncMap2D):
    """
        Return a gaussian or exponential kernel
    """
    def __init__(self,size,kernelType='gauss',term='',**kwargs):
        super(LateralWeightsMap,self).__init__(utils.subArrays,size,kernelType=kernelType,**kwargs)
        center = (size - 1)/2
        self.term = term #self.terminaison of the parameters
        if kernelType == 'gauss':
            kernelExc = FuncMap2D(utils.gauss2d,size,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap'+self.term,intensity='iExc'+self.term,width='wExc'+self.term,dt='kernel_dt')
            kernelInh = FuncMap2D(utils.gauss2d,size,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap'+self.term,intensity='iInh'+self.term,width='wInh'+self.term,dt='kernel_dt')
        elif kernelType == 'exp':
            kernelExc = FuncMap2D(utils.exp2d,size,centerX=center,centerY=center)
            kernelExc.registerOnGlobalParamsChange(wrap='wrap'+self.term,intensity='iExc'+self.term,proba='pExc'+self.term,dt='kernel_dt')
            kernelInh = FuncMap2D(utils.exp2d,size,centerX=center,centerY=center)
            kernelInh.registerOnGlobalParamsChange(wrap='wrap'+self.term,intensity='iInh'+self.term,proba='pInh'+self.term,dt='kernel_dt')
        else:
                print("Error bad kernel param %s"%kernelType)
        
        self.addChildren(a=kernelExc,b=kernelInh)

    def _modifyParamsRecursively(self,params):
        size = params['size'] #relatively to general size
        params['wInh'+self.term] *= size
        params['wExc'+self.term] *= size

        alpha = params['alpha'+self.term]

        params['iExc'+self.term] = params['iExc'+self.term]/(size**2) * (40**2)/alpha
        params['iInh'+self.term] = params['iInh'+self.term]/(size**2) * (40**2)/alpha

        params['pExc'+self.term] = params['pExc'+self.term]**(1./size)
        params['pInh'+self.term] = params['pInh'+self.term]**(1./size)


