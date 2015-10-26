import numpy as np

from dnfpy.core.map2D import Map2D
import dnfpy.core.utils as utils
class ModelMap(Map2D):
        """
        Input: 
            1)targetList : list of target index to follow : list of int (children)
            2)activationSize : expected activation bubble size (constructor)
            3)inputMap: the input map (constructor)
        Output:
            A sizexsize array of reals. It is the theoric shape of activation.
            
        Special cases:

        Notes: 
        We don't take the intensity of the input into account:
        We suppose that every input intensity is 1 EVEN IF it is 0.
        """
        def __init__(self,name,size,inputMap,shapeThreshold=0.4,dt=0.1,**kwargs):
                super(SimpleShapeMap,self).__init__(name=name,size=size,dt=dt,shapeThreshold=shapeThreshold,**kwargs)
                self.inputMap = inputMap

        def _compute(self,size,targetList,shapeThreshold):
                #1) Reconstruct the input with intensity = 1
                trackedInput = np.zeros((size,size))
                for targetIndex in targetList:
                        track = self.inputMap.getChild("Inputs_track"+str(targetIndex))
                        center = track.getCenter()
                        intensity,width = track.getShape() #the intensity does not change the shape 
                        wrap = track.getArg('wrap')
                        trackedInput += utils.gauss2d(size,wrap,1,width,center[0],center[1])

                #2)Construct the shape
                self._data = np.where(trackedInput >= shapeThreshold,1.0,0.0)




