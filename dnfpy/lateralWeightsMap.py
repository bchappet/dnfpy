import utils
import cv2
from map2D import Map2D
from funcMap2D import FuncMap2D
class LateralWeightsMap(Map2D):
    def __init__(self,size,dt,globalRealParams):
        super(LateralWeightsMap,self).__init__(size,dt,globalRealParams)
        center = (size - 1)/2
        dtKern = 1e30
        latKernel = self.globalRealParams['lateralWKernel']
        if latKernel == 'gauss':
            kernelExc = FuncMap2D(size,dtKern,globalRealParams,utils.gauss2d,{'size':size,'centerX':center,'centerY':center})
            kernelExc.registerOnGlobalParamsChange({'wrap':'wrap','intensity':'iExc','width':'wExc'})
            kernelInh = FuncMap2D(size,dtKern,globalRealParams,utils.gauss2d,{'size':size,'centerX':center,'centerY':center})
            kernelInh.registerOnGlobalParamsChange({'wrap':'wrap','intensity':'iInh','width':'wInh'})
        elif latKernel == 'exp':
            kernelExc = FuncMap2D(size,dtKern,globalRealParams,utils.exp2d,{'size':size,'centerX':center,'centerY':center})
            kernelExc.registerOnGlobalParamsChange({'wrap':'wrap','intensity':'iExc','proba':'pExc'})
            kernelInh = FuncMap2D(size,dtKern,globalRealParams,utils.exp2d,{'size':size,'centerX':center,'centerY':center})
            kernelInh.registerOnGlobalParamsChange({'wrap':'wrap','intensity':'iInh','proba':'pInh'})
        else:
                print("Error bad kernel param %s"%latKernel)
        
        kernel = FuncMap2D(size,dtKern,globalRealParams,utils.subArrays)
        kernel.addChildren({'a':kernelExc,'b':kernelInh})
        kernelExc.compute()
        kernelInh.compute()
        kernel.compute()

        self.addChildren({'kernel':kernel})
    def compute(self):
        super(LateralWeightsMap,self).compute()
        act = self.children['activation'].getData()
        kernel = self.children['kernel'].getData()
        
        if self.globalRealParams['wrap']:
            border = cv2.BORDER_WRAP
        else:
            border = cv2.BORDER_DEFAULT
        self.lat = cv2.filter2D(act,-1,cv2.flip(kernel,-1),anchor=(-1,-1),borderType=border)

