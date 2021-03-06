from dnfpy.model.activationMapND import ActivationMapND
import numpy as np
from dnfpy.model.fieldMapND import FieldMapND
from dnfpy.model.lateralWeightsMapND import LateralWeightsMapND
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.core.constantMapND import ConstantMapND
from dnfpy.model.lateralWeightsDiff import LateralWeightsDiff
import matplotlib.pyplot as plt

class MapCNNDNF(FieldMapND):
    def __init__(self,name,size,dim=1,dt=0.1,wrap=True,
                 tau=1.0,h=0,
                 wExc=0.5,wInh=2.0,iExc=0.6,iInh=1.0,
                 th=0.75,delta=1.,activation='step',
                 nbStep=0,noiseI=0.0,
                 **kwargs):
        super().__init__(name,size,dim=dim,dt=dt,wrap=wrap,
                    tau=tau,h=h,delta=delta,
                    wExc=wExc,wInh=wInh,iExc=iExc,iInh=iInh,
                    th=th,activation=activation,
                    noiseI=noiseI,
                    **kwargs)

        self.act = ActivationMapND("Activation",size,dim=dim,dt=dt,type=activation,th=th)
        self.lat = LateralWeightsDiff(name+"Kernel",size,dim=dim,dt=dt,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh)
        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(act=self.act)

    def getActivation(self):
        return self.act

    def getArrays(self):
        return [
            self.act,
            self.lat,
        ]


if __name__ == "__main__":
        size = 101
        dim = 2
        shape = (size,)*dim
        dt = 0.1
        time = 0
        dnf = MapDNFND("uut",size,dim=dim);
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
            print("DNF" , dnf.getData())
            print("ACT" , dnf.act.getData())

        plt.subplot(221)
        plt.plot(dnf.getData())
        plt.title("DNF")
        plt.subplot(222)
        plt.plot(dnf.act.getData())
        plt.title("ACT")
        plt.subplot(223)
        plt.plot(dnf.lat.getData())
        plt.title("LAT")
        plt.subplot(224)
        plt.plot(dnf.kernel.getData())
        plt.title("KER")
        plt.show()


