import numpy as np
from dnfpyUtils.stats.stats import Stats
import time
from dnfpyUtils.stats.sumStat import SumStat
 

class StatsNbAct(Stats):
    """
Will compute stats about the activation map

    """
    def initMaps(self,size,dim,dt=0.1,mapUnderStats="",**kwargs):
        activationMap = self.runner.getMap("Activation"+mapUnderStats)
        self.sumStat = SumStat('sum',dt=dt)
        self.sumStat.addChildren(map=activationMap)
        return [self.sumStat]


    def getArrays(self):
        """
        Return a list of stat map to display
        """
        return [self.sumStat]

    def fitness(self,result):
        assert(False)#not implemented

    def finalize(self):
        """
        Do something when simulation ends
        and return information
        """

        mean = self.sumStat.getMean()
        max = self.sumStat.getMax()
        min = self.sumStat.getMin()
        std = self.sumStat.getStd()
        p5 = self.sumStat.getPercentile(5)
        p95 = self.sumStat.getPercentile(95)

       
        return (mean,min,max,std,p5,p95)

    @staticmethod
    def getColumns():
        return ['mean','min','max','std','p5','p95']




