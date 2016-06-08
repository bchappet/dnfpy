import numpy as np
from scipy import ndimage
from dnfpy.core.constantMapND import ConstantMap
from scipy import misc
from dnfpyUtils.scenarios.scenario import Scenario
"""
Load a static image
"""
def to_gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

class Constant(Scenario):
    def initMaps(self,size=49,dim=2,file="data/dice.jpg",timeStop=0.2,constant=0,**kwargs):
        self.timeStop = timeStop
        try:
            im = misc.imread(file)
        except Exception as e:
            print(e)
            im = misc.face()
        im = misc.imresize(im,(size,size))
        gray = to_gray(im)
        value = (gray/255-0.5)*2

        self.input = ConstantMap("picture",size=size,value=value)
        return [self.input]

    def _apply(self):
        if self.isTime(self.timeStop):
            size ,dim,constant = self.getArgs('size','dim','constant')
            self.input.setData(np.ones((size,)*dim)*constant)

        
 
