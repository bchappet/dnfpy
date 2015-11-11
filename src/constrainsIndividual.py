import sys
import numpy as np
from scipy.special import erf

from getClassUtils import getClassFromName
import dnfpy.controller.runnerView as runnerView
import dnfpy.controller.runner as runner

import begin #very usefull arg parsing library


import dnfpy.core.utilsND as utils


def constraints(indiv):
            """
            indiv dictinary
            We are applying constrains to the individual given to the model
            return 0 if constraints are satisfied
            """
            alpha = 10

            kE = indiv['iExc']
            kI = indiv['iInh']
            wE = indiv['wExc']
            wI = indiv['wInh']
            th = indiv['th']
            h = indiv['h']
            size = indiv["size"]
            dim = indiv['dim']

            if(h >= th) or (kE <= kI):
                constraints =  100000

            kE2 = kE*size**dim/100 *40**dim/alpha
            kI2 = kI*size**dim/100 *40**dim/alpha
            a = np.linspace(0,size,1000)

            assert(wE > 0)
            assert(wI > 0)
            solution =  utils.dogSolution(a,kE2,kI2,wE,wI)
            zeroCross  = np.where(np.diff(np.sign(solution-th+h)))[0]#solution - th == 0?
            derivative = np.gradient(solution)

            aStable = np.nan
            if np.any(derivative[zeroCross] < 0):
                    #stable point
                    constraint = 0
                    aStable =  a[zeroCross[derivative[zeroCross] < 0]]
            else:
                    if(len(zeroCross) == 0):
                        #no fixed point, return the minimal distance from 0 
                        constraint =  np.min(np.abs(solution -th + h))
                    else:
                        #fixed point but unstable, return the slope of the derivative?
                        constraint = np.sum(derivative[zeroCross])

            return constraint,aStable


   
@begin.start
def main(indiv="{}"):
    individual = eval(indiv)
    print(constraints(individual))

