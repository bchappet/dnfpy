import numpy as np
from dnfpy.core.map2D import Map2D
import struct

def addressToCoordAEDAT1(address,res):
    pol = address & 0x0001
    YAddr = address >> 8 & 0x007f
    XAddr = address >> 1 & 0x007f
    return YAddr,XAddr,pol

def addressToCoordAEDAT2(address,res):
    #XAddr = (address >> 17) & 0x00007FFF
    #YAddr = (address >> 2) & 0x00007FFF
    #pol = (address >> 1) & 0x00000001
    xmask = 0x00fe
    xshift = 1
    ymask = 0x7f00
    yshift = 8
    pmask = 0x1
    pshift = 0

    XAddr = (address & xmask) >> xshift
    YAddr = (address & ymask) >> yshift
    pol = (address & pmask) >> pshift

    return YAddr,XAddr,pol


def unpackAEDAT1(f,p):
    f.seek(p)
    byte = f.read(6)
    p+=6
    address,timeStamp = struct.unpack(">HI",byte)
    return address,timeStamp,p

def unpackAEDAT2(f,p):
    f.seek(p)
    byte = f.read(8)
    p+=8

    address,timeStamp = struct.unpack(">II",byte)
    #print(timeStamp)
    return address,timeStamp,p

class AEDatReader(Map2D):
    def __init__(self,name,size,fileName,dt=0.1,tick=10):
        """
        tick in us
        timeStep in us
        """
        super().__init__(name=name,size=size,fileName=fileName,dt=dt,tick=tick,timeStep=dt/(tick*1e-6))

    def detectFormat(self,f):
        p = 0 # pointer for byte
        line = f.readline()
        p += len(line)
        print(line[0:2])
        if line[0:2] == b'#!':
            format = line[2:-2].decode()
            line=f.readline()
            p += len(line)
            while line and line[0:1] == b'#':
                line=f.readline()
                p += len(line)
        else:
            format = "AER-DAT1.0"
        return format,p


    def _compute(self,timeStep,size):
        self.dataTmp[...] = 0

        
        address,timeStamp,self.p = self.unpack(self.f,self.p)
        YAddr,XAddr,pol = self.addressToCoord(address,128)
        if not(self.lastTimeStamp): 
            self.lastTimeStamp = timeStamp
        self.lastTimeStamp = self.lastTimeStamp + timeStep
        #print(self.lastTimeStamp/1e6)
        while timeStamp < self.lastTimeStamp :
            address,timeStamp,self.p = self.unpack(self.f,self.p)
            YAddr,XAddr,pol = self.addressToCoord(address,128)
            self.dataTmp[-YAddr,-XAddr] += 1

        self._data[...] = self.dataTmp[:size,:size]


    def reset(self):
        super().reset()
        fileName = self._init_kwargs['fileName']
        self.f = open(fileName,"rb")
        self.lastTimeStamp = None
        self.dataTmp = np.zeros((128,128))

        self.format,self.p = self.detectFormat(self.f)
        print(self.format)
        if self.format == "AER-DAT1.0":
            self.addressToCoord = addressToCoordAEDAT1
            self.unpack = unpackAEDAT1
        elif self.format == "AER-DAT2.0":
            self.addressToCoord = addressToCoordAEDAT2
            self.unpack = unpackAEDAT2
        else:
            print("unknown format " + str(self.format))


