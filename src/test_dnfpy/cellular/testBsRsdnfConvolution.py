import unittest
import time
import numpy as np
import matplotlib.pyplot as plt
from dnfpy.cellular.bsRsdnfConvolution import BsRsdnfConvolution
from dnfpy.core.constantMap import ConstantMap
import dnfpy.view.staticViewMatplotlib as view


class TestBsRsdnfConvolutionMap(unittest.TestCase):
    def setUp(self):
        self.size = 49
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut = BsRsdnfConvolution("uut",self.size)
        self.uut.addChildren(activation=activationMap)

    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        self.assertEqual(np.sum(data),0)


    def test_update_act(self):
        self.uut.setParamsRec(pSpike=0.1)
        #self.uut.setParamsRec(precisionProba=8)
        sizeStream = 200
        repet = sizeStream+2*self.size-1
        self.uut.setParamsRec(sizeStream=sizeStream)
        #self.uut.setParamsRec(nstep=repet)
        data = self.getData(repet)
        sumD = np.sum(data)
        print("min : %s, max: %s, sum: %s"%(np.min(data),np.max(data),sumD))
        view.plotArray(data)
        view.show()
        self.assertAlmostEqual(sumD,-267.47505206164101)


    def test_diag_std(self):
        self.uut.setParamsRec(pSpike=0.1)
        self.uut.setParamsRec(precisionProba=30)
        self.uut.setParamsRec(iExc=1.51,iInh=0.92),#pExc=0.00045,pInh=0.44)
        sizeStream = 200
        self.uut.setParamsRec(sizeStream=sizeStream)
        diags = []
        repet = sizeStream+2*self.size-1
        #self.uut.setParamsRec(nstep=repet)
        for i in range(2):
            print("Repetition %s"%i)
            self.uut.resetData()
            data = self.getData(repet)
            diag = self.getDiag(data)
            diags.append(diag)

        (mean,std) = self.computeStatsDiag(diags)
        print(mean)
        print(std)

    def getData(self,repet):
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                self.activation[self.size//2+i][self.size//2+j] = 1;
        start = time.clock()
        for i in range(repet):
            self.uut.compute()
        end = time.clock()
        print("elapsed time %s"%(end-start))
        data = self.uut.getData()
        return data

    def getDiag(self,data):
        diag = []
        for i in range(data.shape[0]):
            diag.append(data[i,i])
        return np.array(diag)


    def computeStatsDiag(self,diags):
        mean = np.mean(diags,axis=0)
        std = np.std(diags,axis=0)
        x = range(0,len(mean))
        plt.plot(x,mean)
        plt.errorbar(x,mean,yerr=std)
        plt.show()
        return (mean,std)

if __name__ == "__main__":
    unittest.main()
