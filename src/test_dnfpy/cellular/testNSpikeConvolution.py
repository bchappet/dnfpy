import unittest
import matplotlib.pyplot as plt
import numpy as np
from dnfpy.cellular.nSpikeConvolution import NSpikeConvolution
from dnfpy.core.constantMap import ConstantMap


class TestNSpikeConvolutionMap(unittest.TestCase):
    def setUp(self):
        self.size = 49
        self.activation = np.zeros((self.size,self.size),np.intc)
        activationMap = ConstantMap("actmap",self.size, self.activation)
        self.uut = NSpikeConvolution("uut",self.size,reproductible=True)
        self.uut.addChildren(activation=activationMap)

    def test_update(self):
        self.uut.compute()
        data = self.uut.getData()
        self.assertEqual(np.sum(data),0)



    def test_update_act(self):
        data = self.getData()
        print("min : %s, max: %s, sum: %s"%(np.min(data),np.max(data),np.sum(data)))
        self.assertEqual(np.sum(data), -414.94460641399417  )
        #view.plotArray(data)
        #view.show()

    def getData(self):
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                self.activation[self.size/2+i][self.size/2+j] = 1;
        self.uut.compute()
        data = self.uut.getData()
        return data

    def test_diag_std(self):
        self.uut.setParamsRec(nspike=1)
        diags = []
        for i in range(10):
            print("Repetition %s"%i)
            data = self.getData()
            diag = self.getDiag(data)
            diags.append(diag)

        mean,std = self.computeStatsDiag(diags)
        print mean
        print std
#        self.assertAlmostEqual(mean[0],-0.16524448)#50


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
