#
#graphical library:
#






import subprocess
import sys
import re
import matplotlib.pyplot as plt
import csv
import numpy
import math
from matplotlib.ticker import FuncFormatter
import matplotlib.gridspec as gridspec





def finalize():
	plt.xticks([])
	plt.yticks([])
	plt.show()
	#plt.savefig(fileName+'.eps',dpi=100,format='eps')
	#plt.savefig(fileName+'.png')

def csvToArray(fileName):#return array
		data = csv.reader(open(fileName),delimiter=',')
		data = list(data)
		data = numpy.array(data).astype('float')
		return data
def egaliseColorBar(data,bar):
		maximum = numpy.amax(data)
		minimum = numpy.amin(data)
		egal = max(abs(maximum),abs(minimum))
		plt.clim(-egal,+egal)
		bar.set_ticks([roundUp(-egal),0,roundDown(+egal)])
		
def roundDown(x):
	return math.floor(x*100)/100
def roundUp(x):
	return math.ceil(x*100)/100

#Plot a np.array, with egalised colorbar
def plotArray(data):
	ret = plt.imshow(data,interpolation='nearest',cmap='RdYlBu_r',origin='lower')
	bar = plt.colorbar(shrink=.92)
	egaliseColorBar(data,bar)
	return ret
				

def saveFig(plt,fileName):
	dpi = 300
	print "Saving..." + fileName+".[eps|png]"
	plt.savefig(fileName+'.eps',dpi=dpi,format='eps')
	plt.savefig(fileName+'.png',dpi=dpi)
	
	
def plotCurve(x,label,save,fileName):
	plt.plot(x,label=label)
	if(save):
		saveFig(plt,fileName)
	else:
		plt.show()



def plotMaps(maps):
	"""Expect a dictionary name: map"""
	i = 0
        size = len(maps)
        width = int(math.ceil(math.sqrt(size)))
        height = int(math.ceil(size/float(width)))
	f, axarr = plt.subplots(height,width)
        gs = gridspec.GridSpec(height, width)
	for name in maps:
                if( i == len(maps)-1): #last fig
                        ax = plt.subplot(gs[i/width,i%width :])		
                else:
        	        ax = plt.subplot(gs[i/width,i%width])		
		array = maps[name]
		plotArray(array)
		ax.set_title(name)
		plt.xticks([])
		plt.yticks([])
		i+=1

	
	
		
	

