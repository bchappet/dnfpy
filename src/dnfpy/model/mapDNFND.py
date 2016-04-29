from dnfpy.model.activationMapND import ActivationMapND
import numpy as np
from dnfpy.model.fieldMapND import FieldMapND
from dnfpy.model.lateralWeightsMapND import LateralWeightsMapND
from dnfpy.model.lateralWeightsMapExpND import LateralWeightsMapExpND
from dnfpy.model.lateralWeightsMapLinND import LateralWeightsMapLinND
from dnfpy.model.lateralWeightsMapStep import LateralWeightsMapStep
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.core.constantMapND import ConstantMapND
#import matplotlib.pyplot as plt

class MapDNFND(FieldMapND):
    """
    lateral: 'dog','doe','dol' difference of gaussian, difference of exponential or diferrence of linear function
    fashion : 'chappet,'fix' fix fashion is designed to have similar parameters for the kernels
    """
    def __init__(self,name,size,dim=1,dt=0.1,wrap=True,
                 tau=0.64,h=0,
                 model='cnft',th=0.75,delta=1.,activation='step',
                 iExc=1.25,iInh=0.7,wExc=0.1,wInh=1.0,alpha=10,
                 mapSize=1.,nbStep=0,noiseI=0.0,lateral='dog',
                 fashion='chappet',
                 **kwargs):
        super(MapDNFND,self).__init__("Potential"+name,size,dim=dim,dt=dt,wrap=wrap,
                    tau=tau,h=h,delta=delta,
                    model=model,th=th,activation=activation,
                    noiseI=noiseI,lateral=lateral,
                    **kwargs)

        self.act = ActivationMapND("Activation"+name,size,dim=dim,dt=dt,type=activation,th=th)
        self.lat =ConvolutionND("Lateral"+name,size,dim=dim,dt=dt,wrap=wrap)
        #self.kernel = LateralWeightsMapND(name+"Kernel",mapSize=mapSize,
        #                               globalSize=size,dim=dim,wrap=wrap,
        #                              iExc=iExc,iInh=iInh,wExc=wExc,
        #                             wInh=wInh,alpha=alpha,nbStep=nbStep)


        globalSize = size if wrap else int(np.round(2.0*size))
        if lateral=='dog':
            self.kernel = LateralWeightsMapND("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,
                                        iExc=iExc,iInh=iInh,wExc=wExc,
                                        wInh=wInh,alpha=alpha,nbStep=nbStep,fashion=fashion)
        elif lateral=='doe':
            self.kernel = LateralWeightsMapExpND("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,
                                        iExc=iExc,iInh=iInh,pExc=wExc,
                                        pInh=wInh,alpha=alpha,nbStep=nbStep,fashion=fashion)
        elif lateral=='dol':
            self.kernel = LateralWeightsMapLinND("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,
                                        betaExc=iExc,betaInh=iInh,alphaExc=wExc,
                                        alphaInh=wInh,alpha=alpha,nbStep=nbStep,fashion=fashion)
        elif lateral=='step':
            self.kernel = LateralWeightsMapStep("Kernel"+name,mapSize=mapSize,dim=dim,
                                        globalSize=globalSize,wrap=wrap,iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh)
        else:
            raise("Parameter lateral should be 'dog', 'doe' or 'dol'. %s invalid"%(lateral))
 
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


