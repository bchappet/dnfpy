import numpy as np
import matplotlib.pyplot as plt

class StochBitStream:
    def __init__(self,size,valMax=1):
        self.size = size
        self.valMin = 0.
        self.valMax = valMax

    def genStream(self,proba):
        return np.where(np.random.uniform(size=(self.size))<=proba,1,0)


    def andOp(self,bs_a,bs_b):
        """
        return va * vb / valMax
        """
        return bs_a*bs_b

    def orOp(self,bs_a,bs_b):
        return bs_a|bs_b

    def multiplexerOp(self,bs_a,bs_b):
        select = self.genStream(0.5)
        return select*bs_a + (1-select)*bs_b


    def decode(self,bs):
        return np.mean(bs)*(self.valMax-self.valMin)-self.valMin

    def encode(self,val):
        proba = (float(val)+self.valMin)/(self.valMax-self.valMin)
        return self.genStream(proba)

    def getPrecisionStep(self):
        return (1./self.size) *(self.valMax-self.valMin)-self.valMin


    def plotMultQuality(self):
        X = np.arange(0,self.valMax,self.getPrecisionStep())
        Y = []
        for i in X:
            a =  self.encode(i)
            b = self.encode(i)
            res = self.multiplexerOp(a,b)
            Y.append(self.decode(res))
        plt.plot(X,Y)
        plt.plot(X,2*X/2)
        plt.title("Mult quality")
        plt.show()

    def plotOrQuality(self):
        X = np.arange(0,self.valMax,self.getPrecisionStep())
        Y = []
        for i in X:
            a =  self.encode(i)
            b = self.encode(i)
            res = self.orOp(a,b)
            Y.append(self.decode(res))
        plt.plot(X,Y)
        plt.plot(X,2*X)
        plt.title("Or quality")
        plt.show()

    def plotAndQuality(self):
        X = np.arange(0,self.valMax,self.getPrecisionStep())
        Y = []
        for i in X:
            a =  self.encode(i)
            b = self.encode(i)
            res = self.andOp(a,b)
            Y.append(self.decode(res))
        plt.plot(X,Y)
        plt.plot(X,X*X/self.valMax)
        plt.title("And quality")
        plt.show()



if __name__ == "__main__":
    sbs = StochBitStream(1000,valMax=1)
    print("precision step : %s"%sbs.getPrecisionStep())
    a = sbs.encode(3)
    b = sbs.encode(5)
    res= sbs.multiplexerOp(a,b)
    print sbs.decode(res)
    sbs.plotQuality()


