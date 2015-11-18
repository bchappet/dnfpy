from dnfpy.model.activationMapND import ActivationMapND
import numpy as np
from dnfpy.model.fieldMapND import FieldMapND
from dnfpy.model.lateralWeightsMapSpace import LateralWeightsMapSpace
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.core.constantMapND import ConstantMapND
import matplotlib.pyplot as plt

class MapDNFSpace(FieldMapND):
    """
    lateral: 'dog','doe','dol' difference of gaussian, difference of exponential or diferrence of linear function
    fashion : 'chappet,'fix' fix fashion is designed to have similar parameters for the kernels
    """
    def __init__(self,name,size,dim,space,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 model='cnft',th=0.75,delta=1.,activation='step',
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=1,alpha=10,
                 mapSize=1.,nbStep=0,noiseI=0.0,lateral='dog',
                 fashion='fix',globalInh=0.0,
                 **kwargs):
        super().__init__(name,size=size,dim=dim,dt=dt,wrap=wrap,
                    tau=tau,h=h,delta=delta,
                    model=model,th=th,activation=activation,
                    noiseI=noiseI,lateral=lateral,globalInh=globalInh,
                    **kwargs)

        self.act = ActivationMapND("Activation",size,dim=dim,dt=dt,type=activation,th=th)
        self.lat = ConvolutionND("Lateral",size,dim=dim,dt=dt,wrap=wrap)

        self.kernel = LateralWeightsMapSpace(name+"Kernel",space=space,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep,
                                        fashion=fashion,lateral=lateral,globalInh=globalInh)
 
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(source=self.act,kernel=self.kernel)

    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
        ]


if __name__ == "__main__":
        import math
        size = 101
        dim = 1
        shape = (size,)*dim
        dt = 0.1
        time = 0
        
        xStart = -10
        xEnd = 10

        size = int(((math.floor(size/2.)) * 2) + 1)#Ensure size is odd for convolution
        #Define the space matrix:
        axis = np.linspace(xStart,xEnd, size)
        axiss = [axis]*dim
        space = np.meshgrid(*axiss)
        x = space[0]


        [iExc,wExc,iInh,wInh] = [1.0, 2.5, 0.5, 4.0]
        dnf = MapDNFSpace("uut",size,dim=dim,space=space,fashion='fix',iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh);
        inputArray = np.zeros(shape);
        input = ConstantMapND("input",size,inputArray)

        dnf.addChildren(aff=input)
        dnf.kernel.kernelExc.compute()
        dnf.kernel.kernelInh.compute()
        dnf.kernel.compute()


        inputArray[(size/2,)*dim] = 1
        inputArray[(size/2-1,)*dim] = 1
        inputArray[(size/2+1,)*dim] = 1
        for i in range(100):
            time += dt
            dnf.act.update(time)
            #print("DNF" , dnf.getData())
            #print("ACT" , dnf.act.getData())

        plt.subplot(221)
        plt.plot(x,dnf.getData())
        plt.title("DNF")
        plt.subplot(222)
        plt.plot(x,dnf.act.getData())
        plt.title("ACT")
        plt.subplot(223)
        plt.plot(x,dnf.lat.getData())
        plt.title("LAT")
        plt.subplot(224)
        plt.plot(x,dnf.kernel.getData())
        plt.title("KER")
        plt.show()





