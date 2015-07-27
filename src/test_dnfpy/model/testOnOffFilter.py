from dnfpy.model.onOffFilter import OnOffFilter
import unittest
import dnfpy.view.staticViewMatplotlib as view
import matplotlib.pyplot as plt
import numpy as np

class TestOnOffFilter(unittest.TestCase):

        def test_1(self):
            uut = OnOffFilter("uut",100,onIntXY=(1,1),onStdXY=np.array([0.1,0.5]),
                              offIntXY = (1,1), offStdXY = np.array([0.1,0.5]),
                              shift = 0.2)

            uut.compute()
            view.plotArray(uut.getData())
            plt.show()


if __name__ == '__main__':
    unittest.main()





