import matplotlib.pyplot as plt



def getBarStyle():
    return dict(
        ecolor='black',
    )

def getColorsStyle():
    return ['red','green','blue']



def getSaveParams():
    return dict(
        transparent=True,
        dpi=300,
    )

def saveFigure(fileName):
    kwargs =getSaveParams()
    plt.savefig(fileName+".png",format='png',**kwargs)
    plt.savefig(fileName+".eps",format='eps',**kwargs)
