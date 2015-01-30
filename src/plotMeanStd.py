import matplotlib.pyplot as plt
import sys
import numpy as np
import plotStyle



def readValue(valStr):
    """
    Convert data to float if possible otherwise it is text
    """
    try:
        res = float(valStr)
    except ValueError:
        res = valStr
    return res

def getModalitySpan(header,data,modalityName,fatherSpan=None):
    """
    data: array 2D
    modalityName: string modality name to find in the array
    return (columnModality,(lineStart,lineEnd+1)) relatively to another span
    or None if no other span
    """
    #If there is no father span we consider that it is the whole data
    if fatherSpan:
        adaptedFatherSpan = fatherSpan
    else:
        adaptedFatherSpan = (0,(0,len(data)))

    if modalityName in header:
        #If modality is in header, it on the whole father span
        modalityIndex = header.index(modalityName)
        return modalityIndex,adaptedFatherSpan[1]
    else:
        #Else we have to find it as column are like modalityName,modValue
        rangeStart = -1
        rangeEnd = -1
        modalityIndex = -1
        for i in range(*adaptedFatherSpan[1]):
            if rangeStart==-1 and modalityName in data[i]:
                rangeStart = i - adaptedFatherSpan[1][0]
                modalityIndex = int(np.where(data[i] == modalityName)[0])+1
            elif rangeStart != -1 and modalityName not in data[i]:
                rangeEnd = i+1 - adaptedFatherSpan[1][0]
        if rangeEnd == -1:
            #The end is the end of adaptedFather span
            rangeEnd = adaptedFatherSpan[1][1] - adaptedFatherSpan[1][0]
        return modalityIndex,(rangeStart,rangeEnd)



    pass

def getSetModality(data,modalitySpan):
    """
    Return the list of the modality values
    """
    modalities = []
    for i in range(*modalitySpan[1]):
        mod = data[i,modalitySpan[0]]
        if mod not in modalities:
            modalities.append(mod)
    return modalities




def readFile(fileName):
    """
    Return the header (first line)  and the data as np 2d array
    """
    data = np.loadtxt(fileName,dtype=np.str,ndmin=2,delimiter=",")
    header = file(fileName,'r').readline()
    header = header[2:-1]
    header = header.split(",")
    return (header,data)

def generateIndividuals(nbMod1,nbMod2,barWidth,interMod1Space=0.,interMod2Space=1.):
    ind = []
    print nbMod1
    print nbMod2
    for i in range(nbMod1):
        for j in range(nbMod2):
            ind.append(i*interMod2Space+j*(interMod1Space+barWidth))

    return np.array(ind,dtype=np.float)

def generateHeights(data,characColumn,modalitySpan1,modalitySpan2):
    """
    TODO finish to include span 2
    """
    height = []
    for i in range(*modalitySpan1[1]):
        height.append(data[i,characColumn])
    return np.array(height,dtype=np.float)

def generateErrors(data,characColumn,modalitySpan1,modalitySpan2):
    """
    TODO finish to include span 2
    """
    errors = []
    for i in range(*modalitySpan1[1]):
        errors.append(
            np.array(
                [data[i,characColumn+1],data[i,characColumn+2]],
                dtype=np.float)
        )
    return np.array(errors)



def generateLabels(mod1,mod2,modality1,modality2):
    labels = []
    for m1 in mod1:
        for m2 in mod2:
            labels.append(modality2 + ": "+m2)
    return labels

def generateColors(mod1,mod2):
    colors = ['red','green','blue','grey','black']
    ret = []
    for i in range(len(mod1)):
        for j in range(len(mod2)):
            ret.append(colors[j])
    return ret






def plot(fileInName,imageOutName="fig",charac="ErrorDist",
         modality1="scenario",modality2="nbStep"):
    """
    Perfor a barplot a one modality over another modality of one charach
    I      I I
    II  I  III
    III II III

    """

    header,data = readFile(fileInName) #transform data.csv in np.array
    modalitySpan1 = getModalitySpan(header,data,modality1)
    print modalitySpan1
    modalitySpan2 = getModalitySpan(header,data,modality2,modalitySpan1)
    print modalitySpan2
    characColumn = header.index(charac)
    mod1 = getSetModality(data,modalitySpan1)
    print mod1
    mod2 = getSetModality(data,modalitySpan2)
    print mod2
    nbMod1 = len(mod1)
    nbMod2 = len(mod2)

    barWidth = 0.1

    ind = generateIndividuals(nbMod1,nbMod2,barWidth=barWidth,interMod2Space=1)
    print ind
    heights = generateHeights(data,characColumn,modalitySpan1,modalitySpan2)
    print heights
    errors = generateErrors(data,characColumn,modalitySpan1,modalitySpan2)
    print errors
    labels = generateLabels(mod1,mod2,modality1,modality2)
    print labels
    colors = generateColors(mod1,mod2)
    print colors

    fig, ax = plt.subplots()
    for i in range(nbMod2):
        indexes = range(i,len(ind),nbMod2)
        ax.bar(ind[indexes],heights[indexes]
                      ,width=barWidth,yerr=np.transpose(errors[indexes]),
               color=colors[i],label=labels[i],ecolor='black')
    ax.set_xticks(ind[range(0,len(ind),nbMod2)]+nbMod2*barWidth/2.)
    ax.set_xticklabels(mod1)
    ax.set_ylabel('Distance Error')
    ax.legend(loc = 'upper left')
    plotStyle.saveFigure(imageOutName)
    plt.show()




if __name__ == "__main__":
    fileName = sys.argv[1]
    imageName = sys.argv[2]
    charcName = sys.argv[3]
    mod1 = sys.argv[4]
    mod2 = sys.argv[5]
    plot(fileInName=fileName,imageOutName=imageName,charac=charcName,
         modality1=mod1,modality2=mod2)



