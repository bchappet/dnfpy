import numpy as np
from dnfpy.view.renderable import Renderable
from dnfpy.model.model import Model
from dnfpy.model.activationMapND import ActivationMap
from dnfpy.core.constantMapND import ConstantMap
from dnfpy.model.kernelConvolution import KernelConvolution
from dnfpy.model.fieldMapND import FieldMap

def getTemplate(name='edge'):
    """
    Return a tup A,B <=> latKernel,affKernel
    """
    if name == 'edge':
        latKernel=[[-1,-1,-1],
                   [-1, 8,-1],
                   [-1,-1,-1]]
        affKernel=[[ 0, 0, 0],
                   [ 0, 2, 0],
                   [ 0, 0, 0]]
    elif name == 'diff':
        latKernel=[[0, 1, 0],
                   [1,-4, 1],
                   [0, 1, 0]]
        affKernel=[[0, 0, 0],
                   [0, 1, 0],
                   [0, 0, 0]]
    else:
        raise Exception("name " + name + " does not match")

    latKernel = np.array(latKernel).astype(np.float)
    affKernel = np.array(affKernel).astype(np.float)
    return latKernel,affKernel

    



class CnnMap(FieldMap):
    def __init__(self,name,size=49,dt=0.1,dim=2,wrap=True,model='cnft',
            latMode='constant',affMode='constant',
            affKernel=[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],
            latKernel=[[ 0, 0, 0],[ 0,2, 0],[ 0, 0, 0]],
            tau=1,h=0,leak=0,activation='cnn',
            **kwargs):
        super().__init__(name,size,dim=dim,dt=dt,wrap=wrap,model=model,
                latMode=latMode,affMode=affMode,leak=leak,activation=activation,
                **kwargs)
        print('z',h,'leak',leak,'act',activation)
        self.act = ActivationMap(name+"_act",size,dt=dt,dim=dim,type=activation)
        self.act.addChildren(field=self)

        self.lat = KernelConvolution(name+"_lat",size,dt=dt,dim=dim,wrap=wrap,
                lateral=latMode,value=np.array(latKernel))
        self.aff = KernelConvolution(name+"_aff",size,dt=dt,dim=dim,wrap=wrap,
                lateral=affMode,value=np.array(affKernel))

        self.lat.addChildren(source=self.act)
        self.addChildren(aff=self.aff,lat=self.lat)
        




class Cnn(Model,Renderable):
    def initMaps(self,size=49,dt=0.1,dim=2,wrap=True,
            tau=1.0,h=-1,leak=1.0,
            template="edge",activation='cnn',
            **kwargs):
        latMode='constant'
        affMode='constant'
        latKernel,affKernel = getTemplate(template)

        self.field = CnnMap("cnn",size,dt,dim,wrap,model='cnft',
                latMode=latMode,affMode=affMode,activation=activation,
                latKernel=latKernel,affKernel=affKernel,
                tau=tau,h=h,leak=leak)
        return [self.field,]

    def getArrays(self):
        ret =  [self.field,self.field.act]
        return ret

    #override Model
    def onAfferentMapChange(self,afferentMap):
        self.field.aff.addChildren(source=afferentMap)

    def onClick(self,mapName,x,y):
        print("clicked on %s, at coord %s,%s"%((mapName),x,y))
