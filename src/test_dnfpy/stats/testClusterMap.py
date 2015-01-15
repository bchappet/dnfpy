import unittest
import  dbscanOnFocus as uut
import numpy as np
from clusterMap import ClusterMap

class TestDBScanFocus(unittest.TestCase):
    def setUp(self):
        self.size = 20
        self.sample = np.zeros((self.size,self.size))
        self.uut = ClusterMap("uut",0,dt=0.1,np_arr=self.sample,
                              clustSize=0.3,
                              sizeNpArr=self.size)

    def testDBSCAN_empty(self):
        self.uut.compute()
        self.assertEqual(self.uut.getArg("nbComputationEmpty"),1)
        self.uut.compute()
        self.assertEqual(self.uut.getArg("nbComputationEmpty"),2)

    def testDBSCAN(self):
        self.sample[0,0] = 1
        self.sample[0,3] = 1
        self.sample[10,0] = 1
        self.sample[10,3] = 1
        self.uut.compute()
        self.assertEqual(self.uut.getArg("nbOutliners"),0)
        data = self.uut.getData()
        self.assertTrue(data.shape == (2,2))
        self.assertTrue((data==[0,1.5]).any())
        self.assertTrue((data==[10,1.5]).any())

    def testdbScanOutliners(self):
        self.sample[0,0] = 1
        self.sample[0,3] = 1
        self.sample[5,5] = 1
        self.sample[10,0] = 1
        self.sample[10,3] = 1
        self.uut.setParams(min_samples=2)
        self.uut.compute()
        self.assertEqual(self.uut.getArg("nbOutliners"),1)
        data = self.uut.getData()
        self.assertTrue(data.shape == (2,2))
        self.assertTrue((data==[0,1.5]).any())
        self.assertTrue((data==[10,1.5]).any())

    def testDBSCANContinuous(self):
        self.sample[0,0] = 1
        self.sample[0,3] = 1
        self.sample[10,0] = 1
        self.sample[10,3] = 1
        self.uut.setParams(continuity=1.)
        self.uut.compute()
        self.assertEquals(self.uut.getArg("nbNewCluster"),2)
        self.assertEquals(self.uut.getArg("nbDiscontinuousCluster"),0)
        data = self.uut.getData()

        clust0 = data[0]
        clust1 = data[1]

        self.sample[0,1] = 1
        self.sample[0,2] = 1
        self.sample[10,1] = 1
        self.sample[10,2] = 1
        self.uut.compute()
        self.assertEquals(self.uut.getArg("nbNewCluster"),0)
        self.assertEquals(self.uut.getArg("nbDiscontinuousCluster"),0)
        data = self.uut.getData()
        self.assertTrue((clust0 - data[0] < 3).all())
        self.assertFalse((abs(clust1 - data[0]) < 3).all())
        self.assertTrue((clust1 - data[1] < 3).all())
        self.assertFalse((abs(clust0 - data[1]) < 3).all())



if __name__ == "__main__":
    unittest.main()


