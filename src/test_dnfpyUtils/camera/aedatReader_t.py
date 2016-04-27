import unittest
import os
from dnfpyUtils.camera.aedatReader import AEDatReader


class AEDatReader_t(unittest.TestCase):
    def setUp(self):
        dirName = os.path.dirname(os.path.realpath(__file__))
        self.uut = AEDatReader('uut',dirName+'/Tmpdiff128-2006-02-14T07-45-15-0800-0 walk to kripa.dat')

    def testTimeStep(self):
        self.assertAlmostEqual(self.uut.getArg('timeStep'),1e5)





if __name__ == "__main__":
    unittest.main()
