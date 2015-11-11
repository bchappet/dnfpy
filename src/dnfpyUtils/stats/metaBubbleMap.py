import numpy as np

from dnfpy.core.mapND import MapND
import dnfpy.core.utilsND as utils
class MetaBubbleMap(MapND):
        """
        Input: 
            metaModel : map (child) the position of the model bubble
            activationMap : map (constructor) to get the parameters of activation

            width : float size of the artificial activation (constructor)
        Output:
            a map of size size and dimension dim creating an artificial activation (1) at the position
            given by the meta model
        """
        def __init__(self,name,size,activationMap,dim=1,dt=0.1,wrap=True,width=0.2,**kwargs):
                super(MetaBubbleMap,self).__init__(name=name,size=size,dim=dim,dt=dt,width=width,wrap=wrap,**kwargs)
                self.activationMap = activationMap


        def _compute(self,metaModel,width,size,dim,wrap):
                gauss = utils.gaussNd(size,wrap,1,width*size,metaModel*size)
                args = self.activationMap.getArgs('type','th','beta','dtype')
                args['th'] = 0.6
                self._data = self.activationMap.activation(gauss,**args)
                






        




