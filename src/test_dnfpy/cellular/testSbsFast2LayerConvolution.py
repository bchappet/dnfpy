import unittest
import time
import numpy as np
import matplotlib.pyplot as plt
from dnfpy.cellular.sbsFast2LayerConvolution import SbsFast2LayerConvolution
from dnfpy.core.constantMap import ConstantMap
import dnfpy.view.staticViewMatplotlib as view


class TestSbsFast2LayerConvolution(unittest.TestCase):
    def setUp(self):
        self.size = 49
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut = SbsFast2LayerConvolution("uut",self.size)
        self.uut.addChildren(activation=activationMap)

    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        print(data)
        self.assertEqual(np.sum(data),0)


    def test_update_act(self):
        self.uut.setParams(pSpike=0.1)
        sizeStream = 200
        self.uut.setParams(sizeStream=sizeStream)
        data = self.getData()
        sumD = np.sum(data)
        print("min : %s, max: %s, sum: %s"%(np.min(data),np.max(data),sumD))
        view.plotArray(data)
        view.show()
        self.assertAlmostEqual(sumD,-297.74427321949184)


    def test_diag_std(self):
        self.uut.setParams(pSpike=0.1)
        self.uut.setParams(precisionProba=30)
        self.uut.setParams(iExc=1.51,iInh=0.92),#pExc=0.00045,pInh=0.44)
        sizeStream = 200
        self.uut.setParamsRec(sizeStream=sizeStream)
        diags = []
        #self.uut.setParamsRec(nstep=repet)
        for i in range(2):
            print("Repetition %s"%i)
            self.uut.resetData()
            data = self.getData()
            diag = self.getDiag(data)
            diags.append(diag)

        (mean,std) = self.computeStatsDiag(diags)
        print mean
        print std

    def getData(self):
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                self.activation[self.size/2+i][self.size/2+j] = 1;
        start = time.clock()
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
