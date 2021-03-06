from dnfpy.model.activationMapND import ActivationMap
import numpy as np
from dnfpy.model.fieldMapND import FieldMap
from dnfpy.model.convolutionND import ConvolutionND
from dnfpy.core.constantMapND import ConstantMap
from dnfpy.model.kernelConvolution import KernelConvolution
from dnfpy.model.sfaMap import SFAMap

class MapDNFND(FieldMap):
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
                 sfa=False,tauSFA=1.0,mSFA=4.8,beta=0.2,
                 errorProb=0.0,errorType='none',
                 **kwargs):
        super().__init__("Potential"+name,size,dim=dim,dt=dt,wrap=wrap,
                    tau=tau,h=h,delta=delta,
                    model=model,th=th,activation=activation,
                    noiseI=noiseI,lateral=lateral,
                    beta=beta,
                    **kwargs)

        self.act = ActivationMap("Activation"+name,size,dim=dim,dt=dt,type=activation,th=th,
            errorProb=errorProb,errorType=errorType)
        self.lat = KernelConvolution("Lateral"+name,size,dim=dim,dt=dt,wrap=wrap,nbStep=nbStep,
                iExc=iExc,iInh=iInh,wExc=wExc,wInh=wInh,alpha=alpha,fashion=fashion,lateral=lateral)

        if sfa:
            self.sfa = SFAMap("SFA"+name,size,dim=dim,tau=tauSFA,dt=dt,m=mSFA)
            self.sfa.addChildren(pot=self)
            self.addChildren(sfa=self.sfa)
        else:
            self.sfa = None


        self.act.addChildren(field=self)
        self.addChildren(lat=self.lat)
        self.lat.addChildren(source=self.act)

    def getActivation(self):
        return self.act

    def getArrays(self):
        li= [
            self.act,
            self.lat,
        ]
        if self.sfa:
            li.append(self.sfa)
        return li


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


