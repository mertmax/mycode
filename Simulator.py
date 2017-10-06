# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 19:28:10 2017

@author: Efe
"""
import pandas as pd

import Utils 
import PatternDistribution as pattern

def evaluatePerfomance(cvSet,histRange,patternLenRange):
    perfomances = pd.DataFrame();
    for histSize in histRange:
        for patternLen in patternLenRange:
            perf = cvSet.loc[cvSet.patternLen==patternLen].loc[cvSet.histSize==histSize].ptr.mean()
            perfomances = perfomances.append(pd.DataFrame([[histSize, patternLen, perf]],columns = ["histSize", "patternLen", "perf"]))
    return perfomances

def crossValidatePatternDistribution(allData,histRange, patternLenRange,cvFold):
    cvSet = pd.DataFrame()
    dataSize = int((allData.shape[0] - allData.shape[0]%cvFold)/cvFold)
    for i in range(0,cvFold,1):
        data = allData[i*dataSize:(i+1)*dataSize]
        newCv = evalPatternDistribution(data,histRange, patternLenRange)
        newCv.loc[:,'fold'] = i
        cvSet =  cvSet.append(newCv)
    cvSet.reset_index(drop=True, inplace=True)
    return cvSet

def evalPatternDistribution(data, histRange, patternLenRange):
    result = pd.DataFrame()
    for histSize in histRange:
        for patternLen in patternLenRange:
            e, distribution, string, ptr, ppt = runPatternDistribution(data,
                histSize, patternLen, 5000, max(histRange), printStats = True )
            new_result = pd.DataFrame([[histSize,patternLen,ptr,ppt,e.log]],columns = ["histSize","patternLen","ptr","ppt","log"])
            result = result.append(new_result)
    result.reset_index(drop=True, inplace=True)
    return result

def runPatternDistribution(data,histSize,patternLen,runPeriods,maxHistLen,printStats = False):
    e, distribution, string = pattern.run(data, histSize, runPeriods, patternLen, maxHistLen )
    ptr = e.getPTR()
    ppt = e.getPPT()
    if printStats:   
        print("History: " + "{0:3.0f}".format(histSize) +
          " Pattern length: " + str(patternLen)+ 
          " PTR: " + "{0:.3f}".format(ptr)+
          " PPT: %" + "{0: .2f}".format(ppt*100))
    return e, distribution, string, ptr, ppt

def testBuyOnly(data,histRange):
    perfomances = pd.DataFrame()
    for histSize in histRange:
        eBuy = pattern.runBuy(data,histSize,max(histRange))
        perfomances = perfomances.append(pd.DataFrame([[histSize, 0, eBuy.getPTR()]],columns = ["histSize", "patternLen", "perf"]))
    Utils.plotPerfHeatmap(perfomances)
    return eBuy
#datafile  = "USDTRY-1440-HLOC-lag0-2017.08.08.csv"
#data = Utils.readMT4data(datafile, 1000)

#datafile  = "C:\\Users\\max\\Google Drive\\Thesis\\Data\\Investing.csv"
#data = Utils.readInvData(datafile)
histRange = (20, 50, 100, 150, 200)
patternLenRange = (3, 4, 5, 6)

datafile  = r"C:\Investing.csv"
filedata = Utils.readInvData(datafile)
alldata = filedata[:-300]
alldata = alldata[-(max(histRange)+2*100):]  #262
data = alldata[:-100]
valData = alldata[-(max(histRange)+100):]

#datafile = "C:\\Users\\max\\Google Drive\\Thesis\\Data\\BTC_HOURLY_OHLC.csv"
#data = Utils.readBTCdata(datafile)

cvFold = 1
cvSet= crossValidatePatternDistribution(data,histRange, patternLenRange,cvFold)
modelPerf= evaluatePerfomance(cvSet,histRange,patternLenRange)
Utils.plotPerfHeatmap(modelPerf)
eBuy = testBuyOnly(data,histRange)

print("\nvalidation\n")

cvFold = 1
cvSet= crossValidatePatternDistribution(valData,histRange, patternLenRange,cvFold)
modelPerf= evaluatePerfomance(cvSet,histRange,patternLenRange)
Utils.plotPerfHeatmap(modelPerf)
eBuy = testBuyOnly(valData,histRange)


#e, distribution, string, ptr, ppt = runPatternDistribution(valData,histSize=50,patternLen=7,runPeriods=5000,maxHistLen=200,printStats=True)


