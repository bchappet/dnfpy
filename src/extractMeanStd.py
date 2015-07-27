import scikits.bootstrap as boot
import numpy as np
import sys
#python runExperimentpy "['ModelDNF']" "[]" "['ScenarioTracking','ScenarioNoise','ScenarioDistracters']" 100 10 dnf_nbStep log



def getMeanStdFile(fileInName,fileOutName,nbRepetition=100):
    fileIn = file(fileInName,'r')
    header = fileIn.readline().rstrip()
    headerList = header.split(",")
    columCharac = headerList.index('it')
    columnConvergenceIndex = headerList.index('ConvergenceTime')
    print headerList

    linesToSaveMean = []
    linesToSaveBoot = []

    textArray = fileIn.read()
    textArray = textArray.split('\n')


    array = np.genfromtxt(fileInName,delimiter=",",skip_header=1,
                          missing_values="None",filling_values=np.nan,
                       usecols=range(columCharac+1,len(headerList)),autostrip=True)

    print array

    for i in range(0,len(array),nbRepetition):
        line = textArray[i]
        lineArray = line.split(',')
        means = []
        bootstraps = []
        nbNan = 0

        subArray = array[i:i+nbRepetition,:]
        for j in range(len(subArray[0])):
            column = subArray[:,j]
            columnWithoutNan = column[~np.isnan(column)]
            mean = np.mean(columnWithoutNan,axis=0)
            std = np.std(columnWithoutNan)
            if std > 0:
                bootstrap =  boot.ci(columnWithoutNan,output='errorbar')
            else:
                bootstrap = np.array([[0.],[0.]])

            bootstraps.append(mean)
            bootstraps.extend(list(bootstrap.flatten()))
            means.append(mean)
            if j == columnConvergenceIndex - columCharac-1:
                nbNan = len(column) - len(columnWithoutNan)

        means.append(nbNan)
        bootstraps.append(nbNan)
        strMeans = np.array(means,dtype=np.str)
        strBoots = np.array(bootstraps,dtype=np.str)
        lineMean = np.append(lineArray[0:columCharac],strMeans)
        lineBoot = np.append(lineArray[0:columCharac],strBoots)
        print(lineMean)
        print(lineBoot)
        linesToSaveMean.append(lineMean)
        linesToSaveBoot.append(lineBoot)
        headerBootList = headerList[0:columCharac]
        for i in range(columCharac+1,len(headerList)):
            headerBootList.append(headerList[i])
            headerBootList.append(headerList[i]+"_down")
            headerBootList.append(headerList[i]+"_up")
        headerBoot = ",".join(headerBootList)

    np.savetxt(fileOutName+"_mean.csv",np.array(linesToSaveMean),fmt='%s',delimiter=",",header=header+",nbNoFocus")
    np.savetxt(fileOutName+"_std.csv",np.array(linesToSaveBoot),fmt='%s',delimiter=",",header=headerBoot+",nbNoFocus")


if __name__ == "__main__":
    getMeanStdFile(sys.argv[1],sys.argv[2],nbRepetition=eval(sys.argv[3]))









