import numpy as np
from dnfpy.core.map2D import Map2D
import struct

def addressToCoordAEDAT1(address,res):
    pol = address & 0x0001
    YAddr = address >> 8 & 0x007f
    XAddr = address >> 1 & 0x007f
    return YAddr,XAddr,pol

def addressToCoordAEDAT2(address,res):
    XAddr = (address >> 17) & 0x00007FFF
    YAddr = (address >> 2) & 0x00007FFF
    pol = (address >> 1) & 0x00000001

    return YAddr,XAddr,pol


def unpackAEDAT1(f):
    byte = f.read(6)
    return struct.unpack(">hi",byte)

def unpackAEDAT2(f):
    byte = f.read(8)
    return struct.unpack("II",byte)

class AEDatReader(Map2D):
    def __init__(self,name,size,fileName,dt=0.1,tick=1):
        super().__init__(name=name,size=size,fileName=fileName,dt=dt,tick=tick,timeStep=dt/(tick*1e-6))
        self.f = open(fileName,"rb")
        self.lastTimeStamp = None
        self.dataTmp = np.zeros((128,128))

        self.format = self.detectFormat(self.f)
        print(self.format)
        if self.format == "AER-DAT1.0":
            self.addressToCoord = addressToCoordAEDAT1
            self.unpack = unpackAEDAT1
        elif self.format == "AER-DAT2.0":
            self.addressToCoord = addressToCoordAEDAT2
            self.unpack = unpackAEDAT2
        else:
            print("unknown format " + str(self.format))


    def detectFormat(self,f):
        line = f.readline()
        print(line[0:2])
        if line[0:2] == b'#!':
            format = line[2:-2].decode()
            while line[0] == "#":
                line=f.readline()
        else:
            format = "AER-DAT1.0"
        return format


    def _compute(self,timeStep,size):
        self.dataTmp[...] = 0

        address,timeStamp = self.unpack(self.f)
        YAddr,XAddr,pol = self.addressToCoord(address,128)
        if not(self.lastTimeStamp): 
            self.lastTimeStamp = timeStamp
        self.lastTimeStamp = self.lastTimeStamp + timeStep
        while timeStamp < self.lastTimeStamp :
            address,timeStamp = self.unpack(self.f)
            YAddr,XAddr,pol = self.addressToCoord(address,128)
            self.dataTmp[-YAddr,-XAddr] += 1

        self._data[...] = self.dataTmp[:size,:size]


    def reset(self):
        super().reset()
        fileName = self._init_kwargs['fileName']
        self.f = open(fileName,"rb")
        self.lastTimeStamp = None







