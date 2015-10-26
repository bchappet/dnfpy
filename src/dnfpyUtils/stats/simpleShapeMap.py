import numpy as np

from dnfpy.core.mapND import MapND
import dnfpy.core.utilsND as utils
class SimpleShapeMap(MapND):
        """
        Input: 
            1)targetList : list of target index to follow : list of int (children)
            2)shapeThreshold : threshold of input shape (constructor)
            3)inputMap: the input map (constructor)
        Output:
            A sizexsize array of reals. It is the theoric shape of activation.
            
        Special cases:

        Notes: 
        We don't take the intensity of the input into account:
        We suppose that every input intensity is 1 EVEN IF it is 0.
        """
        def __init__(self,name,size,inputMap,dim=1,shapeThreshold=0.4,dt=0.1,**kwargs):
                super(SimpleShapeMap,self).__init__(name=name,size=size,dim=dim,dt=dt,shapeThreshold=shapeThreshold,**kwargs)
                self.inputMap = inputMap

        def _compute(self,size,targetList,shapeThreshold,dim):
                #1) Reconstruct the input with intensity = 1
                trackedInput = np.zeros((size,)*dim)
                for targetIndex in targetList:
                        track = self.inputMap.getChild("Inputs_track"+str(targetIndex))
                        center = track.getCenter()
                        intensity,width = track.getShape() #the intensity does not change the shape 
                        wrap = track.getArg('wrap')
                        
                        trackedInput += utils.gaussNd(size,wrap,1,width,center)

                #2)Construct the shape
                self._data = np.where(trackedInput >= shapeThreshold,1.0,0.0)




