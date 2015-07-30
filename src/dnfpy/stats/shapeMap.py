from dnfpy.core.map2D import Map2D
from scipy.spatial import distance
import numpy as np
import dnfpy.core.utils as utils

class ShapeMap(Map2D):
    """
    Given the tracked stimulus, gives the theoretical shape of the potential field
    Children:
        tracksCenter= TrackedMap (to get coordinate of tracked stim)
        inputMap is a map where we can getParams: wStim_

    Params:
        shapeType: in ['exp','gauss'] shape of the excitatory lateral weights

    """
    def __init__(self,name,size=1,dt=0.1,
                wrap = True,
                shapeType = 'gauss',
                wStim = 1.,
                **kwargs):
        super(ShapeMap,self).__init__(name=name,size=size,dt=dt,wrap=wrap,
                                      shapeType=shapeType,
                                      **kwargs)
        self.latMap = None #will be set on add children

    def _compute(self,size,wrap,shapeType,tracksCenter):
        self._data = np.zeros((size,size))
        for trackCenter in tracksCenter:
            #print("trackCenter %s"%trackCenter)
            if len(trackCenter) < 2 or np.all(trackCenter == [-1,-1]):
                #No tracked stim
                pass
            else:
                #We can generate the theoritical shape
                #iExc = self.latMap.getArg('iExc_')
                #iInh = self.latMap.getArg('iInh_')
                wStim = self.inputMap.getWidth()
                iStim = 1
                #scalingFactor = wStim/(iExc-iInh)
                #print("scaling factor : %s"%scalingFactor)
                #if shapeType == 'gauss':
                #    wExc = self.latMap.getArg('wExc_')
                    #wInh = self.latMap.getArg('wInh_')
                excLat = utils.gauss2d(size,wrap,iStim,wStim,trackCenter[0],trackCenter[1])
                    #inhLat = utils.gauss2d(size,wrap,iInh,wInh,trackCenter[0],trackCenter[1])
                self._data +=  np.where(excLat>0.65,1,0)
                #else:
                 #   pExc = self.latMap.getArg('pExc_')
                    #pInh = self.latMap.getArg('pInh_')
                  #  excLat = utils.exp2d(size,wrap,iExc,pExc,trackCenter[0],trackCenter[1])
                    #inhLat = utils.exp2d(size,wrap,iInh,pInh,trackCenter[0],trackCenter[1])
                   # self._data +=  2/iExc *  excLat**1.4


    def _onAddChildren(self,**kwargs):
        """
        expect tracksCenter  latMap inputsMap
        """
        self.inputMap = kwargs["inputMap"]






