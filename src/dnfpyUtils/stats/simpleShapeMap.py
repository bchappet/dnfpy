import numpy as np

from dnfpy.core.mapND import MapND
import dnfpy.core.utils as utils
class SimpleShapeMap(MapND):
        """
        Param:
            1)convTime float in second. The shape is zero for convTime seconds
            2)shapeThreshold : threshold of input shape
            3) wm : bool if true the shape will disapear when intensity of input track is 0
        Children:
            1)targetList : list of target index to follow : list of int 
            3)inputMap: the input map 
        Output:
            A sizexsize array of reals. It is the theoric shape of activation.
            
        Special cases:

        Notes: 
        We don't take the intensity of the input into account we suppose it is always 1.0


        Methods:
        eraseShape() erase the shape with the speed tau

        """
        def __init__(self,name,size,dim=1,shapeThreshold=0.6,dt=0.1,convTime=1.2,wm=False,tau=1.2,**kwargs):
                super(SimpleShapeMap,self).__init__(name=name,size=size,dim=dim,dt=dt,shapeThreshold=shapeThreshold,
                                convTime=convTime,wm=wm,tau=tau,erase=False,**kwargs)
                self.inputMap = None
                self.iShape = 1.0

        def _compute(self,size,targetList,shapeThreshold,dim,time,convTime,wm,tau,erase,dt):
                if erase:
                        self.iShape += dt/tau*(-self.iShape)

                if time > convTime:
                    #1) Reconstruct the input with intensity = 1
                    trackedInput = np.zeros((size,)*dim)
                    for targetIndex in targetList:
                        track = self.inputMap.getChild("Inputs_track"+str(targetIndex))
                        center = track.getCenter()
                        intensity,width = track.getShape() #the intensity does not change the shape 
                        wrap = track.getArg('wrap')

                        #if not(wm) and intensity < 10e-5:
                           #no memory, the bubble disapear when intensity is 0
                        #   pass
                        #else:
                        trackedInput += utils.gaussNd(size,wrap,self.iShape,width,center)

                    #2)Construct the shape
                    self._data = np.where(trackedInput >= shapeThreshold,1.0,0.0)
                else:
                    self._data= np.zeros((size,)*dim)

        def eraseShape(self):
                self.setArg(erase=True)


        def _onAddChildren(self,**kwargs):
                """
                We add the input map as attribute

                """
                try:
                    self.inputMap = kwargs['inputMap']
                except:
                    pass




