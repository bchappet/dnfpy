import numpy as np
import dnfpy.view.staticViewMatplotlib as view
from dnfpy.core.map2D import Map2D
import time

import socket
import struct
from threading import Thread
from queue import Queue


def matrix_active(size,x, y, pol):
    matrix = np.zeros([size, size])
    if(len(x) == len(y)):
        for i in range(len(x)):
            matrix[-y[i], -x[i]] = abs(pol[i])  # matrix[x[i],y[i]] + pol[i]
    else:
        print("error x,y missmatch")
    return matrix



class DvsMap(Map2D):
    """
    Connect to given host port and read the events
    the computations are done on a diffirent thread
    """
    def __init__(self,name,size,dt=0.1,dtype=np.int8,**kwargs):
        super().__init__(name,size,dt=dt,**kwargs)
        host = "127.0.0.1"
        port = 8888
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))


    def _compute(self,size):
        x, y, p = self.read_events()
        this_m = matrix_active(size+1,x, y, p)
        self._data =  this_m[:-1,:-1]




    def close(self):
        pass
        


    def read_events(self):
        """ A simple function that read events from cAER tcp"""

        data = self.sock.recvfrom(64 * 1024)[0]  # we read the full packet, which is one UDP message. Use a big size to ensure we get it all.

        # read header
        eventtype = struct.unpack('H', data[0:2])[0]
        if(eventtype == 1):  # something is wrong as we set in the cAER to send only polarity events
            eventsource = struct.unpack('H', data[2:4])[0]
            eventsize = struct.unpack('I', data[4:8])[0]
            eventoffset = struct.unpack('I', data[8:12])[0]
            eventtsoverflow = struct.unpack('I', data[12:16])[0]
            eventcapacity = struct.unpack('I', data[16:20])[0]
            eventnumber = struct.unpack('I', data[20:24])[0]
            eventvalid = struct.unpack('I', data[24:28])[0]
            counter = 28  # eventnumber[0]
            x_addr_tot = []
            y_addr_tot = []
            pol_tot = []
            while(data[counter:counter + eventsize]):  # loop over all event packets
                aer_data = struct.unpack('I', data[counter:counter + 4])[0]
                timestamp = struct.unpack('I', data[counter + 4:counter + 8])[0]
                x_addr = (aer_data >> 17) & 0x00007FFF
                y_addr = (aer_data >> 2) & 0x00007FFF
                x_addr_tot.append(x_addr)
                y_addr_tot.append(y_addr)
                pol = (aer_data >> 1) & 0x00000001
                pol_tot.append(pol)
                #print (timestamp, x_addr, y_addr, pol)
                counter = counter + eventsize

        return x_addr_tot, y_addr_tot, pol_tot
