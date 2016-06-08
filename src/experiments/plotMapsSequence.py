import sys
import dnfpy.view.staticViewMatplotlib as view
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os,glob
import re
import numpy as np
from dnfpy.core.utils import cosTraj

color = 'black'

showBar = True
showArrows = False
showCross = True
#if show arrow
radius = 0.3
center = 0.
period = 36
dt = 0.1


path = sys.argv[1] #name of the save folder
mapNames = eval(sys.argv[2]) #list of names "['a','b',...]"
#timeList = eval(sys.argv[3]) #list of time "[1,2]"
timeList = []
if len(sys.argv) > 3:
    traceNames = eval(sys.argv[3]) #list of the traces "['ta','tb',...]" if no trace, only the time will be displayed
else:
    traceNames = []

def getArray(name,time):
    tStr = str(time)
    timeStr = "_".join(tStr.split("."))
    return np.loadtxt(path + name + "_" + timeStr + ".csv",delimiter=",")

def getTrackCenter(index,time,sizeArray):
    phase = index/2.
    radius_ = radius * sizeArray
    center_ = center * sizeArray + (sizeArray-1)/2

    print(cosTraj(26.4,50,36,30.3,0))
    print(cosTraj(26.4,50,36,30.3,0.25))

    x = cosTraj(time,center_,period,radius_,phase)
    y = cosTraj(time,center_,period,radius_,phase+0.25)
    
    return x,y




for filename in glob.glob(os.path.join(path, '*.csv')):
    split1 = filename.split('_')
    if len(split1) == 3:
        mapOfFile = (split1[-3]).split('/')[-1]
        if mapNames[0] == mapOfFile:
            time = eval(".".join(re.compile("[_\.]").split(filename)[-3:-1]))
            timeList.append(time)
timeList.sort()

print(mapNames,timeList)

#get size array
sizeArray = getArray(mapNames[0],timeList[0]).shape[0]


#We prepare the grid
grid = gridspec.GridSpec(len(mapNames)+len(traceNames), len(timeList))
#we need to adjust the size of the grid to be sure that every map fit
size = 2
#fig = plt.figure(figsize=(size*len(timeList),size*(len(mapNames)+len(traceNames))))
fig = plt.figure(figsize = (9,size*(len(mapNames)+len(traceNames))))
main_ax = plt.gca()



for i in range(len(mapNames)):
    for j in range(len(timeList)):
        axes = plt.subplot(grid[i,j])
            
        if j == 0: #plot name
            plt.text(-0.15,0.5,mapNames[i],transform=axes.transAxes,va='center',ha='left',zorder=100,fontsize=12,rotation=90)


        if mapNames[i] == "Inputs":
            time = timeList[j]
            for indexStim in [0,1]:
                #(x,y) = getTrackCenter(indexStim,time,sizeArray)

                x = getArray("Inputs_track"+str(indexStim)+"_c0",time)
                y = getArray("Inputs_track"+str(indexStim)+"_c1",time)
                (xt,yt) = getTrackCenter(indexStim,time+5,sizeArray)
                #[xFig,yFig] = axis.transData.transform([x,y])
                if j==0 and showArrows:
                        axes.annotate("",
                        xy=(xt, yt), xycoords='data',
                        xytext=(x, y), textcoords='data',
                        arrowprops=dict(arrowstyle="->",
                                        connectionstyle="arc3,rad=-0.3",
                                        ),
                        )
                if showCross:
                        marker = axes.scatter([x], [y], marker='+',color=color)
             
        plt.xticks([]), plt.yticks([])
        array = getArray(mapNames[i],timeList[j])
        img = view.plotArray(array,showBar=False,egal=1)
        if i == len(mapNames) -1:
            plt.text(0.5,-0.1,timeList[j],va='center',ha='center',transform=axes.transAxes)

    if showBar:
        #plot colorbar
        axisbg='w'
        rect = [0.,0.,1,1]
        box = axes.get_position()
        width = box.width
        height = box.height
        inax_position  = axes.transAxes.transform(rect[0:2])
        transFigure = fig.transFigure.inverted()
        infig_position = transFigure.transform(inax_position)    
        x = infig_position[0]+0.03
        y = infig_position[1]
        width *= rect[2]
        height *= rect[3]
        print(x,y,width,height)
               
        
        subax = fig.add_axes([x,y,width,height],axisbg=axisbg)

        egal  = 1
        a = np.array([[-egal,egal]])
        img = view.plotArray(a,showBar=False,egal=egal)
        bar = plt.colorbar(shrink=.9)
        plt.gca().set_visible(False)
        #axes.set_visible(False)
        view.egaliseColorBar(egal,bar)



if len(traceNames) > 0:


    lwTrace= 2
    lineColor = 'black'
    lineWidth = 2

    traceName = traceNames[0]
    trace =  np.load(path + traceName + ".csv.npy")

    x = np.linspace(0,timeList[-1],len(trace))
    axis = plt.subplot(grid[-1,:])

    maxLenTrace = np.max([len(t) for t in trace])
    balancedTrace = np.ones((len(trace),maxLenTrace))*np.nan
    for i in range(len(trace)):
        for j in range(len(trace[i])):
            balancedTrace[i,j] = trace[i][j]

    for i in range(maxLenTrace):
        plt.plot(x,balancedTrace[:,i],lw=1,color=color)
    # Hide the right and top spines
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axis.yaxis.set_ticks_position('left')
    axis.xaxis.set_ticks_position('bottom')
    
    plt.xlabel("Time (s)")
    plt.ylabel("Error distance",multialignment='center')

    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=10)
    formatter=ticker.FormatStrFormatter("%1.2f")
    ax.yaxis.set_major_formatter(formatter)
    plt.xlim(0,timeList[-1])

    plt.ylim(0,0.1)
    ylim = ax.get_ylim()
    plt.ylim(ylim)

    #Add lines on trace
    for it in zip(timeList):
            plt.plot([it,it],ylim,color=lineColor,lw=lineWidth)


    newax = fig.add_axes(main_ax.get_position(), frameon=False)
    #plt.subplot2grid(grid,(gridY-2,0),colspan=gridX,rowspan=2)
    size =100
    plt.xlim([0,size])
    plt.ylim([0,size])
    rowSize = size/float(len(mapNames)+1)
    yto = 0 + rowSize + rowSize/10.0 -rowSize/15.0 -3
    yfrom =0 +  rowSize - rowSize/10.0 -rowSize/50.0

    #xfrom = np.linspace(0,size,len(trace),endpoint=False)
    xfrom = [x / timeList[-1] * size for x in timeList]

    nbIt = len(timeList)
    xto = np.linspace(nbIt,size,nbIt,endpoint=True)
    print("xfrom : " + str(xfrom))

    xmargin = size /float( nbIt *5)
    print("xmargin : " + str(xmargin))
    image = (size - (nbIt-1)*xmargin)/float(nbIt)
    print("image : " + str(image))
    xto=np.arange(image/2,size,image+xmargin)
    print("xto : " + str(xto))

    print("xfrom lenght : " + str(len(xfrom)))



    for i in range(len(timeList)):
            plt.plot([xfrom[i],xto[i]],[yfrom,yto],color=lineColor,lw=lineWidth)

plt.xticks([])
plt.yticks([])





plt.show()











