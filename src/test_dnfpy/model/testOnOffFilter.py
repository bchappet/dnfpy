from dnfpy.model.onOffFilter import OnOffFilter
import unittest
import dnfpy.view.staticViewMatplotlib as view
import matplotlib.pyplot as plt

class TestOnOffFilter(unittest.TestCase):

        def test_1(self):
            uut = OnOffFilter(100,onIntXY=(1,1),onStdXY=(10,50),offIntXY = (1,1), offStdXY = (10,50),shift = 20)
            uut.artificialRecursiveComputation()
            view.plotArray(uut.getData())
            plt.show()

        def test_params(self):
            uut = OnOffFilter(30)
            uut.registerOnGlobalParamsChange(onIntXY = 'onIntXY',
                    onStdXY = 'onStdXY', offIntXY = 'offIntXY',
                    offStdXY = 'offStdXY',shift = 'shift')
            params = dict(onIntXY = (1,1), onStdXY = (0.1,0.5),
                    offIntXY = (1,1), offStdXY = (0.1,0.5), 
                    shift = 0.2)
            uut.updateParams(params)
            uut.artificialRecursiveComputation()
            view.plotArray(uut.getData())
            plt.show()

if __name__ == '__main__':
    unittest.main()





